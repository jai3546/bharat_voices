"""
Database manager for Google Sheets and Airtable integration
"""

import gspread
import pandas as pd
from google.auth import default
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime, timezone
import json
import uuid
from typing import Dict, List, Any, Optional
import os
from pyairtable import Api
from utils.config import Config

class DatabaseManager:
    """Manages data storage and retrieval from Google Sheets or Airtable"""
    
    def __init__(self):
        self.config = Config()
        self.sheets_client = None
        self.airtable_client = None
        self.spreadsheet = None
        self.base = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize Google Sheets and Airtable clients"""
        try:
            # Initialize Google Sheets
            if os.path.exists(self.config.GOOGLE_CREDENTIALS_PATH):
                scope = [
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive"
                ]
                creds = Credentials.from_service_account_file(
                    self.config.GOOGLE_CREDENTIALS_PATH, 
                    scopes=scope
                )
                self.sheets_client = gspread.authorize(creds)
                
                # Open or create spreadsheet
                try:
                    self.spreadsheet = self.sheets_client.open("Bharat Voices Database")
                except gspread.SpreadsheetNotFound:
                    self.spreadsheet = self.sheets_client.create("Bharat Voices Database")
                    self._setup_sheets()
            
            # Initialize Airtable
            if self.config.AIRTABLE_API_KEY and self.config.AIRTABLE_BASE_ID:
                self.airtable_client = Api(self.config.AIRTABLE_API_KEY)
                self.base = self.airtable_client.base(self.config.AIRTABLE_BASE_ID)
                
        except Exception as e:
            st.error(f"Database initialization error: {str(e)}")
    
    def _setup_sheets(self):
        """Setup initial Google Sheets structure"""
        try:
            # Create worksheets
            worksheets = {
                "submissions": [
                    "id", "timestamp", "user_id", "title", "content", "content_type",
                    "language", "dialect", "english_translation", "ai_translated",
                    "category", "ai_categorized", "audio_url", "likes", "featured",
                    "location", "cultural_context"
                ],
                "users": [
                    "user_id", "display_name", "email", "native_language", "location",
                    "join_date", "total_submissions", "total_likes", "badges", "streak"
                ],
                "interactions": [
                    "id", "user_id", "submission_id", "interaction_type", "timestamp"
                ],
                "analytics": [
                    "date", "total_submissions", "new_users", "active_users",
                    "top_language", "top_category", "featured_story"
                ]
            }
            
            for sheet_name, headers in worksheets.items():
                try:
                    worksheet = self.spreadsheet.worksheet(sheet_name)
                except gspread.WorksheetNotFound:
                    worksheet = self.spreadsheet.add_worksheet(
                        title=sheet_name, 
                        rows=1000, 
                        cols=len(headers)
                    )
                    worksheet.append_row(headers)
                    
        except Exception as e:
            st.error(f"Sheet setup error: {str(e)}")
    
    def save_submission(self, submission_data: Dict[str, Any]) -> str:
        """Save a new submission to the database"""
        try:
            # Generate unique ID
            submission_id = str(uuid.uuid4())
            
            # Prepare data
            row_data = [
                submission_id,
                datetime.now(timezone.utc).isoformat(),
                submission_data.get("user_id", "anonymous"),
                submission_data.get("title", ""),
                submission_data.get("content", ""),
                submission_data.get("content_type", ""),
                submission_data.get("language", ""),
                submission_data.get("dialect", ""),
                submission_data.get("english_translation", ""),
                submission_data.get("ai_translated", False),
                submission_data.get("category", ""),
                submission_data.get("ai_categorized", False),
                submission_data.get("audio_url", ""),
                0,  # initial likes
                False,  # not featured initially
                submission_data.get("location", ""),
                submission_data.get("cultural_context", "")
            ]
            
            # Save to Google Sheets
            if self.spreadsheet:
                worksheet = self.spreadsheet.worksheet("submissions")
                worksheet.append_row(row_data)
            
            # Save to Airtable (if configured)
            if self.base:
                airtable_data = {
                    "ID": submission_id,
                    "Timestamp": datetime.now(timezone.utc).isoformat(),
                    "User ID": submission_data.get("user_id", "anonymous"),
                    "Title": submission_data.get("title", ""),
                    "Content": submission_data.get("content", ""),
                    "Content Type": submission_data.get("content_type", ""),
                    "Language": submission_data.get("language", ""),
                    "English Translation": submission_data.get("english_translation", ""),
                    "Category": submission_data.get("category", ""),
                    "Likes": 0
                }
                self.base.table("Submissions").create(airtable_data)
            
            return submission_id
            
        except Exception as e:
            st.error(f"Error saving submission: {str(e)}")
            return ""
    
    def get_submissions(self, limit: int = 50, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Retrieve submissions from database"""
        try:
            submissions = []
            
            if self.spreadsheet:
                worksheet = self.spreadsheet.worksheet("submissions")
                records = worksheet.get_all_records()
                
                # Apply filters
                if filters:
                    filtered_records = []
                    for record in records:
                        match = True
                        for key, value in filters.items():
                            if key in record and record[key] != value:
                                match = False
                                break
                        if match:
                            filtered_records.append(record)
                    records = filtered_records
                
                # Sort by timestamp (newest first) and limit
                records = sorted(records, key=lambda x: x.get("timestamp", ""), reverse=True)
                submissions = records[:limit]
            
            return submissions
            
        except Exception as e:
            st.error(f"Error retrieving submissions: {str(e)}")
            return []
    
    def update_submission_likes(self, submission_id: str, increment: int = 1) -> bool:
        """Update likes count for a submission"""
        try:
            if self.spreadsheet:
                worksheet = self.spreadsheet.worksheet("submissions")
                records = worksheet.get_all_records()
                
                for i, record in enumerate(records, start=2):  # Start from row 2 (after header)
                    if record.get("id") == submission_id:
                        current_likes = int(record.get("likes", 0))
                        new_likes = max(0, current_likes + increment)
                        worksheet.update_cell(i, 14, new_likes)  # Column 14 is likes
                        return True
            
            return False
            
        except Exception as e:
            st.error(f"Error updating likes: {str(e)}")
            return False
    
    def save_user_interaction(self, user_id: str, submission_id: str, interaction_type: str):
        """Save user interaction (like, share, etc.)"""
        try:
            interaction_data = [
                str(uuid.uuid4()),
                user_id,
                submission_id,
                interaction_type,
                datetime.now(timezone.utc).isoformat()
            ]
            
            if self.spreadsheet:
                worksheet = self.spreadsheet.worksheet("interactions")
                worksheet.append_row(interaction_data)
                
        except Exception as e:
            st.error(f"Error saving interaction: {str(e)}")
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            stats = {
                "total_submissions": 0,
                "total_likes": 0,
                "languages_used": set(),
                "categories_used": set(),
                "streak": 0,
                "badges": []
            }
            
            if self.spreadsheet:
                # Get submissions by user
                worksheet = self.spreadsheet.worksheet("submissions")
                records = worksheet.get_all_records()
                
                user_submissions = [r for r in records if r.get("user_id") == user_id]
                stats["total_submissions"] = len(user_submissions)
                
                for submission in user_submissions:
                    stats["total_likes"] += int(submission.get("likes", 0))
                    if submission.get("language"):
                        stats["languages_used"].add(submission["language"])
                    if submission.get("category"):
                        stats["categories_used"].add(submission["category"])
                
                stats["languages_used"] = list(stats["languages_used"])
                stats["categories_used"] = list(stats["categories_used"])
            
            return stats
            
        except Exception as e:
            st.error(f"Error getting user stats: {str(e)}")
            return {}
    
    def get_analytics_data(self) -> Dict[str, Any]:
        """Get platform analytics data"""
        try:
            analytics = {
                "total_submissions": 0,
                "total_users": 0,
                "languages_count": 0,
                "categories_distribution": {},
                "languages_distribution": {},
                "recent_activity": []
            }
            
            if self.spreadsheet:
                # Get submissions data
                submissions_ws = self.spreadsheet.worksheet("submissions")
                submissions = submissions_ws.get_all_records()
                
                analytics["total_submissions"] = len(submissions)
                
                # Count languages and categories
                languages = {}
                categories = {}
                
                for submission in submissions:
                    lang = submission.get("language", "Unknown")
                    cat = submission.get("category", "Uncategorized")
                    
                    languages[lang] = languages.get(lang, 0) + 1
                    categories[cat] = categories.get(cat, 0) + 1
                
                analytics["languages_distribution"] = languages
                analytics["categories_distribution"] = categories
                analytics["languages_count"] = len(languages)
                
                # Get recent activity (last 10 submissions)
                recent = sorted(submissions, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]
                analytics["recent_activity"] = recent
            
            return analytics
            
        except Exception as e:
            st.error(f"Error getting analytics: {str(e)}")
            return {}
    
    def search_submissions(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search submissions by content, title, or metadata"""
        try:
            results = []
            
            if self.spreadsheet:
                worksheet = self.spreadsheet.worksheet("submissions")
                records = worksheet.get_all_records()
                
                query_lower = query.lower()
                
                for record in records:
                    # Search in title, content, and translation
                    searchable_text = " ".join([
                        record.get("title", ""),
                        record.get("content", ""),
                        record.get("english_translation", "")
                    ]).lower()
                    
                    if query_lower in searchable_text:
                        # Apply additional filters if provided
                        if filters:
                            match = True
                            for key, value in filters.items():
                                if key in record and record[key] != value:
                                    match = False
                                    break
                            if match:
                                results.append(record)
                        else:
                            results.append(record)
            
            return results
            
        except Exception as e:
            st.error(f"Error searching submissions: {str(e)}")
            return []
