from dataclasses import dataclass, field
from typing import List, Dict, Any
import os

@dataclass
class Config:
    APP_NAME: str = "Bharat Voices"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database
    GOOGLE_SHEETS_URL: str = os.getenv("GOOGLE_SHEETS_URL", "")
    GOOGLE_CREDENTIALS_PATH: str = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
    AIRTABLE_API_KEY: str = os.getenv("AIRTABLE_API_KEY", "")
    AIRTABLE_BASE_ID: str = os.getenv("AIRTABLE_BASE_ID", "")

    # AI
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Translation
    TRANSLATION_MODEL: str = "Helsinki-NLP/opus-mt-mul-en"
    CATEGORIZATION_MODEL: str = "facebook/bart-large-mnli"

    # Audio
    WHISPER_MODEL: str = "base"
    MAX_AUDIO_DURATION: int = 300
    AUDIO_SAMPLE_RATE: int = 16000

    # Gamification
    BADGES: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "first_story": {"name": "First Steps", "description": "Submitted your first story", "icon": "🌱", "requirement": 1},
        "cultural_preserver": {"name": "Cultural Preserver", "description": "Submitted 10 stories", "icon": "🏛️", "requirement": 10},
        "story_weaver": {"name": "Story Weaver", "description": "Submitted 25 stories", "icon": "🧵", "requirement": 25},
        "wisdom_keeper": {"name": "Wisdom Keeper", "description": "Submitted 50 stories", "icon": "📚", "requirement": 50},
        "multilingual": {"name": "Multilingual Master", "description": "Submitted stories in 3+ languages", "icon": "🌍", "requirement": 3},
        "community_favorite": {"name": "Community Favorite", "description": "Received 100+ likes", "icon": "❤️", "requirement": 100},
        "streak_master": {"name": "Streak Master", "description": "7-day submission streak", "icon": "🔥", "requirement": 7}
    })

    # Content
    CATEGORIES: List[str] = field(default_factory=lambda: [
        "Wisdom & Life Lessons", "Love & Relationships", "Family & Community",
        "Nature & Environment", "Courage & Heroism", "Morality & Ethics",
        "Spirituality & Faith", "Work & Perseverance", "Humor & Wit",
        "Tradition & Culture", "Children's Tales", "Historical Stories"
    ])
    CONTENT_TYPES: List[str] = field(default_factory=lambda: [
        "Proverb", "Folk Tale", "Saying", "Short Story",
        "Poem", "Song", "Riddle", "Legend"
    ])
    LANGUAGES: Dict[str, str] = field(default_factory=lambda: {"en": "English"})  # Simplified example

    # Progress tracking (add these!)
    COLLECTION_TARGET: int = 1000
    DAILY_TARGET: int = 10
