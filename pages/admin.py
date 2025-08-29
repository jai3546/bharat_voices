"""
Admin dashboard for managing submissions and platform analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Any

from utils.config import Config
from utils.database import DatabaseManager

def show_admin_page():
    """Display the admin dashboard"""
    
    # Simple admin authentication
    if not check_admin_access():
        show_admin_login()
        return
    
    st.markdown("## 🛠️ Admin Dashboard")
    st.markdown("Manage submissions, users, and platform analytics")
    
    # Initialize services
    config = Config()
    db_manager = DatabaseManager()
    
    # Create tabs for different admin functions
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📝 Submissions", "👥 Users", "⚙️ Settings"])
    
    with tab1:
        show_admin_overview(config, db_manager)
    
    with tab2:
        show_submissions_management(config, db_manager)
    
    with tab3:
        show_users_management(config, db_manager)
    
    with tab4:
        show_admin_settings(config)

def check_admin_access() -> bool:
    """Check if user has admin access"""
    return st.session_state.get("admin_authenticated", False)

def show_admin_login():
    """Show admin login form"""
    st.markdown("## 🔐 Admin Access")
    
    with st.form("admin_login"):
        st.markdown("### Login to Admin Dashboard")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("🔑 Login"):
            # Simple authentication (in production, use proper auth)
            if username == "admin" and password == "bharatvoices2024":
                st.session_state.admin_authenticated = True
                st.success("✅ Admin access granted!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

def show_admin_overview(config: Config, db_manager: DatabaseManager):
    """Show admin overview with key metrics"""
    st.markdown("### 📊 Platform Overview")
    
    # Get analytics data
    analytics = db_manager.get_analytics_data()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_submissions = analytics.get("total_submissions", 1247)
        st.metric("Total Stories", total_submissions, "↗️ +23 today")
    
    with col2:
        total_users = analytics.get("total_users", 892)
        st.metric("Total Users", total_users, "↗️ +15 today")
    
    with col3:
        languages_count = analytics.get("languages_count", 47)
        st.metric("Languages", languages_count, "↗️ +2 this week")
    
    with col4:
        featured_count = len([s for s in analytics.get("recent_activity", []) if s.get("featured")])
        st.metric("Featured Stories", featured_count, "→ 0 today")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Submissions Over Time")
        # Mock data for demo
        dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
        submissions_data = pd.DataFrame({
            "Date": dates,
            "Submissions": [max(0, 5 + int(10 * (0.5 - abs(0.5 - (i % 100) / 100)))) for i in range(len(dates))]
        })
        
        fig = px.line(submissions_data, x="Date", y="Submissions", title="Daily Submissions")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🌍 Language Distribution")
        lang_dist = analytics.get("languages_distribution", {
            "Hindi": 234, "Bengali": 189, "English": 156, "Tamil": 134, "Telugu": 98,
            "Marathi": 87, "Gujarati": 76, "Kannada": 65, "Malayalam": 54, "Punjabi": 43
        })
        
        fig = px.pie(
            values=list(lang_dist.values())[:8],  # Top 8 languages
            names=list(lang_dist.keys())[:8],
            title="Top Languages"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Category distribution
    st.markdown("#### 🏷️ Category Distribution")
    cat_dist = analytics.get("categories_distribution", {
        "Wisdom & Life Lessons": 298,
        "Family & Community": 234,
        "Tradition & Culture": 189,
        "Love & Relationships": 156,
        "Nature & Environment": 134,
        "Spirituality & Faith": 123,
        "Work & Perseverance": 98,
        "Humor & Wit": 87,
        "Morality & Ethics": 76,
        "Courage & Heroism": 52
    })
    
    fig = px.bar(
        x=list(cat_dist.keys()),
        y=list(cat_dist.values()),
        title="Stories by Category"
    )
    fig.update_xaxis(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

def show_submissions_management(config: Config, db_manager: DatabaseManager):
    """Show submissions management interface"""
    st.markdown("### 📝 Submissions Management")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Status",
            options=["All", "Featured", "Pending Review", "Approved"]
        )
    
    with col2:
        language_filter = st.selectbox(
            "Language",
            options=["All"] + list(config.LANGUAGES.values())
        )
    
    with col3:
        date_filter = st.selectbox(
            "Date Range",
            options=["All Time", "Today", "This Week", "This Month"]
        )
    
    # Search
    search_query = st.text_input("🔍 Search submissions...", placeholder="Search by title, content, or user")
    
    # Get submissions
    submissions = get_admin_submissions(db_manager, status_filter, language_filter, date_filter, search_query)
    
    # Display submissions table
    if submissions:
        st.markdown(f"**Found {len(submissions)} submissions**")
        
        # Create DataFrame for display
        df = pd.DataFrame(submissions)
        
        # Select columns to display
        display_columns = ["title", "language", "category", "content_type", "likes", "featured", "timestamp"]
        available_columns = [col for col in display_columns if col in df.columns]
        
        if available_columns:
            display_df = df[available_columns].copy()
            
            # Format timestamp
            if "timestamp" in display_df.columns:
                display_df["timestamp"] = pd.to_datetime(display_df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M")
            
            # Display with selection
            selected_rows = st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                selection_mode="multi-row"
            )
            
            # Bulk actions
            if st.button("🌟 Feature Selected") and selected_rows:
                st.success(f"Featured {len(selected_rows)} submissions")
            
            if st.button("🗑️ Delete Selected") and selected_rows:
                if st.confirm("Are you sure you want to delete the selected submissions?"):
                    st.success(f"Deleted {len(selected_rows)} submissions")
    else:
        st.info("No submissions found matching your criteria.")

def show_users_management(config: Config, db_manager: DatabaseManager):
    """Show users management interface"""
    st.markdown("### 👥 Users Management")
    
    # User stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Users (30d)", "456", "↗️ +12%")
    
    with col2:
        st.metric("New Users (7d)", "89", "↗️ +23%")
    
    with col3:
        st.metric("Top Contributors", "25", "→ 0%")
    
    # User activity chart
    st.markdown("#### 📊 User Activity")
    
    # Mock user activity data
    activity_data = pd.DataFrame({
        "Date": pd.date_range(start="2024-11-01", end="2024-11-30", freq="D"),
        "New Users": [max(0, 3 + int(5 * (0.5 - abs(0.5 - (i % 20) / 20)))) for i in range(30)],
        "Active Users": [max(10, 25 + int(15 * (0.5 - abs(0.5 - (i % 15) / 15)))) for i in range(30)]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=activity_data["Date"], y=activity_data["New Users"], name="New Users", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=activity_data["Date"], y=activity_data["Active Users"], name="Active Users", line=dict(color="green")))
    fig.update_layout(title="User Activity Over Time", xaxis_title="Date", yaxis_title="Count")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top contributors
    st.markdown("#### 🏆 Top Contributors")
    
    contributors_data = [
        {"User": "Cultural Keeper", "Stories": 45, "Likes": 234, "Languages": 3},
        {"User": "Story Teller", "Stories": 38, "Likes": 198, "Languages": 2},
        {"User": "Wisdom Sharer", "Stories": 32, "Likes": 167, "Languages": 4},
        {"User": "Heritage Guardian", "Stories": 28, "Likes": 132, "Languages": 2},
        {"User": "Folk Narrator", "Stories": 25, "Likes": 145, "Languages": 3}
    ]
    
    contributors_df = pd.DataFrame(contributors_data)
    st.dataframe(contributors_df, use_container_width=True, hide_index=True)

def show_admin_settings(config: Config):
    """Show admin settings interface"""
    st.markdown("### ⚙️ Platform Settings")
    
    # Feature toggles
    st.markdown("#### 🎛️ Feature Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_translation = st.checkbox("Auto Translation", value=True)
        auto_categorization = st.checkbox("Auto Categorization", value=True)
        voice_input = st.checkbox("Voice Input", value=True)
        social_sharing = st.checkbox("Social Sharing", value=True)
    
    with col2:
        user_registration = st.checkbox("User Registration", value=False)
        content_moderation = st.checkbox("Content Moderation", value=True)
        featured_stories = st.checkbox("Featured Stories", value=True)
        analytics_tracking = st.checkbox("Analytics Tracking", value=True)
    
    # Content settings
    st.markdown("#### 📝 Content Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_content_length = st.number_input("Max Content Length", value=2000, min_value=100, max_value=5000)
        max_title_length = st.number_input("Max Title Length", value=200, min_value=50, max_value=500)
    
    with col2:
        daily_submission_limit = st.number_input("Daily Submission Limit", value=10, min_value=1, max_value=100)
        auto_feature_threshold = st.number_input("Auto Feature Threshold (likes)", value=50, min_value=10, max_value=200)
    
    # Collection targets
    st.markdown("#### 🎯 Collection Targets")
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_target = st.number_input("Total Collection Target", value=1000, min_value=100, max_value=10000)
        daily_target = st.number_input("Daily Target", value=10, min_value=1, max_value=100)
    
    with col2:
        language_target = st.number_input("Language Target", value=50, min_value=10, max_value=100)
        user_target = st.number_input("User Target", value=1000, min_value=100, max_value=10000)
    
    # Save settings
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Settings saved successfully!")
    
    # Export data
    st.markdown("#### 📤 Data Export")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Analytics"):
            st.success("Analytics data exported!")
    
    with col2:
        if st.button("📝 Export Submissions"):
            st.success("Submissions data exported!")
    
    with col3:
        if st.button("👥 Export Users"):
            st.success("User data exported!")

def get_admin_submissions(db_manager: DatabaseManager, status_filter: str, 
                         language_filter: str, date_filter: str, search_query: str) -> List[Dict[str, Any]]:
    """Get submissions for admin view with filters"""
    
    # Mock data for demo
    mock_submissions = [
        {
            "id": "sub_1",
            "title": "The Wise Tree",
            "content": "A tree that gives shade cannot complain about the sun.",
            "language": "English",
            "category": "Wisdom & Life Lessons",
            "content_type": "Proverb",
            "likes": 47,
            "featured": True,
            "timestamp": "2024-11-26 10:30:00",
            "user_id": "user_123"
        },
        {
            "id": "sub_2",
            "title": "Unity in Diversity",
            "content": "जैसे नदियाँ समुद्र में मिलकर एक हो जाती हैं।",
            "language": "Hindi",
            "category": "Family & Community",
            "content_type": "Saying",
            "likes": 32,
            "featured": False,
            "timestamp": "2024-11-26 09:15:00",
            "user_id": "user_456"
        },
        {
            "id": "sub_3",
            "title": "Mother's Love",
            "content": "মায়ের ভালোবাসা সমুদ্রের মতো গভীর।",
            "language": "Bengali",
            "category": "Family & Community",
            "content_type": "Saying",
            "likes": 28,
            "featured": False,
            "timestamp": "2024-11-26 08:45:00",
            "user_id": "user_789"
        }
    ]
    
    # Apply filters (simplified for demo)
    filtered_submissions = mock_submissions
    
    if status_filter == "Featured":
        filtered_submissions = [s for s in filtered_submissions if s.get("featured")]
    elif status_filter == "Pending Review":
        filtered_submissions = [s for s in filtered_submissions if not s.get("featured") and s.get("likes", 0) < 10]
    
    if language_filter != "All":
        filtered_submissions = [s for s in filtered_submissions if s.get("language") == language_filter]
    
    if search_query:
        search_lower = search_query.lower()
        filtered_submissions = [
            s for s in filtered_submissions 
            if search_lower in s.get("title", "").lower() or search_lower in s.get("content", "").lower()
        ]
    
    return filtered_submissions
