"""
Bharat Voices - Cultural Storytelling Platform
A lightweight, multilingual Streamlit application for collecting and sharing cultural stories.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Import custom modules
try:
    from utils.config import Config
    from utils.database import DatabaseManager
    from utils.translation import TranslationService
    from utils.categorization import CategorizationService
    from utils.audio import AudioProcessor
    from utils.gamification import GamificationManager
    from utils.social_cards import SocialCardGenerator
    from pages import submission, community, admin, profile, analytics
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Please ensure all required modules are installed. Run: pip install -r requirements.txt")

# Page configuration
st.set_page_config(
    page_title="Bharat Voices - Cultural Storytelling Platform",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/bharat-voices',
        'Report a bug': 'https://github.com/your-repo/bharat-voices/issues',
        'About': """
        # Bharat Voices
        A cultural storytelling platform that preserves and shares wisdom from around the world.
        
        **Features:**
        - Submit stories in your native language
        - Voice-to-text recording
        - AI translation and categorization
        - Community engagement
        - Gamification and badges
        - Social media sharing
        """
    }
)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'submissions_count' not in st.session_state:
        st.session_state.submissions_count = 0
    if 'user_badges' not in st.session_state:
        st.session_state.user_badges = []
    if 'current_streak' not in st.session_state:
        st.session_state.current_streak = 0
    if 'offline_drafts' not in st.session_state:
        st.session_state.offline_drafts = []
    if 'language_preference' not in st.session_state:
        st.session_state.language_preference = 'English'

# Custom CSS for styling
def load_custom_css():
    """Load custom CSS for better UI"""
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .stats-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .submission-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        background: #667eea;
        color: white;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
    
    .progress-container {
        background: #e9ecef;
        border-radius: 10px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .featured-story {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #fdcb6e;
    }
    
    .community-stats {
        display: flex;
        justify-content: space-around;
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .language-tag {
        background: #17a2b8;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
    }
    
    .category-tag {
        background: #28a745;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize session state
    init_session_state()
    
    # Load custom CSS
    load_custom_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🗣️ Bharat Voices</h1>
        <p>Preserving Cultural Wisdom Through Stories</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/667eea/ffffff?text=Bharat+Voices", width=200)
        
        selected = option_menu(
            menu_title="Navigation",
            options=["Home", "Submit Story", "Community", "Analytics", "Admin", "Profile"],
            icons=["house", "plus-circle", "people", "bar-chart", "gear", "person"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#667eea"},
            }
        )
        
        # Progress tracker
        st.markdown("### 📊 Collection Progress")
        total_target = 1000
        current_count = st.session_state.submissions_count
        progress = min(current_count / total_target, 1.0)
        
        st.progress(progress)
        st.write(f"**{current_count}/{total_target}** stories collected")
        
        # User stats (if user exists)
        if st.session_state.user_id:
            st.markdown("### 🏆 Your Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Stories", len(st.session_state.offline_drafts))
            with col2:
                st.metric("Streak", st.session_state.current_streak)
    
    # Route to different pages based on selection
    try:
        if selected == "Home":
            show_home_page()
        elif selected == "Submit Story":
            submission.show_submission_page()
        elif selected == "Community":
            community.show_community_page()
        elif selected == "Analytics":
            analytics.show_analytics_page()
        elif selected == "Admin":
            admin.show_admin_page()
        elif selected == "Profile":
            profile.show_profile_page()
    except Exception as e:
        st.error(f"Error loading page: {e}")
        st.info("Please check that all required dependencies are installed.")

def show_home_page():
    """Display the home page"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## Welcome to Bharat Voices! 🌍")
        st.markdown("""
        **Bharat Voices** is a platform where cultural wisdom comes alive. Share your local proverbs, 
        folk tales, sayings, and stories in your native language. Help preserve the rich tapestry 
        of human wisdom for future generations.
        
        ### ✨ Features:
        - 🎤 **Voice Recording**: Record your stories directly
        - 🌐 **Auto Translation**: AI translates to English
        - 🏷️ **Smart Categorization**: AI organizes by themes
        - 👥 **Community Engagement**: Like, share, and discover
        - 🏆 **Gamification**: Earn badges and climb leaderboards
        - 📱 **Social Sharing**: Create beautiful story cards
        """)
        
        # Quick stats
        st.markdown("### 📈 Platform Statistics")
        col1_stats, col2_stats, col3_stats, col4_stats = st.columns(4)
        
        with col1_stats:
            st.metric("Total Stories", "1,247", "↗️ 23")
        with col2_stats:
            st.metric("Languages", "47", "↗️ 2")
        with col3_stats:
            st.metric("Contributors", "892", "↗️ 15")
        with col4_stats:
            st.metric("Countries", "23", "↗️ 1")
    
    with col2:
        st.markdown("### 🌟 Featured Story of the Day")
        st.markdown("""
        <div class="featured-story">
            <h4>🌱 "A tree that falls in the forest..."</h4>
            <p><em>"जो पेड़ जंगल में गिरता है, वह अकेला नहीं गिरता।"</em></p>
            <p><strong>Translation:</strong> "A tree that falls in the forest does not fall alone."</p>
            <p><strong>Meaning:</strong> Every action affects the community around us.</p>
            <div style="margin-top: 1rem;">
                <span class="language-tag">Hindi</span>
                <span class="category-tag">Wisdom</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Recent activity
        st.markdown("### 📝 Recent Activity")
        recent_activities = [
            "🇮🇳 New Hindi proverb added",
            "🇧🇩 Bengali folk tale shared",
            "🇳🇵 Nepali saying translated",
            "🇱🇰 Tamil story featured",
            "🇵🇰 Urdu poem categorized"
        ]
        
        for activity in recent_activities:
            st.markdown(f"• {activity}")

if __name__ == "__main__":
    main()
