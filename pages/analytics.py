"""
Analytics dashboard for platform insights and corpus statistics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Any

from utils.config import Config
from utils.database import DatabaseManager

def show_analytics_page():
    """Display the analytics dashboard"""
    st.markdown("## 📊 Platform Analytics")
    st.markdown("Insights into our growing cultural corpus and community engagement")
    
    # Initialize services
    config = Config()
    db_manager = DatabaseManager()
    
    # Create tabs for different analytics views
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🌍 Languages", "🏷️ Categories", "👥 Community"])
    
    with tab1:
        show_overview_analytics(config, db_manager)
    
    with tab2:
        show_language_analytics(config, db_manager)
    
    with tab3:
        show_category_analytics(config, db_manager)
    
    with tab4:
        show_community_analytics(config, db_manager)

def show_overview_analytics(config: Config, db_manager: DatabaseManager):
    """Show overview analytics"""
    st.markdown("### 📊 Platform Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Stories", "1,247", "↗️ +23 today")
    
    with col2:
        st.metric("Active Languages", "47", "↗️ +2 this week")
    
    with col3:
        st.metric("Contributors", "892", "↗️ +15 today")
    
    with col4:
        st.metric("Countries", "23", "↗️ +1 this month")
    
    # Progress towards collection goal
    st.markdown("### 🎯 Collection Progress")
    
    current_count = 1247
    target_count = config.COLLECTION_TARGET
    progress_percentage = (current_count / target_count) * 100
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Progress bar
        st.progress(min(progress_percentage / 100, 1.0))
        st.markdown(f"**{current_count:,} / {target_count:,} stories** ({progress_percentage:.1f}% complete)")
        
        # Estimated completion
        daily_average = 23  # Mock daily average
        days_remaining = max(0, (target_count - current_count) / daily_average)
        completion_date = datetime.now() + timedelta(days=days_remaining)
        
        st.info(f"📅 Estimated completion: {completion_date.strftime('%B %d, %Y')} ({int(days_remaining)} days)")
    
    with col2:
        # Collection speed gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = daily_average,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Daily Average"},
            gauge = {
                'axis': {'range': [None, 50]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 10], 'color': "lightgray"},
                    {'range': [10, 25], 'color': "gray"},
                    {'range': [25, 50], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 30
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Growth trends
    st.markdown("### 📈 Growth Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Submissions over time
        dates = pd.date_range(start="2024-01-01", end="2024-11-26", freq="D")
        submissions_data = pd.DataFrame({
            "Date": dates,
            "Daily Submissions": [max(0, 15 + int(10 * (0.5 - abs(0.5 - (i % 30) / 30)))) for i in range(len(dates))],
            "Cumulative": range(100, 100 + len(dates) * 4, 4)
        })
        
        fig = px.line(submissions_data, x="Date", y="Daily Submissions", 
                     title="Daily Submissions Over Time")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # User growth
        user_data = pd.DataFrame({
            "Date": dates,
            "New Users": [max(0, 5 + int(8 * (0.5 - abs(0.5 - (i % 20) / 20)))) for i in range(len(dates))],
            "Total Users": range(50, 50 + len(dates) * 3, 3)
        })
        
        fig = px.line(user_data, x="Date", y="New Users", 
                     title="New Users Over Time")
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent milestones
    st.markdown("### 🏆 Recent Milestones")
    
    milestones = [
        {"date": "Nov 25, 2024", "milestone": "🎉 Reached 1,200 stories!", "type": "success"},
        {"date": "Nov 20, 2024", "milestone": "🌍 Added support for Sinhala language", "type": "info"},
        {"date": "Nov 15, 2024", "milestone": "👥 Welcomed our 800th contributor", "type": "success"},
        {"date": "Nov 10, 2024", "milestone": "🏷️ Introduced new category: Historical Stories", "type": "info"},
        {"date": "Nov 5, 2024", "milestone": "🔥 Highest daily submissions: 45 stories", "type": "warning"}
    ]
    
    for milestone in milestones:
        if milestone["type"] == "success":
            st.success(f"**{milestone['date']}** - {milestone['milestone']}")
        elif milestone["type"] == "info":
            st.info(f"**{milestone['date']}** - {milestone['milestone']}")
        else:
            st.warning(f"**{milestone['date']}** - {milestone['milestone']}")

def show_language_analytics(config: Config, db_manager: DatabaseManager):
    """Show language-specific analytics"""
    st.markdown("### 🌍 Language Analytics")
    
    # Language distribution
    language_data = {
        "Hindi": 234, "Bengali": 189, "English": 156, "Tamil": 134, "Telugu": 98,
        "Marathi": 87, "Gujarati": 76, "Kannada": 65, "Malayalam": 54, "Punjabi": 43,
        "Urdu": 38, "Odia": 32, "Assamese": 28, "Nepali": 25, "Sinhala": 22
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top languages pie chart
        top_languages = dict(list(language_data.items())[:8])
        others_count = sum(list(language_data.values())[8:])
        if others_count > 0:
            top_languages["Others"] = others_count
        
        fig = px.pie(
            values=list(top_languages.values()),
            names=list(top_languages.keys()),
            title="Language Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Language growth over time
        lang_growth_data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],
            "Hindi": [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70],
            "Bengali": [15, 20, 25, 28, 32, 35, 38, 42, 45, 48, 52],
            "English": [25, 28, 32, 35, 38, 40, 42, 45, 48, 50, 52],
            "Tamil": [10, 15, 18, 22, 25, 28, 30, 33, 36, 38, 40]
        })
        
        fig = px.line(lang_growth_data, x="Month", y=["Hindi", "Bengali", "English", "Tamil"],
                     title="Top Languages Growth")
        st.plotly_chart(fig, use_container_width=True)
    
    # Language statistics table
    st.markdown("### 📊 Detailed Language Statistics")
    
    lang_stats = []
    for lang, count in language_data.items():
        avg_likes = max(5, int(count * 0.3 + (hash(lang) % 10)))
        featured_count = max(1, count // 20)
        lang_stats.append({
            "Language": lang,
            "Stories": count,
            "Avg Likes": avg_likes,
            "Featured": featured_count,
            "% of Total": f"{(count / sum(language_data.values())) * 100:.1f}%"
        })
    
    df = pd.DataFrame(lang_stats)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Language diversity metrics
    st.markdown("### 🌐 Diversity Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_languages = len(language_data)
        st.metric("Active Languages", total_languages)
    
    with col2:
        # Calculate language diversity index (simplified Shannon diversity)
        total_stories = sum(language_data.values())
        diversity_index = -sum((count/total_stories) * (count/total_stories) for count in language_data.values())
        st.metric("Diversity Index", f"{diversity_index:.2f}")
    
    with col3:
        # Languages with recent activity
        recent_languages = 12  # Mock number
        st.metric("Recently Active", recent_languages)

def show_category_analytics(config: Config, db_manager: DatabaseManager):
    """Show category-specific analytics"""
    st.markdown("### 🏷️ Category Analytics")
    
    # Category distribution
    category_data = {
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
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Category bar chart
        fig = px.bar(
            x=list(category_data.keys()),
            y=list(category_data.values()),
            title="Stories by Category"
        )
        fig.update_xaxis(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Category engagement (likes per story)
        engagement_data = {cat: max(10, count // 5 + (hash(cat) % 15)) 
                          for cat, count in category_data.items()}
        
        fig = px.bar(
            x=list(engagement_data.keys()),
            y=list(engagement_data.values()),
            title="Average Likes per Category"
        )
        fig.update_xaxis(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Category trends
    st.markdown("### 📈 Category Trends")
    
    # Mock trend data
    months = ["Sep", "Oct", "Nov"]
    trend_data = pd.DataFrame({
        "Month": months,
        "Wisdom & Life Lessons": [85, 92, 98],
        "Family & Community": [70, 78, 82],
        "Tradition & Culture": [60, 65, 72],
        "Love & Relationships": [45, 52, 58]
    })
    
    fig = px.line(trend_data, x="Month", 
                 y=["Wisdom & Life Lessons", "Family & Community", "Tradition & Culture", "Love & Relationships"],
                 title="Category Growth Trends (Last 3 Months)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Category insights
    st.markdown("### 💡 Category Insights")
    
    insights = [
        "📈 **Wisdom & Life Lessons** is the most popular category, representing 24% of all stories",
        "❤️ **Love & Relationships** stories receive the highest average likes (18.5 per story)",
        "🔥 **Humor & Wit** is the fastest-growing category this month (+15%)",
        "🌍 **Nature & Environment** stories are most popular in rural areas",
        "📚 **Tradition & Culture** has the highest translation rate (95%)"
    ]
    
    for insight in insights:
        st.markdown(insight)

def show_community_analytics(config: Config, db_manager: DatabaseManager):
    """Show community engagement analytics"""
    st.markdown("### 👥 Community Analytics")
    
    # Engagement metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Likes", "12,456", "↗️ +234 today")
    
    with col2:
        st.metric("Avg Likes/Story", "9.8", "↗️ +0.3")
    
    with col3:
        st.metric("Featured Stories", "47", "→ 0 today")
    
    with col4:
        st.metric("Sharing Rate", "23%", "↗️ +2%")
    
    # User engagement patterns
    st.markdown("### 📊 User Engagement Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily activity pattern
        hours = list(range(24))
        activity = [2, 1, 1, 1, 2, 3, 5, 8, 12, 15, 18, 20, 22, 25, 23, 20, 18, 16, 14, 12, 8, 6, 4, 3]
        
        fig = px.bar(x=hours, y=activity, title="Activity by Hour of Day")
        fig.update_xaxis(title="Hour")
        fig.update_yaxis(title="Stories Submitted")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Weekly pattern
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekly_activity = [85, 92, 88, 95, 78, 65, 72]
        
        fig = px.bar(x=days, y=weekly_activity, title="Activity by Day of Week")
        fig.update_yaxis(title="Stories Submitted")
        st.plotly_chart(fig, use_container_width=True)
    
    # Top contributors
    st.markdown("### 🏆 Top Contributors")
    
    contributors = [
        {"Rank": 1, "User": "Cultural Keeper", "Stories": 45, "Likes": 234, "Languages": 3},
        {"Rank": 2, "User": "Story Teller", "Stories": 38, "Likes": 198, "Languages": 2},
        {"Rank": 3, "User": "Wisdom Sharer", "Stories": 32, "Likes": 167, "Languages": 4},
        {"Rank": 4, "User": "Heritage Guardian", "Stories": 28, "Likes": 132, "Languages": 2},
        {"Rank": 5, "User": "Folk Narrator", "Stories": 25, "Likes": 145, "Languages": 3}
    ]
    
    df = pd.DataFrame(contributors)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Geographic distribution
    st.markdown("### 🌍 Geographic Distribution")
    
    # Mock geographic data
    countries = ["India", "Bangladesh", "Nepal", "Sri Lanka", "Pakistan", "Myanmar", "Thailand", "Others"]
    story_counts = [756, 234, 89, 67, 45, 32, 24, 100]
    
    fig = px.bar(x=countries, y=story_counts, title="Stories by Country/Region")
    st.plotly_chart(fig, use_container_width=True)
    
    # Engagement insights
    st.markdown("### 💡 Community Insights")
    
    insights = [
        "🕐 **Peak activity** occurs between 2-4 PM local time",
        "📅 **Weekdays** see 15% more submissions than weekends",
        "🏆 **Top 10% of users** contribute 40% of all stories",
        "🌍 **India** accounts for 60% of all submissions",
        "❤️ **Stories with cultural context** receive 25% more likes",
        "🔄 **Return rate**: 68% of users submit multiple stories"
    ]
    
    for insight in insights:
        st.markdown(insight)
