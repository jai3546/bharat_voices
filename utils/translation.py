"""
Translation service using Hugging Face transformers and other translation APIs
"""

import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import requests
from deep_translator import GoogleTranslator, MyMemoryTranslator
from typing import Optional, Dict, Any
import os
from utils.config import Config
import torch

class TranslationService:
    """Handles text translation using multiple services"""
    
    def __init__(self):
        self.config = Config()
        self.hf_translator = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize translation models"""
        try:
            # Initialize Hugging Face translation pipeline
            if self.config.HUGGINGFACE_API_KEY:
                # Use API for better performance
                self.hf_api_url = "https://api-inference.huggingface.co/models/"
                self.hf_headers = {"Authorization": f"Bearer {self.config.HUGGINGFACE_API_KEY}"}
            else:
                # Load local model (slower but free)
                try:
                    self.hf_translator = pipeline(
                        "translation",
                        model=self.config.TRANSLATION_MODEL,
                        device=0 if self.device == "cuda" else -1
                    )
                except Exception as e:
                    st.warning(f"Could not load local translation model: {str(e)}")
                    self.hf_translator = None
                    
        except Exception as e:
            st.error(f"Translation service initialization error: {str(e)}")
    
    def translate_text(self, text: str, source_lang: str = "auto", target_lang: str = "en") -> Optional[str]:
        """
        Translate text using the best available method
        
        Args:
            text: Text to translate
            source_lang: Source language code (ISO 639-1)
            target_lang: Target language code (ISO 639-1)
            
        Returns:
            Translated text or None if translation fails
        """
        if not text or not text.strip():
            return None
        
        # Try multiple translation methods in order of preference
        translation_methods = [
            self._translate_with_huggingface_api,
            self._translate_with_huggingface_local,
            self._translate_with_google,
            self._translate_with_mymemory
        ]
        
        for method in translation_methods:
            try:
                result = method(text, source_lang, target_lang)
                if result and result.strip() and result.lower() != text.lower():
                    return result
            except Exception as e:
                st.warning(f"Translation method failed: {str(e)}")
                continue
        
        return None
    
    def _translate_with_huggingface_api(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Translate using Hugging Face API"""
        if not self.config.HUGGINGFACE_API_KEY:
            return None
        
        # Map language codes to model names
        model_map = {
            ("hi", "en"): "Helsinki-NLP/opus-mt-hi-en",
            ("bn", "en"): "Helsinki-NLP/opus-mt-bn-en",
            ("te", "en"): "Helsinki-NLP/opus-mt-te-en",
            ("ta", "en"): "Helsinki-NLP/opus-mt-ta-en",
            ("mr", "en"): "Helsinki-NLP/opus-mt-mr-en",
            ("gu", "en"): "Helsinki-NLP/opus-mt-gu-en",
            ("kn", "en"): "Helsinki-NLP/opus-mt-kn-en",
            ("ml", "en"): "Helsinki-NLP/opus-mt-ml-en",
            ("pa", "en"): "Helsinki-NLP/opus-mt-pa-en",
            ("ur", "en"): "Helsinki-NLP/opus-mt-ur-en",
            ("ne", "en"): "Helsinki-NLP/opus-mt-ne-en",
            ("si", "en"): "Helsinki-NLP/opus-mt-si-en",
            ("zh", "en"): "Helsinki-NLP/opus-mt-zh-en",
            ("ja", "en"): "Helsinki-NLP/opus-mt-ja-en",
            ("ko", "en"): "Helsinki-NLP/opus-mt-ko-en",
            ("ar", "en"): "Helsinki-NLP/opus-mt-ar-en",
            ("fa", "en"): "Helsinki-NLP/opus-mt-fa-en",
            ("tr", "en"): "Helsinki-NLP/opus-mt-tr-en",
            ("ru", "en"): "Helsinki-NLP/opus-mt-ru-en",
            ("de", "en"): "Helsinki-NLP/opus-mt-de-en",
            ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
            ("es", "en"): "Helsinki-NLP/opus-mt-es-en",
            ("pt", "en"): "Helsinki-NLP/opus-mt-pt-en",
            ("it", "en"): "Helsinki-NLP/opus-mt-it-en",
            ("nl", "en"): "Helsinki-NLP/opus-mt-nl-en",
            ("sv", "en"): "Helsinki-NLP/opus-mt-sv-en",
            ("no", "en"): "Helsinki-NLP/opus-mt-no-en",
            ("da", "en"): "Helsinki-NLP/opus-mt-da-en",
            ("fi", "en"): "Helsinki-NLP/opus-mt-fi-en",
            ("pl", "en"): "Helsinki-NLP/opus-mt-pl-en",
            ("cs", "en"): "Helsinki-NLP/opus-mt-cs-en",
            ("hu", "en"): "Helsinki-NLP/opus-mt-hu-en",
            ("ro", "en"): "Helsinki-NLP/opus-mt-ro-en",
            ("bg", "en"): "Helsinki-NLP/opus-mt-bg-en",
            ("hr", "en"): "Helsinki-NLP/opus-mt-hr-en",
            ("sr", "en"): "Helsinki-NLP/opus-mt-sr-en",
            ("sk", "en"): "Helsinki-NLP/opus-mt-sk-en",
            ("sl", "en"): "Helsinki-NLP/opus-mt-sl-en",
            ("et", "en"): "Helsinki-NLP/opus-mt-et-en",
            ("lv", "en"): "Helsinki-NLP/opus-mt-lv-en",
            ("lt", "en"): "Helsinki-NLP/opus-mt-lt-en"
        }
        
        model_name = model_map.get((source_lang, target_lang))
        if not model_name:
            # Try multilingual model
            model_name = "Helsinki-NLP/opus-mt-mul-en"
        
        api_url = f"{self.hf_api_url}{model_name}"
        
        payload = {"inputs": text}
        response = requests.post(api_url, headers=self.hf_headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("translation_text", "")
        
        return None
    
    def _translate_with_huggingface_local(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Translate using local Hugging Face model"""
        if not self.hf_translator:
            return None
        
        try:
            result = self.hf_translator(text, max_length=512)
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("translation_text", "")
        except Exception as e:
            st.warning(f"Local HF translation failed: {str(e)}")
        
        return None
    
    def _translate_with_google(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Translate using Google Translator (free tier)"""
        try:
            # Handle auto-detection
            if source_lang == "auto":
                translator = GoogleTranslator(target=target_lang)
            else:
                translator = GoogleTranslator(source=source_lang, target=target_lang)
            
            result = translator.translate(text)
            return result
            
        except Exception as e:
            st.warning(f"Google translation failed: {str(e)}")
            return None
    
    def _translate_with_mymemory(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Translate using MyMemory translator (free tier)"""
        try:
            if source_lang == "auto":
                # MyMemory doesn't support auto-detection well
                return None
            
            translator = MyMemoryTranslator(source=source_lang, target=target_lang)
            result = translator.translate(text)
            return result
            
        except Exception as e:
            st.warning(f"MyMemory translation failed: {str(e)}")
            return None
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of the given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code or None if detection fails
        """
        try:
            from langdetect import detect
            detected_lang = detect(text)
            return detected_lang
        except Exception as e:
            st.warning(f"Language detection failed: {str(e)}")
            return None
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return self.config.LANGUAGES
    
    def batch_translate(self, texts: list, source_lang: str = "auto", target_lang: str = "en") -> list:
        """
        Translate multiple texts in batch
        
        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            List of translated texts
        """
        translations = []
        
        for text in texts:
            translation = self.translate_text(text, source_lang, target_lang)
            translations.append(translation or text)  # Fallback to original if translation fails
        
        return translations
    
    def get_translation_confidence(self, original: str, translated: str) -> float:
        """
        Estimate translation confidence based on simple heuristics
        
        Args:
            original: Original text
            translated: Translated text
            
        Returns:
            Confidence score between 0 and 1
        """
        if not original or not translated:
            return 0.0
        
        # Simple heuristics for confidence
        confidence = 1.0
        
        # Penalize if translation is identical (might indicate failure)
        if original.lower() == translated.lower():
            confidence *= 0.3
        
        # Penalize if translation is much shorter or longer
        length_ratio = len(translated) / len(original)
        if length_ratio < 0.3 or length_ratio > 3.0:
            confidence *= 0.5
        
        # Penalize if translation contains many non-alphabetic characters
        alpha_ratio = sum(c.isalpha() for c in translated) / len(translated)
        if alpha_ratio < 0.5:
            confidence *= 0.7
        
        return min(confidence, 1.0)
    
    def suggest_improvements(self, original: str, translated: str) -> list:
        """
        Suggest improvements for translation
        
        Args:
            original: Original text
            translated: Translated text
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        if not translated or translated.strip() == "":
            suggestions.append("Translation appears to be empty. Try a different translation service.")
        
        if original.lower() == translated.lower():
            suggestions.append("Translation is identical to original. Check if the source language is correct.")
        
        confidence = self.get_translation_confidence(original, translated)
        if confidence < 0.5:
            suggestions.append("Translation confidence is low. Consider manual review or alternative translation.")
        
        # Check for common translation issues
        if len(translated.split()) < len(original.split()) * 0.3:
            suggestions.append("Translation seems too short. Some meaning might be lost.")
        
        if len(translated.split()) > len(original.split()) * 3:
            suggestions.append("Translation seems too long. It might be overly verbose.")
        
        return suggestions
