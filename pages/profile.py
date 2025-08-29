"""
User profile page for tracking personal contributions and achievements
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Any

from utils.config import Config
from utils.database import DatabaseManager
from utils.gamification import GamificationManager

def show_profile_page():
    """Display user profile page"""
    st.markdown("## 👤 Your Profile")
    
    # Initialize services
    config = Config()
    db_manager = DatabaseManager()
    gamification = GamificationManager()
    
    # Get or create user ID
    user_id = get_or_create_user_id()
    
    # Create tabs for different profile sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📝 My Stories", "🏆 Achievements", "⚙️ Settings"])
    
    with tab1:
        show_profile_overview(user_id, config, db_manager, gamification)
    
    with tab2:
        show_user_stories(user_id, config, db_manager)
    
    with tab3:
        show_user_achievements(user_id, config, gamification)
    
    with tab4:
        show_profile_settings(user_id, config)

def get_or_create_user_id() -> str:
    """Get existing user ID or create anonymous one"""
    if "user_id" not in st.session_state:
        # Create anonymous user ID
        import uuid
        st.session_state.user_id = f"anon_{uuid.uuid4().hex[:8]}"
    
    return st.session_state.user_id

def show_profile_overview(user_id: str, config: Config, db_manager: DatabaseManager, gamification: GamificationManager):
    """Show profile overview with stats and recent activity"""
    
    # User info section
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Profile picture placeholder
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 50%; width: 150px; height: 150px; margin: auto;">
            <div style="font-size: 4rem; margin-top: 1rem;">👤</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display name
        display_name = st.session_state.get("display_name", "Cultural Contributor")
        st.markdown(f"### {display_name}")
        
        # User since
        join_date = st.session_state.get("join_date", datetime.now().strftime("%B %Y"))
        st.markdown(f"**Member since:** {join_date}")
    
    with col2:
        # User statistics
        user_stats = db_manager.get_user_stats(user_id)
        
        col2_1, col2_2, col2_3 = st.columns(3)
        
        with col2_1:
            total_stories = user_stats.get("total_submissions", 0)
            st.metric("Stories Shared", total_stories, "📝")
        
        with col2_2:
            total_likes = user_stats.get("total_likes", 0)
            st.metric("Likes Received", total_likes, "❤️")
        
        with col2_3:
            current_streak = gamification.calculate_user_streak(user_id)
            st.metric("Current Streak", f"{current_streak} days", "🔥")
        
        # Additional stats
        col2_4, col2_5, col2_6 = st.columns(3)
        
        with col2_4:
            languages_used = len(user_stats.get("languages_used", []))
            st.metric("Languages Used", languages_used, "🌍")
        
        with col2_5:
            categories_used = len(user_stats.get("categories_used", []))
            st.metric("Categories", categories_used, "🏷️")
        
        with col2_6:
            badges_earned = len(user_stats.get("badges", []))
            st.metric("Badges Earned", badges_earned, "🏆")
    
    # Progress towards collection goal
    st.markdown("### 🎯 Your Contribution Progress")
    
    collection_target = config.COLLECTION_TARGET
    platform_total = 1247  # Mock platform total
    user_contribution = total_stories
    
    if platform_total > 0:
        user_percentage = (user_contribution / platform_total) * 100
        st.markdown(f"You've contributed **{user_percentage:.1f}%** of all stories on the platform!")
    
    progress_col1, progress_col2 = st.columns(2)
    
    with progress_col1:
        # Personal milestone progress
        milestones = [1, 5, 10, 25, 50, 100]
        next_milestone = next((m for m in milestones if m > user_contribution), 100)
        
        if next_milestone:
            milestone_progress = user_contribution / next_milestone
            st.progress(milestone_progress)
            st.caption(f"Progress to {next_milestone} stories: {user_contribution}/{next_milestone}")
    
    with progress_col2:
        # Platform contribution
        platform_progress = platform_total / collection_target
        st.progress(min(platform_progress, 1.0))
        st.caption(f"Platform progress: {platform_total}/{collection_target} stories")
    
    # Recent activity
    st.markdown("### 📈 Your Recent Activity")
    
    # Mock activity data
    activity_data = get_user_activity_data(user_id)
    
    if activity_data:
        # Activity chart
        df = pd.DataFrame(activity_data)
        fig = px.line(df, x="date", y="submissions", title="Your Daily Submissions (Last 30 Days)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Start sharing stories to see your activity here!")

def show_user_stories(user_id: str, config: Config, db_manager: DatabaseManager):
    """Show user's submitted stories"""
    st.markdown("### 📝 Your Stories")
    
    # Get user's stories
    user_stories = db_manager.get_submissions(filters={"user_id": user_id})
    
    if not user_stories:
        # Show mock stories for demo
        user_stories = get_mock_user_stories()
    
    if user_stories:
        # Filters and sorting
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sort_by = st.selectbox("Sort by", ["Recent", "Most Liked", "Title"])
        
        with col2:
            filter_language = st.selectbox(
                "Filter by Language",
                ["All"] + list(set(story.get("language", "") for story in user_stories))
            )
        
        with col3:
            filter_category = st.selectbox(
                "Filter by Category",
                ["All"] + list(set(story.get("category", "") for story in user_stories))
            )
        
        # Apply filters
        filtered_stories = user_stories
        if filter_language != "All":
            filtered_stories = [s for s in filtered_stories if s.get("language") == filter_language]
        if filter_category != "All":
            filtered_stories = [s for s in filtered_stories if s.get("category") == filter_category]
        
        # Sort stories
        if sort_by == "Most Liked":
            filtered_stories.sort(key=lambda x: x.get("likes", 0), reverse=True)
        elif sort_by == "Title":
            filtered_stories.sort(key=lambda x: x.get("title", ""))
        else:  # Recent
            filtered_stories.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        # Display stories
        for story in filtered_stories:
            display_user_story_card(story)
    else:
        st.info("You haven't shared any stories yet. Start by visiting the Submit Story page!")
        if st.button("📝 Share Your First Story"):
            st.switch_page("pages/submission.py")

def show_user_achievements(user_id: str, config: Config, gamification: GamificationManager):
    """Show user achievements and progress"""
    st.markdown("### 🏆 Your Achievements")
    
    # Get user badges
    user_badges = gamification.get_user_badges(user_id)
    
    # Display earned badges
    if user_badges:
        gamification.display_badge_showcase(user_badges)
    else:
        st.info("🏅 No badges earned yet. Keep sharing stories to unlock achievements!")
    
    # Achievement progress
    st.markdown("### 📈 Achievement Progress")
    progress = gamification.get_achievement_progress(user_id)
    gamification.display_progress_bars(progress)
    
    # Leaderboard position
    st.markdown("### 🏅 Your Rankings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        submissions_rank = gamification.get_user_rank(user_id, "submissions")
        st.markdown("#### 📝 Stories Leaderboard")
        if submissions_rank["rank"] != "Not ranked":
            st.success(f"🏆 Rank #{submissions_rank['rank']} with {submissions_rank['value']} stories")
        else:
            st.info("Not yet ranked. Share more stories to appear on the leaderboard!")
    
    with col2:
        likes_rank = gamification.get_user_rank(user_id, "likes")
        st.markdown("#### ❤️ Likes Leaderboard")
        if likes_rank["rank"] != "Not ranked":
            st.success(f"🏆 Rank #{likes_rank['rank']} with {likes_rank['value']} likes")
        else:
            st.info("Not yet ranked. Create engaging content to get more likes!")
    
    # Daily challenge
    st.markdown("### 🎯 Today's Challenge")
    daily_challenge = gamification.get_daily_challenge()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; margin: 1rem 0;">
        <h4 style="margin: 0; color: white;">{daily_challenge['icon']} {daily_challenge['title']}</h4>
        <p style="margin: 0.5rem 0; color: white;">{daily_challenge['description']}</p>
        <p style="margin: 0; font-weight: bold; color: white;">Reward: {daily_challenge['reward']}</p>
    </div>
    """, unsafe_allow_html=True)

def show_profile_settings(user_id: str, config: Config):
    """Show profile settings"""
    st.markdown("### ⚙️ Profile Settings")
    
    # Personal information
    st.markdown("#### 👤 Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        display_name = st.text_input(
            "Display Name",
            value=st.session_state.get("display_name", "Cultural Contributor")
        )
        
        native_language = st.selectbox(
            "Native Language",
            options=list(config.LANGUAGES.values()),
            index=list(config.LANGUAGES.values()).index(st.session_state.get("native_language", "English"))
        )
    
    with col2:
        location = st.text_input(
            "Location (Optional)",
            value=st.session_state.get("location", "")
        )
        
        bio = st.text_area(
            "Bio (Optional)",
            value=st.session_state.get("bio", ""),
            height=100
        )
    
    # Preferences
    st.markdown("#### 🎛️ Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_translate = st.checkbox(
            "Auto-translate my stories",
            value=st.session_state.get("auto_translate", True)
        )
        
        auto_categorize = st.checkbox(
            "Auto-categorize my stories",
            value=st.session_state.get("auto_categorize", True)
        )
    
    with col2:
        email_notifications = st.checkbox(
            "Email notifications",
            value=st.session_state.get("email_notifications", False)
        )
        
        public_profile = st.checkbox(
            "Make profile public",
            value=st.session_state.get("public_profile", True)
        )
    
    # Privacy settings
    st.markdown("#### 🔒 Privacy Settings")
    
    show_real_name = st.checkbox(
        "Show real name on stories",
        value=st.session_state.get("show_real_name", False)
    )
    
    show_location = st.checkbox(
        "Show location on stories",
        value=st.session_state.get("show_location", True)
    )
    
    allow_story_sharing = st.checkbox(
        "Allow others to share my stories",
        value=st.session_state.get("allow_story_sharing", True)
    )
    
    # Save settings
    if st.button("💾 Save Settings", type="primary"):
        # Update session state
        st.session_state.display_name = display_name
        st.session_state.native_language = native_language
        st.session_state.location = location
        st.session_state.bio = bio
        st.session_state.auto_translate = auto_translate
        st.session_state.auto_categorize = auto_categorize
        st.session_state.email_notifications = email_notifications
        st.session_state.public_profile = public_profile
        st.session_state.show_real_name = show_real_name
        st.session_state.show_location = show_location
        st.session_state.allow_story_sharing = allow_story_sharing
        
        st.success("✅ Settings saved successfully!")
    
    # Data export
    st.markdown("#### 📤 Data Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export My Data"):
            st.success("Your data export has been prepared!")
    
    with col2:
        if st.button("🗑️ Delete Account"):
            if st.confirm("Are you sure you want to delete your account? This action cannot be undone."):
                st.error("Account deletion requested. Please contact support.")

def display_user_story_card(story: Dict[str, Any]):
    """Display a story card in user's profile"""
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"### {story.get('title', 'Untitled')}")
        
        with col2:
            likes = story.get("likes", 0)
            st.markdown(f"❤️ {likes} likes")
        
        with col3:
            if story.get("featured"):
                st.markdown("⭐ **Featured**")
        
        # Content preview
        content = story.get("content", "")
        if len(content) > 200:
            content = content[:197] + "..."
        st.markdown(f"*{content}*")
        
        # Metadata
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Language:** {story.get('language', 'Unknown')}")
        
        with col2:
            st.markdown(f"**Category:** {story.get('category', 'Uncategorized')}")
        
        with col3:
            timestamp = story.get("timestamp", "")
            if timestamp:
                try:
                    date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_date = date.strftime("%b %d, %Y")
                    st.markdown(f"**Date:** {formatted_date}")
                except:
                    st.markdown(f"**Date:** {timestamp[:10]}")
        
        st.markdown("---")

def get_user_activity_data(user_id: str) -> List[Dict[str, Any]]:
    """Get user activity data for the last 30 days"""
    # Mock activity data
    activity = []
    for i in range(30):
        date = datetime.now() - timedelta(days=29-i)
        submissions = max(0, int(2 * (0.5 - abs(0.5 - (i % 10) / 10))))
        activity.append({
            "date": date.strftime("%Y-%m-%d"),
            "submissions": submissions
        })
    
    return activity

def get_mock_user_stories() -> List[Dict[str, Any]]:
    """Get mock user stories for demo"""
    return [
        {
            "id": "user_story_1",
            "title": "The Patient Farmer",
            "content": "A farmer who plants today eats tomorrow. Patience is the seed of prosperity.",
            "content_type": "Proverb",
            "language": "English",
            "category": "Work & Perseverance",
            "likes": 15,
            "featured": False,
            "timestamp": (datetime.now() - timedelta(days=2)).isoformat()
        },
        {
            "id": "user_story_2",
            "title": "Grandmother's Wisdom",
            "content": "My grandmother always said: 'The tree that bends in the storm survives, while the rigid one breaks.'",
            "content_type": "Folk Tale",
            "language": "English",
            "category": "Wisdom & Life Lessons",
            "likes": 23,
            "featured": True,
            "timestamp": (datetime.now() - timedelta(days=5)).isoformat()
        }
    ]
