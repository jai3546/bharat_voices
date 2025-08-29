"""
Community page for browsing and interacting with stories
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from utils.config import Config
from utils.database import DatabaseManager
from utils.social_cards import SocialCardGenerator

def show_community_page():
    """Display the community page with story feed and interactions"""
    st.markdown("## 👥 Community Stories")
    st.markdown("Discover and engage with cultural stories from around the world")
    
    # Initialize services
    config = Config()
    db_manager = DatabaseManager()
    card_generator = SocialCardGenerator()
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["🌟 Featured", "🔥 Recent", "🔍 Search"])
    
    with tab1:
        show_featured_stories(config, db_manager, card_generator)
    
    with tab2:
        show_recent_stories(config, db_manager, card_generator)
    
    with tab3:
        show_search_interface(config, db_manager, card_generator)

def show_featured_stories(config: Config, db_manager: DatabaseManager, card_generator: SocialCardGenerator):
    """Show featured stories section"""
    st.markdown("### ⭐ Featured Stories")
    
    # Get featured stories
    featured_stories = db_manager.get_submissions(
        filters={"featured": True},
        limit=10
    )
    
    if not featured_stories:
        # Show mock featured stories for demo
        featured_stories = get_mock_featured_stories()
    
    # Display featured story of the day
    if featured_stories:
        story_of_day = featured_stories[0]
        display_featured_story_card(story_of_day, card_generator)
    
    # Display other featured stories
    st.markdown("### 🌟 More Featured Stories")
    
    if len(featured_stories) > 1:
        for story in featured_stories[1:6]:  # Show next 5 featured stories
            display_story_card(story, db_manager, card_generator, featured=True)
    else:
        st.info("No additional featured stories available.")

def show_recent_stories(config: Config, db_manager: DatabaseManager, card_generator: SocialCardGenerator):
    """Show recent stories section"""
    st.markdown("### 🔥 Recent Stories")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        language_filter = st.selectbox(
            "Filter by Language",
            options=["All Languages"] + list(config.LANGUAGES.values()),
            key="recent_language_filter"
        )
    
    with col2:
        category_filter = st.selectbox(
            "Filter by Category",
            options=["All Categories"] + config.CATEGORIES,
            key="recent_category_filter"
        )
    
    with col3:
        content_type_filter = st.selectbox(
            "Filter by Type",
            options=["All Types"] + config.CONTENT_TYPES,
            key="recent_type_filter"
        )
    
    # Build filters
    filters = {}
    if language_filter != "All Languages":
        filters["language"] = language_filter
    if category_filter != "All Categories":
        filters["category"] = category_filter
    if content_type_filter != "All Types":
        filters["content_type"] = content_type_filter
    
    # Get recent stories
    recent_stories = db_manager.get_submissions(filters=filters, limit=20)
    
    if not recent_stories:
        # Show mock recent stories for demo
        recent_stories = get_mock_recent_stories()
    
    # Display stories
    if recent_stories:
        for story in recent_stories:
            display_story_card(story, db_manager, card_generator)
    else:
        st.info("No stories found matching your filters.")

def show_search_interface(config: Config, db_manager: DatabaseManager, card_generator: SocialCardGenerator):
    """Show search interface"""
    st.markdown("### 🔍 Search Stories")
    
    # Search form
    with st.form("search_form"):
        search_query = st.text_input(
            "Search stories, proverbs, and sayings...",
            placeholder="Enter keywords, themes, or phrases"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            search_language = st.selectbox(
                "Language",
                options=["Any Language"] + list(config.LANGUAGES.values())
            )
        
        with col2:
            search_category = st.selectbox(
                "Category",
                options=["Any Category"] + config.CATEGORIES
            )
        
        search_submitted = st.form_submit_button("🔍 Search", type="primary")
    
    # Perform search
    if search_submitted and search_query:
        with st.spinner("Searching stories..."):
            # Build search filters
            search_filters = {}
            if search_language != "Any Language":
                search_filters["language"] = search_language
            if search_category != "Any Category":
                search_filters["category"] = search_category
            
            # Search stories
            search_results = db_manager.search_submissions(search_query, search_filters)
            
            if not search_results:
                # Show mock search results for demo
                search_results = get_mock_search_results(search_query)
            
            # Display results
            if search_results:
                st.success(f"Found {len(search_results)} stories matching your search")
                
                for story in search_results:
                    display_story_card(story, db_manager, card_generator, highlight_query=search_query)
            else:
                st.warning("No stories found matching your search criteria.")
                st.markdown("**Try:**")
                st.markdown("- Using different keywords")
                st.markdown("- Removing filters")
                st.markdown("- Searching in different languages")

def display_featured_story_card(story: Dict[str, Any], card_generator: SocialCardGenerator):
    """Display the featured story of the day in a special card"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); 
                padding: 2rem; border-radius: 15px; margin: 1rem 0; 
                border: 3px solid #fdcb6e; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        <h3 style="color: #2d3436; margin: 0 0 1rem 0;">🌟 Featured Story of the Day</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the story content
    display_story_card(story, None, card_generator, featured=True, expanded=True)

def display_story_card(story: Dict[str, Any], db_manager: Optional[DatabaseManager], 
                      card_generator: SocialCardGenerator, featured: bool = False, 
                      expanded: bool = False, highlight_query: str = ""):
    """Display a story card with interaction options"""
    
    # Create card container
    card_style = "featured-story" if featured else "submission-card"
    
    with st.container():
        # Story header
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            title = story.get("title", "Untitled Story")
            if highlight_query and highlight_query.lower() in title.lower():
                title = title.replace(highlight_query, f"**{highlight_query}**")
            st.markdown(f"### {title}")
        
        with col2:
            likes = story.get("likes", 0)
            if st.button(f"❤️ {likes}", key=f"like_{story.get('id', 'unknown')}"):
                handle_like_story(story, db_manager)
        
        with col3:
            if st.button("📤 Share", key=f"share_{story.get('id', 'unknown')}"):
                show_share_options(story, card_generator)
        
        # Story content
        content = story.get("content", "")
        if highlight_query and highlight_query.lower() in content.lower():
            content = content.replace(highlight_query, f"**{highlight_query}**")
        
        if len(content) > 300 and not expanded:
            content = content[:297] + "..."
        
        st.markdown(f"*{content}*")
        
        # Translation (if available)
        translation = story.get("english_translation", "")
        if translation and translation != content:
            with st.expander("🌐 English Translation"):
                st.markdown(translation)
        
        # Metadata
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            language = story.get("language", "Unknown")
            st.markdown(f"**Language:** {language}")
        
        with col2:
            category = story.get("category", "Uncategorized")
            st.markdown(f"**Category:** {category}")
        
        with col3:
            content_type = story.get("content_type", "Story")
            st.markdown(f"**Type:** {content_type}")
        
        with col4:
            timestamp = story.get("timestamp", "")
            if timestamp:
                try:
                    date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_date = date.strftime("%b %d, %Y")
                    st.markdown(f"**Date:** {formatted_date}")
                except:
                    st.markdown(f"**Date:** {timestamp[:10]}")
        
        # Cultural context (if available)
        cultural_context = story.get("cultural_context", "")
        if cultural_context:
            with st.expander("📚 Cultural Context"):
                st.markdown(cultural_context)
        
        # Location (if available)
        location = story.get("location", "")
        if location:
            st.markdown(f"**📍 Origin:** {location}")
        
        st.markdown("---")

def handle_like_story(story: Dict[str, Any], db_manager: Optional[DatabaseManager]):
    """Handle story like action"""
    if db_manager:
        story_id = story.get("id", "")
        user_id = st.session_state.get("user_id", f"anon_{hash(st.session_state.get('session_id', 'unknown'))}")
        
        # Update likes in database
        success = db_manager.update_submission_likes(story_id, 1)
        
        if success:
            # Save interaction
            db_manager.save_user_interaction(user_id, story_id, "like")
            st.success("❤️ Story liked!")
            st.rerun()
        else:
            st.error("Failed to like story. Please try again.")
    else:
        st.success("❤️ Story liked!")

def show_share_options(story: Dict[str, Any], card_generator: SocialCardGenerator):
    """Show sharing options for a story"""
    with st.expander("📤 Share Options", expanded=True):
        st.markdown("### Share this story")
        
        # Generate story URL (mock for demo)
        story_url = f"https://bharatvoices.app/story/{story.get('id', 'demo')}"
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📱 Social Media Card**")
            
            # Style selection
            templates = card_generator.get_sharing_templates()
            selected_style = st.selectbox(
                "Choose style:",
                options=list(templates.keys()),
                format_func=lambda x: templates[x]["name"],
                key=f"style_{story.get('id', 'unknown')}"
            )
            
            if st.button("🎨 Generate Card", key=f"generate_{story.get('id', 'unknown')}"):
                with st.spinner("Generating card..."):
                    card_bytes = card_generator.generate_story_card(story, selected_style)
                    if card_bytes:
                        st.image(card_bytes, caption="Social Media Card")
                        st.download_button(
                            "💾 Download Card",
                            data=card_bytes,
                            file_name=f"story_card_{story.get('id', 'demo')}.png",
                            mime="image/png"
                        )
        
        with col2:
            st.markdown("**🔗 Quick Share**")
            
            # Copy link
            st.code(story_url)
            
            # Social media links
            title = story.get("title", "Cultural Story")
            encoded_title = title.replace(" ", "%20")
            encoded_url = story_url.replace(":", "%3A").replace("/", "%2F")
            
            social_links = {
                "Twitter": f"https://twitter.com/intent/tweet?text={encoded_title}&url={encoded_url}",
                "Facebook": f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}",
                "WhatsApp": f"https://wa.me/?text={encoded_title}%20{encoded_url}",
                "Telegram": f"https://t.me/share/url?url={encoded_url}&text={encoded_title}"
            }
            
            for platform, link in social_links.items():
                st.markdown(f"[📱 Share on {platform}]({link})")
            
            # QR Code
            if st.button("📱 Generate QR Code", key=f"qr_{story.get('id', 'unknown')}"):
                qr_bytes = card_generator.generate_qr_code(story_url)
                if qr_bytes:
                    st.image(qr_bytes, caption="QR Code for Story")

def get_mock_featured_stories() -> List[Dict[str, Any]]:
    """Get mock featured stories for demo"""
    return [
        {
            "id": "featured_1",
            "title": "The Wise Elephant",
            "content": "An elephant never forgets, but it also never holds grudges. True wisdom lies in remembering lessons while releasing resentment.",
            "content_type": "Proverb",
            "language": "English",
            "category": "Wisdom & Life Lessons",
            "english_translation": "An elephant never forgets, but it also never holds grudges. True wisdom lies in remembering lessons while releasing resentment.",
            "likes": 47,
            "featured": True,
            "timestamp": datetime.now().isoformat(),
            "cultural_context": "This saying originates from African wisdom traditions, where elephants are revered for their memory and gentle nature despite their strength."
        },
        {
            "id": "featured_2", 
            "title": "Unity in Diversity",
            "content": "जैसे नदियाँ समुद्र में मिलकर एक हो जाती हैं, वैसे ही अलग-अलग संस्कृतियाँ मिलकर मानवता बनाती हैं।",
            "content_type": "Saying",
            "language": "Hindi",
            "category": "Family & Community",
            "english_translation": "Just as rivers merge into the ocean to become one, different cultures unite to form humanity.",
            "likes": 32,
            "featured": True,
            "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
            "location": "Uttar Pradesh, India"
        }
    ]

def get_mock_recent_stories() -> List[Dict[str, Any]]:
    """Get mock recent stories for demo"""
    return [
        {
            "id": "recent_1",
            "title": "The Patient Farmer",
            "content": "A farmer who plants today eats tomorrow. Patience is the seed of prosperity.",
            "content_type": "Proverb",
            "language": "English",
            "category": "Work & Perseverance",
            "likes": 15,
            "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()
        },
        {
            "id": "recent_2",
            "title": "Mother's Love",
            "content": "মায়ের ভালোবাসা সমুদ্রের মতো গভীর, আকাশের মতো বিস্তৃত।",
            "content_type": "Saying",
            "language": "Bengali",
            "category": "Family & Community",
            "english_translation": "A mother's love is as deep as the ocean, as vast as the sky.",
            "likes": 28,
            "timestamp": (datetime.now() - timedelta(hours=5)).isoformat(),
            "location": "West Bengal, India"
        }
    ]

def get_mock_search_results(query: str) -> List[Dict[str, Any]]:
    """Get mock search results for demo"""
    return [
        {
            "id": "search_1",
            "title": f"Story containing '{query}'",
            "content": f"This is a sample story that contains the search term '{query}' and demonstrates how search results would appear.",
            "content_type": "Story",
            "language": "English",
            "category": "Tradition & Culture",
            "likes": 12,
            "timestamp": datetime.now().isoformat()
        }
    ]
