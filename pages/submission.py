"""
Story submission page for Bharat Voices
"""

import streamlit as st
import uuid
from datetime import datetime
import tempfile
import os
from typing import Dict, Any, Optional

# Import utility modules
from utils.config import Config
from utils.database import DatabaseManager
from utils.translation import TranslationService
from utils.categorization import CategorizationService
from utils.audio import AudioProcessor

def show_submission_page():
    """Display the story submission page"""
    st.markdown("## 📝 Share Your Cultural Story")
    st.markdown("Help preserve cultural wisdom by sharing proverbs, folk tales, sayings, or stories from your heritage.")
    
    # Initialize services
    config = Config()
    db_manager = DatabaseManager()
    translation_service = TranslationService()
    categorization_service = CategorizationService()
    audio_processor = AudioProcessor()
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["✍️ Text Input", "🎤 Voice Input"])
    
    with tab1:
        show_text_submission_form(config, db_manager, translation_service, categorization_service)
    
    with tab2:
        show_voice_submission_form(config, db_manager, translation_service, categorization_service, audio_processor)

def show_text_submission_form(config: Config, db_manager: DatabaseManager, 
                             translation_service: TranslationService, 
                             categorization_service: CategorizationService):
    """Show text-based submission form"""
    
    with st.form("text_submission_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Basic information
            st.markdown("### 📋 Story Details")
            
            title = st.text_input(
                "Title *",
                placeholder="Enter a title for your story...",
                max_chars=config.MAX_TITLE_LENGTH,
                help="Give your story a meaningful title"
            )
            
            content = st.text_area(
                "Content *",
                placeholder="Share your proverb, folk tale, saying, or story...",
                height=200,
                max_chars=config.MAX_TEXT_LENGTH,
                help="Write in your native language. AI will help translate it."
            )
            
            cultural_context = st.text_area(
                "Cultural Context (Optional)",
                placeholder="Provide background about when/how this story is used...",
                height=100,
                help="Help others understand the cultural significance"
            )
        
        with col2:
            # Metadata
            st.markdown("### 🏷️ Classification")
            
            content_type = st.selectbox(
                "Content Type *",
                options=config.CONTENT_TYPES,
                help="What type of cultural content is this?"
            )
            
            language = st.selectbox(
                "Language *",
                options=list(config.LANGUAGES.values()),
                help="What language is your story written in?"
            )
            
            dialect = st.text_input(
                "Dialect/Region (Optional)",
                placeholder="e.g., Punjabi (Malwai), Tamil (Madras)",
                help="Specify regional dialect if applicable"
            )
            
            location = st.text_input(
                "Location (Optional)",
                placeholder="e.g., Punjab, India",
                help="Where is this story from?"
            )
            
            # AI assistance options
            st.markdown("### 🤖 AI Assistance")
            
            auto_translate = st.checkbox(
                "Auto-translate to English",
                value=True,
                help="AI will translate your story to English"
            )
            
            auto_categorize = st.checkbox(
                "Auto-categorize content",
                value=True,
                help="AI will suggest a category for your story"
            )
        
        # Translation preview section
        if auto_translate and content:
            with st.expander("🌐 Translation Preview", expanded=False):
                if st.button("Generate Translation"):
                    with st.spinner("Translating..."):
                        language_code = config.get_language_code(language)
                        translation = translation_service.translate_text(
                            content, 
                            source_lang=language_code,
                            target_lang="en"
                        )
                        if translation:
                            st.text_area(
                                "English Translation",
                                value=translation,
                                height=150,
                                key="translation_preview"
                            )
                            st.session_state.current_translation = translation
        
        # Categorization preview
        if auto_categorize and content:
            with st.expander("🏷️ Category Suggestion", expanded=False):
                if st.button("Suggest Category"):
                    with st.spinner("Analyzing content..."):
                        category = categorization_service.categorize_content(content, content_type)
                        if category:
                            st.success(f"Suggested category: **{category}**")
                            st.session_state.suggested_category = category
        
        # Submit button
        submitted = st.form_submit_button(
            "🚀 Submit Story",
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            handle_text_submission(
                title, content, cultural_context, content_type, language, dialect, location,
                auto_translate, auto_categorize, config, db_manager, 
                translation_service, categorization_service
            )

def show_voice_submission_form(config: Config, db_manager: DatabaseManager,
                              translation_service: TranslationService,
                              categorization_service: CategorizationService,
                              audio_processor: AudioProcessor):
    """Show voice-based submission form"""
    
    st.markdown("### 🎤 Record Your Story")
    st.info("Click the microphone to start recording. Speak clearly in your native language.")
    
    # Audio recording interface
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Placeholder for audio recorder component
        # This would be replaced with actual streamlit-mic-recorder component
        if st.button("🎤 Start Recording", type="primary", use_container_width=True):
            st.info("Recording functionality will be implemented with streamlit-mic-recorder")
            # audio_data = st_audiorec()
        
        # Audio playback placeholder
        if "recorded_audio" in st.session_state:
            st.audio(st.session_state.recorded_audio)
            
            if st.button("🔄 Re-record", use_container_width=True):
                del st.session_state.recorded_audio
                st.rerun()
    
    # Voice-to-text conversion
    if "recorded_audio" in st.session_state:
        st.markdown("### 📝 Transcription")
        
        col1, col2 = st.columns(2)
        
        with col1:
            transcription_language = st.selectbox(
                "Audio Language",
                options=list(config.LANGUAGES.values()),
                help="What language did you speak in?"
            )
        
        with col2:
            if st.button("🔤 Convert to Text"):
                with st.spinner("Converting speech to text..."):
                    # Transcribe audio
                    transcription = audio_processor.transcribe_audio(
                        st.session_state.recorded_audio,
                        language=config.get_language_code(transcription_language)
                    )
                    if transcription:
                        st.session_state.voice_transcription = transcription
        
        # Show transcription and allow editing
        if "voice_transcription" in st.session_state:
            with st.form("voice_submission_form"):
                st.markdown("### ✏️ Review and Edit")
                
                title = st.text_input(
                    "Title *",
                    placeholder="Enter a title for your story..."
                )
                
                content = st.text_area(
                    "Transcribed Content *",
                    value=st.session_state.voice_transcription,
                    height=200,
                    help="Review and edit the transcription if needed"
                )
                
                # Same metadata fields as text form
                col1, col2 = st.columns(2)
                
                with col1:
                    content_type = st.selectbox(
                        "Content Type *",
                        options=config.CONTENT_TYPES
                    )
                    
                    dialect = st.text_input(
                        "Dialect/Region (Optional)",
                        placeholder="e.g., Punjabi (Malwai)"
                    )
                
                with col2:
                    location = st.text_input(
                        "Location (Optional)",
                        placeholder="e.g., Punjab, India"
                    )
                    
                    cultural_context = st.text_area(
                        "Cultural Context (Optional)",
                        height=100
                    )
                
                # Submit voice recording
                voice_submitted = st.form_submit_button(
                    "🚀 Submit Voice Story",
                    type="primary",
                    use_container_width=True
                )
                
                if voice_submitted:
                    handle_voice_submission(
                        title, content, cultural_context, content_type, 
                        transcription_language, dialect, location,
                        config, db_manager, translation_service, categorization_service
                    )

def handle_text_submission(title: str, content: str, cultural_context: str,
                          content_type: str, language: str, dialect: str, location: str,
                          auto_translate: bool, auto_categorize: bool,
                          config: Config, db_manager: DatabaseManager,
                          translation_service: TranslationService,
                          categorization_service: CategorizationService):
    """Handle text submission processing"""
    
    # Validation
    if not title or not content or not content_type or not language:
        st.error("Please fill in all required fields (marked with *)")
        return
    
    with st.spinner("Processing your submission..."):
        try:
            # Prepare submission data
            submission_data = {
                "user_id": st.session_state.get("user_id", f"anon_{uuid.uuid4().hex[:8]}"),
                "title": title,
                "content": content,
                "content_type": content_type,
                "language": language,
                "dialect": dialect,
                "location": location,
                "cultural_context": cultural_context,
                "ai_translated": False,
                "ai_categorized": False
            }
            
            # Auto-translation
            if auto_translate:
                language_code = config.get_language_code(language)
                if language_code != "en":  # Don't translate if already in English
                    translation = translation_service.translate_text(
                        content, 
                        source_lang=language_code,
                        target_lang="en"
                    )
                    if translation:
                        submission_data["english_translation"] = translation
                        submission_data["ai_translated"] = True
                else:
                    submission_data["english_translation"] = content
            
            # Auto-categorization
            if auto_categorize:
                category = categorization_service.categorize_content(content, content_type)
                if category:
                    submission_data["category"] = category
                    submission_data["ai_categorized"] = True
            
            # Save to database
            submission_id = db_manager.save_submission(submission_data)
            
            if submission_id:
                st.success("🎉 Your story has been submitted successfully!")
                st.balloons()
                
                # Show submission summary
                with st.expander("📋 Submission Summary", expanded=True):
                    st.write(f"**Submission ID:** {submission_id}")
                    st.write(f"**Title:** {title}")
                    st.write(f"**Language:** {language}")
                    st.write(f"**Type:** {content_type}")
                    if submission_data.get("english_translation"):
                        st.write(f"**Translation:** {submission_data['english_translation'][:100]}...")
                    if submission_data.get("category"):
                        st.write(f"**Category:** {submission_data['category']}")
                
                # Update session state
                st.session_state.submissions_count += 1
                
                # Clear form
                if st.button("Submit Another Story"):
                    st.rerun()
            else:
                st.error("Failed to submit your story. Please try again.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def handle_voice_submission(title: str, content: str, cultural_context: str,
                           content_type: str, language: str, dialect: str, location: str,
                           config: Config, db_manager: DatabaseManager,
                           translation_service: TranslationService,
                           categorization_service: CategorizationService):
    """Handle voice submission processing"""
    
    # Similar to text submission but with audio metadata
    if not title or not content or not content_type or not language:
        st.error("Please fill in all required fields (marked with *)")
        return
    
    with st.spinner("Processing your voice submission..."):
        try:
            submission_data = {
                "user_id": st.session_state.get("user_id", f"anon_{uuid.uuid4().hex[:8]}"),
                "title": title,
                "content": content,
                "content_type": content_type,
                "language": language,
                "dialect": dialect,
                "location": location,
                "cultural_context": cultural_context,
                "audio_url": "voice_recording",  # Placeholder for actual audio storage
                "ai_translated": False,
                "ai_categorized": False
            }
            
            # Auto-translate and categorize
            language_code = config.get_language_code(language)
            if language_code != "en":
                translation = translation_service.translate_text(
                    content, source_lang=language_code, target_lang="en"
                )
                if translation:
                    submission_data["english_translation"] = translation
                    submission_data["ai_translated"] = True
            
            category = categorization_service.categorize_content(content, content_type)
            if category:
                submission_data["category"] = category
                submission_data["ai_categorized"] = True
            
            # Save submission
            submission_id = db_manager.save_submission(submission_data)
            
            if submission_id:
                st.success("🎉 Your voice story has been submitted successfully!")
                st.balloons()
                
                # Clear session state
                if "recorded_audio" in st.session_state:
                    del st.session_state.recorded_audio
                if "voice_transcription" in st.session_state:
                    del st.session_state.voice_transcription
                
                st.session_state.submissions_count += 1
            else:
                st.error("Failed to submit your story. Please try again.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
