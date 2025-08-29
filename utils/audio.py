"""
Audio processing service for voice-to-text conversion using Whisper
"""

import streamlit as st
import whisper
import tempfile
import os
from typing import Optional, Dict, Any
import numpy as np
from pydub import AudioSegment
import io
from utils.config import Config

class AudioProcessor:
    """Handles audio recording and speech-to-text conversion"""
    
    def __init__(self):
        self.config = Config()
        self.whisper_model = None
        self._initialize_whisper()
    
    def _initialize_whisper(self):
        """Initialize Whisper model"""
        try:
            # Load Whisper model
            model_size = self.config.WHISPER_MODEL
            self.whisper_model = whisper.load_model(model_size)
            st.success(f"Whisper model '{model_size}' loaded successfully")
            
        except Exception as e:
            st.error(f"Failed to load Whisper model: {str(e)}")
            self.whisper_model = None
    
    def transcribe_audio(self, audio_data: bytes, language: str = None) -> Optional[str]:
        """
        Transcribe audio to text using Whisper
        
        Args:
            audio_data: Audio data in bytes
            language: Language code for transcription (optional)
            
        Returns:
            Transcribed text or None if transcription fails
        """
        if not self.whisper_model:
            st.error("Whisper model not available")
            return None
        
        try:
            # Save audio data to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            # Transcribe audio
            transcription_options = {
                "fp16": False,  # Use fp32 for better compatibility
                "language": language if language and language != "auto" else None
            }
            
            result = self.whisper_model.transcribe(temp_file_path, **transcription_options)
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            # Extract text from result
            if result and "text" in result:
                transcribed_text = result["text"].strip()
                
                # Get additional information
                detected_language = result.get("language", "unknown")
                confidence = self._calculate_confidence(result)
                
                # Store additional info in session state for debugging
                st.session_state.last_transcription_info = {
                    "detected_language": detected_language,
                    "confidence": confidence,
                    "segments": result.get("segments", [])
                }
                
                return transcribed_text
            
        except Exception as e:
            st.error(f"Transcription failed: {str(e)}")
            
        return None
    
    def _calculate_confidence(self, whisper_result: Dict[str, Any]) -> float:
        """
        Calculate confidence score from Whisper result
        
        Args:
            whisper_result: Result from Whisper transcription
            
        Returns:
            Confidence score between 0 and 1
        """
        try:
            segments = whisper_result.get("segments", [])
            if not segments:
                return 0.5  # Default confidence
            
            # Calculate average confidence from segments
            total_confidence = 0
            total_duration = 0
            
            for segment in segments:
                # Whisper doesn't always provide confidence scores
                # Use no_speech_prob as inverse confidence indicator
                no_speech_prob = segment.get("no_speech_prob", 0.5)
                segment_confidence = 1.0 - no_speech_prob
                
                duration = segment.get("end", 0) - segment.get("start", 0)
                total_confidence += segment_confidence * duration
                total_duration += duration
            
            if total_duration > 0:
                return total_confidence / total_duration
            else:
                return 0.5
                
        except Exception:
            return 0.5
    
    def preprocess_audio(self, audio_data: bytes) -> bytes:
        """
        Preprocess audio for better transcription quality
        
        Args:
            audio_data: Raw audio data
            
        Returns:
            Processed audio data
        """
        try:
            # Load audio using pydub
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            # Normalize audio
            audio = audio.normalize()
            
            # Convert to mono if stereo
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Set sample rate to 16kHz (Whisper's preferred rate)
            audio = audio.set_frame_rate(self.config.AUDIO_SAMPLE_RATE)
            
            # Limit duration
            max_duration_ms = self.config.MAX_AUDIO_DURATION * 1000
            if len(audio) > max_duration_ms:
                audio = audio[:max_duration_ms]
                st.warning(f"Audio truncated to {self.config.MAX_AUDIO_DURATION} seconds")
            
            # Export processed audio
            output_buffer = io.BytesIO()
            audio.export(output_buffer, format="wav")
            return output_buffer.getvalue()
            
        except Exception as e:
            st.warning(f"Audio preprocessing failed: {str(e)}")
            return audio_data  # Return original if preprocessing fails
    
    def validate_audio(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Validate audio data and return information
        
        Args:
            audio_data: Audio data to validate
            
        Returns:
            Dictionary with validation results and audio info
        """
        validation_result = {
            "is_valid": False,
            "duration": 0,
            "sample_rate": 0,
            "channels": 0,
            "format": "unknown",
            "size_mb": 0,
            "warnings": [],
            "errors": []
        }
        
        try:
            # Load audio for analysis
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            # Extract information
            validation_result["duration"] = len(audio) / 1000.0  # Convert to seconds
            validation_result["sample_rate"] = audio.frame_rate
            validation_result["channels"] = audio.channels
            validation_result["size_mb"] = len(audio_data) / (1024 * 1024)
            
            # Validate duration
            if validation_result["duration"] > self.config.MAX_AUDIO_DURATION:
                validation_result["warnings"].append(
                    f"Audio duration ({validation_result['duration']:.1f}s) exceeds maximum "
                    f"({self.config.MAX_AUDIO_DURATION}s). Will be truncated."
                )
            
            if validation_result["duration"] < 1.0:
                validation_result["warnings"].append("Audio is very short (< 1 second)")
            
            # Validate sample rate
            if validation_result["sample_rate"] < 8000:
                validation_result["warnings"].append("Low sample rate may affect transcription quality")
            
            # Validate file size
            if validation_result["size_mb"] > 25:  # Streamlit's default upload limit
                validation_result["errors"].append("Audio file too large (> 25MB)")
            
            # Check if audio has content
            if audio.max_possible_amplitude == 0:
                validation_result["errors"].append("Audio appears to be silent")
            
            validation_result["is_valid"] = len(validation_result["errors"]) == 0
            
        except Exception as e:
            validation_result["errors"].append(f"Failed to analyze audio: {str(e)}")
        
        return validation_result
    
    def get_supported_formats(self) -> list:
        """Get list of supported audio formats"""
        return [
            "wav", "mp3", "m4a", "ogg", "flac", "aac", "wma"
        ]
    
    def convert_audio_format(self, audio_data: bytes, target_format: str = "wav") -> bytes:
        """
        Convert audio to specified format
        
        Args:
            audio_data: Input audio data
            target_format: Target format (wav, mp3, etc.)
            
        Returns:
            Converted audio data
        """
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            output_buffer = io.BytesIO()
            audio.export(output_buffer, format=target_format)
            return output_buffer.getvalue()
            
        except Exception as e:
            st.error(f"Audio conversion failed: {str(e)}")
            return audio_data
    
    def extract_audio_features(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Extract features from audio for quality assessment
        
        Args:
            audio_data: Audio data to analyze
            
        Returns:
            Dictionary with audio features
        """
        features = {
            "rms_energy": 0,
            "zero_crossing_rate": 0,
            "spectral_centroid": 0,
            "signal_to_noise_ratio": 0,
            "quality_score": 0
        }
        
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            # Convert to numpy array for analysis
            samples = np.array(audio.get_array_of_samples())
            if audio.channels == 2:
                samples = samples.reshape((-1, 2))
                samples = samples.mean(axis=1)  # Convert to mono
            
            # Normalize samples
            samples = samples.astype(np.float32) / np.max(np.abs(samples))
            
            # Calculate RMS energy
            features["rms_energy"] = np.sqrt(np.mean(samples**2))
            
            # Calculate zero crossing rate
            zero_crossings = np.where(np.diff(np.sign(samples)))[0]
            features["zero_crossing_rate"] = len(zero_crossings) / len(samples)
            
            # Simple quality score based on energy and consistency
            energy_score = min(features["rms_energy"] * 10, 1.0)  # Normalize to 0-1
            consistency_score = 1.0 - min(features["zero_crossing_rate"] * 2, 1.0)
            features["quality_score"] = (energy_score + consistency_score) / 2
            
        except Exception as e:
            st.warning(f"Feature extraction failed: {str(e)}")
        
        return features
    
    def get_transcription_tips(self) -> list:
        """Get tips for better transcription quality"""
        return [
            "🎤 Speak clearly and at a moderate pace",
            "🔇 Record in a quiet environment with minimal background noise",
            "📱 Hold the microphone close to your mouth (6-12 inches)",
            "⏱️ Keep recordings under 5 minutes for best results",
            "🗣️ Speak in your native language for better accuracy",
            "🔊 Ensure adequate volume - not too loud or too quiet",
            "⏸️ Pause briefly between sentences",
            "📝 Spell out numbers and special terms clearly",
            "🎯 Focus on one story or topic per recording",
            "🔄 Re-record if you make mistakes rather than continuing"
        ]
    
    def estimate_transcription_time(self, audio_duration: float) -> float:
        """
        Estimate time needed for transcription
        
        Args:
            audio_duration: Duration of audio in seconds
            
        Returns:
            Estimated transcription time in seconds
        """
        # Whisper typically processes audio at 2-10x real-time speed
        # depending on model size and hardware
        model_speed_factor = {
            "tiny": 8,
            "base": 6,
            "small": 4,
            "medium": 2,
            "large": 1
        }
        
        speed_factor = model_speed_factor.get(self.config.WHISPER_MODEL, 4)
        estimated_time = audio_duration / speed_factor
        
        # Add some buffer time
        return max(estimated_time * 1.5, 5)  # Minimum 5 seconds
