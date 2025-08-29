"""
Gamification system for badges, achievements, and user engagement
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from utils.config import Config
from utils.database import DatabaseManager

class GamificationManager:
    """Manages badges, achievements, streaks, and leaderboards"""
    
    def __init__(self):
        self.config = Config()
        self.db_manager = DatabaseManager()
    
    def check_and_award_badges(self, user_id: str) -> List[str]:
        """
        Check user achievements and award new badges
        
        Args:
            user_id: User identifier
            
        Returns:
            List of newly awarded badge keys
        """
        if not user_id:
            return []
        
        # Get user stats
        user_stats = self.db_manager.get_user_stats(user_id)
        current_badges = set(user_stats.get("badges", []))
        new_badges = []
        
        # Check each badge requirement
        for badge_key, badge_info in self.config.BADGES.items():
            if badge_key in current_badges:
                continue  # User already has this badge
            
            if self._check_badge_requirement(badge_key, badge_info, user_stats):
                new_badges.append(badge_key)
                current_badges.add(badge_key)
                self._award_badge(user_id, badge_key)
        
        return new_badges
    
    def _check_badge_requirement(self, badge_key: str, badge_info: Dict[str, Any], user_stats: Dict[str, Any]) -> bool:
        """Check if user meets badge requirement"""
        requirement = badge_info.get("requirement", 0)
        
        if badge_key == "first_story":
            return user_stats.get("total_submissions", 0) >= 1
        
        elif badge_key == "cultural_preserver":
            return user_stats.get("total_submissions", 0) >= 10
        
        elif badge_key == "story_weaver":
            return user_stats.get("total_submissions", 0) >= 25
        
        elif badge_key == "wisdom_keeper":
            return user_stats.get("total_submissions", 0) >= 50
        
        elif badge_key == "multilingual":
            return len(user_stats.get("languages_used", [])) >= 3
        
        elif badge_key == "community_favorite":
            return user_stats.get("total_likes", 0) >= 100
        
        elif badge_key == "streak_master":
            return user_stats.get("streak", 0) >= 7
        
        return False
    
    def _award_badge(self, user_id: str, badge_key: str):
        """Award a badge to user"""
        try:
            # This would typically update the user's badge list in the database
            # For now, we'll store it in session state
            if "user_badges" not in st.session_state:
                st.session_state.user_badges = []
            
            if badge_key not in st.session_state.user_badges:
                st.session_state.user_badges.append(badge_key)
            
            # Show badge notification
            badge_info = self.config.BADGES.get(badge_key, {})
            st.success(f"🏆 Badge Earned: {badge_info.get('icon', '🏅')} {badge_info.get('name', 'Achievement')}")
            st.balloons()
            
        except Exception as e:
            st.error(f"Error awarding badge: {str(e)}")
    
    def get_user_badges(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all badges earned by user"""
        user_stats = self.db_manager.get_user_stats(user_id)
        badge_keys = user_stats.get("badges", [])
        
        badges = []
        for badge_key in badge_keys:
            badge_info = self.config.BADGES.get(badge_key, {})
            if badge_info:
                badges.append({
                    "key": badge_key,
                    "name": badge_info.get("name", "Unknown Badge"),
                    "description": badge_info.get("description", ""),
                    "icon": badge_info.get("icon", "🏅"),
                    "earned_date": datetime.now().isoformat()  # Would be stored in DB
                })
        
        return badges
    
    def get_available_badges(self) -> List[Dict[str, Any]]:
        """Get all available badges with progress"""
        badges = []
        
        for badge_key, badge_info in self.config.BADGES.items():
            badges.append({
                "key": badge_key,
                "name": badge_info.get("name", "Unknown Badge"),
                "description": badge_info.get("description", ""),
                "icon": badge_info.get("icon", "🏅"),
                "requirement": badge_info.get("requirement", 0)
            })
        
        return badges
    
    def calculate_user_streak(self, user_id: str) -> int:
        """Calculate user's current submission streak"""
        try:
            # Get user's submissions ordered by date
            submissions = self.db_manager.get_submissions(
                filters={"user_id": user_id}
            )
            
            if not submissions:
                return 0
            
            # Sort by timestamp
            submissions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            # Calculate streak
            streak = 0
            current_date = datetime.now().date()
            
            for submission in submissions:
                submission_date = datetime.fromisoformat(
                    submission.get("timestamp", "")
                ).date()
                
                # Check if submission is from current date or consecutive previous days
                expected_date = current_date - timedelta(days=streak)
                
                if submission_date == expected_date:
                    streak += 1
                elif submission_date < expected_date:
                    break  # Gap in streak
            
            return streak
            
        except Exception as e:
            st.warning(f"Error calculating streak: {str(e)}")
            return 0
    
    def get_leaderboard(self, category: str = "submissions", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get leaderboard for specified category
        
        Args:
            category: "submissions", "likes", "badges", or "streak"
            limit: Number of top users to return
            
        Returns:
            List of user rankings
        """
        try:
            # This would typically query the database for user rankings
            # For now, return mock data
            leaderboard = []
            
            if category == "submissions":
                # Mock top contributors
                mock_users = [
                    {"user_id": "user1", "display_name": "Cultural Keeper", "count": 45, "badge_count": 5},
                    {"user_id": "user2", "display_name": "Story Teller", "count": 38, "badge_count": 4},
                    {"user_id": "user3", "display_name": "Wisdom Sharer", "count": 32, "badge_count": 4},
                    {"user_id": "user4", "display_name": "Heritage Guardian", "count": 28, "badge_count": 3},
                    {"user_id": "user5", "display_name": "Folk Narrator", "count": 25, "badge_count": 3}
                ]
                
                for i, user in enumerate(mock_users[:limit], 1):
                    leaderboard.append({
                        "rank": i,
                        "user_id": user["user_id"],
                        "display_name": user["display_name"],
                        "value": user["count"],
                        "badge_count": user["badge_count"],
                        "metric": "stories"
                    })
            
            elif category == "likes":
                # Mock most liked users
                mock_users = [
                    {"user_id": "user2", "display_name": "Story Teller", "likes": 234},
                    {"user_id": "user1", "display_name": "Cultural Keeper", "likes": 198},
                    {"user_id": "user3", "display_name": "Wisdom Sharer", "likes": 167},
                    {"user_id": "user5", "display_name": "Folk Narrator", "likes": 145},
                    {"user_id": "user4", "display_name": "Heritage Guardian", "likes": 132}
                ]
                
                for i, user in enumerate(mock_users[:limit], 1):
                    leaderboard.append({
                        "rank": i,
                        "user_id": user["user_id"],
                        "display_name": user["display_name"],
                        "value": user["likes"],
                        "metric": "likes"
                    })
            
            return leaderboard
            
        except Exception as e:
            st.error(f"Error getting leaderboard: {str(e)}")
            return []
    
    def get_user_rank(self, user_id: str, category: str = "submissions") -> Dict[str, Any]:
        """Get user's rank in specified category"""
        leaderboard = self.get_leaderboard(category, limit=100)
        
        for entry in leaderboard:
            if entry["user_id"] == user_id:
                return entry
        
        # User not in top rankings
        return {
            "rank": "Not ranked",
            "user_id": user_id,
            "display_name": "You",
            "value": 0,
            "metric": category
        }
    
    def get_achievement_progress(self, user_id: str) -> Dict[str, Any]:
        """Get user's progress towards achievements"""
        user_stats = self.db_manager.get_user_stats(user_id)
        current_badges = set(user_stats.get("badges", []))
        
        progress = {}
        
        for badge_key, badge_info in self.config.BADGES.items():
            if badge_key in current_badges:
                progress[badge_key] = {
                    "completed": True,
                    "progress": 100,
                    "current": badge_info.get("requirement", 0),
                    "target": badge_info.get("requirement", 0)
                }
            else:
                current_value = self._get_current_value_for_badge(badge_key, user_stats)
                target_value = badge_info.get("requirement", 0)
                
                progress[badge_key] = {
                    "completed": False,
                    "progress": min((current_value / target_value) * 100, 100) if target_value > 0 else 0,
                    "current": current_value,
                    "target": target_value
                }
        
        return progress
    
    def _get_current_value_for_badge(self, badge_key: str, user_stats: Dict[str, Any]) -> int:
        """Get current value for badge requirement"""
        if badge_key in ["first_story", "cultural_preserver", "story_weaver", "wisdom_keeper"]:
            return user_stats.get("total_submissions", 0)
        elif badge_key == "multilingual":
            return len(user_stats.get("languages_used", []))
        elif badge_key == "community_favorite":
            return user_stats.get("total_likes", 0)
        elif badge_key == "streak_master":
            return user_stats.get("streak", 0)
        
        return 0
    
    def get_daily_challenge(self) -> Dict[str, Any]:
        """Get today's challenge for users"""
        challenges = [
            {
                "title": "Share a Proverb",
                "description": "Submit a traditional proverb from your culture",
                "reward": "10 points",
                "icon": "🌟"
            },
            {
                "title": "Voice Recording",
                "description": "Record a story using voice input",
                "reward": "15 points",
                "icon": "🎤"
            },
            {
                "title": "New Language",
                "description": "Submit a story in a language you haven't used before",
                "reward": "20 points",
                "icon": "🌍"
            },
            {
                "title": "Community Engagement",
                "description": "Like and comment on 5 community stories",
                "reward": "5 points",
                "icon": "❤️"
            },
            {
                "title": "Cultural Context",
                "description": "Add detailed cultural context to your submission",
                "reward": "10 points",
                "icon": "📚"
            }
        ]
        
        # Return a different challenge based on day of year
        day_of_year = datetime.now().timetuple().tm_yday
        challenge_index = day_of_year % len(challenges)
        
        return challenges[challenge_index]
    
    def display_badge_showcase(self, user_badges: List[Dict[str, Any]]):
        """Display user's badges in a showcase format"""
        if not user_badges:
            st.info("🏅 No badges earned yet. Start sharing stories to earn your first badge!")
            return
        
        st.markdown("### 🏆 Your Badges")
        
        # Display badges in a grid
        cols = st.columns(min(len(user_badges), 4))
        
        for i, badge in enumerate(user_badges):
            with cols[i % 4]:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin: 0.5rem 0;">
                    <div style="font-size: 2rem;">{badge.get('icon', '🏅')}</div>
                    <div style="font-weight: bold; margin: 0.5rem 0;">{badge.get('name', 'Badge')}</div>
                    <div style="font-size: 0.8rem; color: #666;">{badge.get('description', '')}</div>
                </div>
                """, unsafe_allow_html=True)
    
    def display_progress_bars(self, progress: Dict[str, Any]):
        """Display progress bars for achievements"""
        st.markdown("### 📈 Achievement Progress")
        
        for badge_key, prog in progress.items():
            badge_info = self.config.BADGES.get(badge_key, {})
            
            if prog["completed"]:
                st.success(f"✅ {badge_info.get('icon', '🏅')} {badge_info.get('name', 'Achievement')} - Completed!")
            else:
                st.markdown(f"**{badge_info.get('icon', '🏅')} {badge_info.get('name', 'Achievement')}**")
                st.progress(prog["progress"] / 100)
                st.caption(f"{prog['current']}/{prog['target']} - {badge_info.get('description', '')}")
                st.markdown("---")
