"""
AI-powered content categorization service
"""

import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import requests
from typing import Optional, List, Dict, Any
import re
from utils.config import Config
import torch

class CategorizationService:
    """Handles content categorization using AI models"""
    
    def __init__(self):
        self.config = Config()
        self.classifier = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize categorization models"""
        try:
            # Initialize zero-shot classification pipeline
            if self.config.HUGGINGFACE_API_KEY:
                # Use API for better performance
                self.hf_api_url = "https://api-inference.huggingface.co/models/"
                self.hf_headers = {"Authorization": f"Bearer {self.config.HUGGINGFACE_API_KEY}"}
            else:
                # Load local model
                try:
                    self.classifier = pipeline(
                        "zero-shot-classification",
                        model=self.config.CATEGORIZATION_MODEL,
                        device=0 if self.device == "cuda" else -1
                    )
                except Exception as e:
                    st.warning(f"Could not load local categorization model: {str(e)}")
                    self.classifier = None
                    
        except Exception as e:
            st.error(f"Categorization service initialization error: {str(e)}")
    
    def categorize_content(self, content: str, content_type: str = "") -> Optional[str]:
        """
        Categorize content into predefined themes
        
        Args:
            content: Text content to categorize
            content_type: Type of content (proverb, folk tale, etc.)
            
        Returns:
            Category name or None if categorization fails
        """
        if not content or not content.strip():
            return None
        
        # Try multiple categorization methods
        methods = [
            self._categorize_with_huggingface_api,
            self._categorize_with_huggingface_local,
            self._categorize_with_keywords,
            self._categorize_with_rules
        ]
        
        for method in methods:
            try:
                result = method(content, content_type)
                if result:
                    return result
            except Exception as e:
                st.warning(f"Categorization method failed: {str(e)}")
                continue
        
        return "Tradition & Culture"  # Default category
    
    def _categorize_with_huggingface_api(self, content: str, content_type: str) -> Optional[str]:
        """Categorize using Hugging Face API"""
        if not self.config.HUGGINGFACE_API_KEY:
            return None
        
        model_name = self.config.CATEGORIZATION_MODEL
        api_url = f"{self.hf_api_url}{model_name}"
        
        # Prepare the classification task
        candidate_labels = self.config.CATEGORIES
        
        payload = {
            "inputs": content,
            "parameters": {
                "candidate_labels": candidate_labels
            }
        }
        
        response = requests.post(api_url, headers=self.hf_headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if "labels" in result and len(result["labels"]) > 0:
                # Return the highest scoring category
                return result["labels"][0]
        
        return None
    
    def _categorize_with_huggingface_local(self, content: str, content_type: str) -> Optional[str]:
        """Categorize using local Hugging Face model"""
        if not self.classifier:
            return None
        
        try:
            candidate_labels = self.config.CATEGORIES
            result = self.classifier(content, candidate_labels)
            
            if "labels" in result and len(result["labels"]) > 0:
                return result["labels"][0]
                
        except Exception as e:
            st.warning(f"Local HF categorization failed: {str(e)}")
        
        return None
    
    def _categorize_with_keywords(self, content: str, content_type: str) -> Optional[str]:
        """Categorize using keyword matching"""
        content_lower = content.lower()
        
        # Define keywords for each category
        category_keywords = {
            "Wisdom & Life Lessons": [
                "wisdom", "lesson", "learn", "experience", "advice", "guidance",
                "truth", "knowledge", "understanding", "insight", "prudence",
                "wise", "sage", "elder", "teaching", "moral", "principle"
            ],
            "Love & Relationships": [
                "love", "heart", "romance", "marriage", "wedding", "couple",
                "relationship", "partner", "beloved", "affection", "passion",
                "dating", "courtship", "bride", "groom", "husband", "wife"
            ],
            "Family & Community": [
                "family", "mother", "father", "child", "parent", "sibling",
                "community", "village", "neighbor", "friend", "together",
                "unity", "bond", "kinship", "clan", "tribe", "home"
            ],
            "Nature & Environment": [
                "nature", "tree", "forest", "river", "mountain", "sea", "ocean",
                "animal", "bird", "flower", "plant", "earth", "sky", "sun",
                "moon", "star", "weather", "season", "rain", "wind"
            ],
            "Courage & Heroism": [
                "courage", "brave", "hero", "warrior", "fight", "battle",
                "strength", "valor", "fearless", "bold", "daring", "gallant",
                "champion", "defender", "protector", "rescue", "victory"
            ],
            "Morality & Ethics": [
                "moral", "ethics", "right", "wrong", "good", "evil", "virtue",
                "sin", "justice", "fairness", "honest", "truth", "lie",
                "integrity", "character", "conscience", "duty", "responsibility"
            ],
            "Spirituality & Faith": [
                "god", "divine", "spiritual", "prayer", "faith", "belief",
                "religion", "sacred", "holy", "temple", "church", "mosque",
                "meditation", "soul", "spirit", "blessing", "miracle"
            ],
            "Work & Perseverance": [
                "work", "labor", "effort", "perseverance", "persistence",
                "dedication", "hard work", "diligence", "industry", "craft",
                "skill", "profession", "job", "career", "success", "achievement"
            ],
            "Humor & Wit": [
                "funny", "humor", "joke", "laugh", "wit", "clever", "amusing",
                "comic", "silly", "ridiculous", "absurd", "irony", "sarcasm",
                "trickster", "fool", "jest", "merry", "cheerful"
            ],
            "Tradition & Culture": [
                "tradition", "culture", "custom", "ritual", "ceremony",
                "festival", "celebration", "heritage", "ancestor", "legacy",
                "folklore", "myth", "legend", "ancient", "old", "historical"
            ],
            "Children's Tales": [
                "child", "children", "young", "little", "small", "innocent",
                "play", "toy", "game", "school", "student", "pupil",
                "fairy", "magic", "wonder", "imagination", "dream"
            ],
            "Historical Stories": [
                "history", "historical", "past", "ancient", "old", "time",
                "king", "queen", "ruler", "empire", "kingdom", "war",
                "battle", "conquest", "dynasty", "chronicle", "legend"
            ]
        }
        
        # Score each category based on keyword matches
        category_scores = {}
        
        for category, keywords in category_keywords.items():
            score = 0
            for keyword in keywords:
                # Count occurrences of each keyword
                score += content_lower.count(keyword)
                # Bonus for exact word matches
                if re.search(r'\b' + re.escape(keyword) + r'\b', content_lower):
                    score += 2
            
            category_scores[category] = score
        
        # Return category with highest score
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            if category_scores[best_category] > 0:
                return best_category
        
        return None
    
    def _categorize_with_rules(self, content: str, content_type: str) -> Optional[str]:
        """Categorize using rule-based approach"""
        content_lower = content.lower()
        
        # Content type specific rules
        if content_type.lower() == "proverb":
            # Proverbs often contain wisdom
            if any(word in content_lower for word in ["wise", "fool", "learn", "teach"]):
                return "Wisdom & Life Lessons"
        
        elif content_type.lower() == "folk tale":
            # Folk tales often involve traditional stories
            if any(word in content_lower for word in ["once upon", "long ago", "ancient"]):
                return "Tradition & Culture"
        
        elif content_type.lower() == "children's tale":
            return "Children's Tales"
        
        # Length-based rules
        if len(content.split()) < 20:
            # Short content is likely a saying or proverb
            return "Wisdom & Life Lessons"
        
        # Pattern-based rules
        if re.search(r'\b(he who|she who|those who)\b', content_lower):
            return "Wisdom & Life Lessons"
        
        if re.search(r'\b(love|heart|beloved)\b', content_lower):
            return "Love & Relationships"
        
        if re.search(r'\b(mother|father|family|child)\b', content_lower):
            return "Family & Community"
        
        return None
    
    def get_category_confidence(self, content: str, category: str) -> float:
        """
        Get confidence score for a category assignment
        
        Args:
            content: Original content
            category: Assigned category
            
        Returns:
            Confidence score between 0 and 1
        """
        if not content or not category:
            return 0.0
        
        # Use keyword matching to estimate confidence
        content_lower = content.lower()
        
        # Get keywords for the assigned category
        category_keywords = self._get_category_keywords().get(category, [])
        
        if not category_keywords:
            return 0.5  # Medium confidence for unknown categories
        
        # Count keyword matches
        matches = 0
        total_keywords = len(category_keywords)
        
        for keyword in category_keywords:
            if keyword in content_lower:
                matches += 1
        
        # Calculate confidence based on keyword density
        keyword_density = matches / total_keywords
        content_length_factor = min(len(content.split()) / 50, 1.0)  # Longer content = higher confidence
        
        confidence = (keyword_density * 0.7) + (content_length_factor * 0.3)
        return min(confidence, 1.0)
    
    def _get_category_keywords(self) -> Dict[str, List[str]]:
        """Get keywords for each category"""
        return {
            "Wisdom & Life Lessons": ["wisdom", "lesson", "learn", "wise", "advice"],
            "Love & Relationships": ["love", "heart", "romance", "marriage", "relationship"],
            "Family & Community": ["family", "mother", "father", "community", "together"],
            "Nature & Environment": ["nature", "tree", "forest", "river", "animal"],
            "Courage & Heroism": ["courage", "brave", "hero", "warrior", "strength"],
            "Morality & Ethics": ["moral", "right", "wrong", "good", "virtue"],
            "Spirituality & Faith": ["god", "spiritual", "prayer", "faith", "sacred"],
            "Work & Perseverance": ["work", "effort", "perseverance", "dedication", "success"],
            "Humor & Wit": ["funny", "humor", "joke", "laugh", "wit"],
            "Tradition & Culture": ["tradition", "culture", "custom", "heritage", "folklore"],
            "Children's Tales": ["child", "children", "young", "play", "magic"],
            "Historical Stories": ["history", "ancient", "king", "war", "past"]
        }
    
    def suggest_alternative_categories(self, content: str, current_category: str) -> List[str]:
        """
        Suggest alternative categories for content
        
        Args:
            content: Content to analyze
            current_category: Currently assigned category
            
        Returns:
            List of alternative category suggestions
        """
        alternatives = []
        
        # Get scores for all categories
        category_scores = {}
        
        for category in self.config.CATEGORIES:
            if category != current_category:
                confidence = self.get_category_confidence(content, category)
                category_scores[category] = confidence
        
        # Sort by confidence and return top 3
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        alternatives = [cat for cat, score in sorted_categories[:3] if score > 0.1]
        
        return alternatives
    
    def batch_categorize(self, contents: List[str], content_types: List[str] = None) -> List[str]:
        """
        Categorize multiple contents in batch
        
        Args:
            contents: List of content texts
            content_types: List of content types (optional)
            
        Returns:
            List of categories
        """
        if content_types is None:
            content_types = [""] * len(contents)
        
        categories = []
        
        for i, content in enumerate(contents):
            content_type = content_types[i] if i < len(content_types) else ""
            category = self.categorize_content(content, content_type)
            categories.append(category or "Tradition & Culture")
        
        return categories
