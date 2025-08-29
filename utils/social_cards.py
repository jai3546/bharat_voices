"""
Social media card generator for sharing stories
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import qrcode
from typing import Dict, Any, Optional
import textwrap
import requests
from utils.config import Config

class SocialCardGenerator:
    """Generates shareable social media cards for stories"""
    
    def __init__(self):
        self.config = Config()
        self.default_font_size = 24
        self.title_font_size = 32
        self.small_font_size = 16
    
    def generate_story_card(self, story_data: Dict[str, Any], style: str = "modern") -> bytes:
        """
        Generate a social media card for a story
        
        Args:
            story_data: Dictionary containing story information
            style: Card style ("modern", "traditional", "minimal")
            
        Returns:
            Image bytes for the generated card
        """
        try:
            # Create image
            width = self.config.CARD_WIDTH
            height = self.config.CARD_HEIGHT
            
            # Choose colors based on style
            colors = self._get_style_colors(style)
            
            # Create image with background
            img = Image.new('RGB', (width, height), colors['background'])
            draw = ImageDraw.Draw(img)
            
            # Add background pattern or gradient
            self._add_background_pattern(img, draw, style, colors)
            
            # Add content
            self._add_story_content(img, draw, story_data, colors)
            
            # Add footer with branding
            self._add_footer(img, draw, colors)
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG', quality=95)
            img_bytes.seek(0)
            
            return img_bytes.getvalue()
            
        except Exception as e:
            st.error(f"Error generating story card: {str(e)}")
            return self._generate_fallback_card(story_data)
    
    def _get_style_colors(self, style: str) -> Dict[str, str]:
        """Get color scheme for different styles"""
        color_schemes = {
            "modern": {
                "background": "#667eea",
                "text": "#ffffff",
                "accent": "#764ba2",
                "secondary": "#f093fb"
            },
            "traditional": {
                "background": "#8B4513",
                "text": "#F5DEB3",
                "accent": "#DAA520",
                "secondary": "#CD853F"
            },
            "minimal": {
                "background": "#2c3e50",
                "text": "#ecf0f1",
                "accent": "#3498db",
                "secondary": "#95a5a6"
            }
        }
        
        return color_schemes.get(style, color_schemes["modern"])
    
    def _add_background_pattern(self, img: Image.Image, draw: ImageDraw.Draw, style: str, colors: Dict[str, str]):
        """Add background pattern or gradient"""
        width, height = img.size
        
        if style == "traditional":
            # Add decorative border
            border_width = 20
            draw.rectangle([0, 0, width, border_width], fill=colors['accent'])
            draw.rectangle([0, height-border_width, width, height], fill=colors['accent'])
            draw.rectangle([0, 0, border_width, height], fill=colors['accent'])
            draw.rectangle([width-border_width, 0, width, height], fill=colors['accent'])
            
        elif style == "modern":
            # Add subtle geometric shapes
            for i in range(5):
                x = width - 100 + i * 20
                y = height - 100 + i * 20
                draw.ellipse([x, y, x+50, y+50], fill=colors['secondary'], outline=None)
    
    def _add_story_content(self, img: Image.Image, draw: ImageDraw.Draw, story_data: Dict[str, Any], colors: Dict[str, str]):
        """Add story content to the card"""
        width, height = img.size
        margin = 60
        
        try:
            # Try to load custom fonts (fallback to default if not available)
            title_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        except:
            title_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Add title
        title = story_data.get("title", "Cultural Story")
        title_wrapped = textwrap.fill(title, width=30)
        
        # Calculate title position
        title_bbox = draw.textbbox((0, 0), title_wrapped, font=title_font)
        title_height = title_bbox[3] - title_bbox[1]
        title_y = margin
        
        draw.text((margin, title_y), title_wrapped, fill=colors['text'], font=title_font)
        
        # Add content
        content = story_data.get("content", "")
        if len(content) > 200:
            content = content[:197] + "..."
        
        content_wrapped = textwrap.fill(content, width=50)
        content_y = title_y + title_height + 40
        
        draw.text((margin, content_y), content_wrapped, fill=colors['text'], font=content_font)
        
        # Add metadata
        language = story_data.get("language", "Unknown")
        category = story_data.get("category", "Story")
        content_type = story_data.get("content_type", "Story")
        
        metadata_y = height - 120
        
        # Language tag
        lang_text = f"🌍 {language}"
        draw.text((margin, metadata_y), lang_text, fill=colors['accent'], font=small_font)
        
        # Category tag
        cat_text = f"🏷️ {category}"
        draw.text((margin, metadata_y + 25), cat_text, fill=colors['accent'], font=small_font)
        
        # Content type
        type_text = f"📖 {content_type}"
        draw.text((margin, metadata_y + 50), type_text, fill=colors['accent'], font=small_font)
    
    def _add_footer(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """Add footer with branding"""
        width, height = img.size
        
        try:
            small_font = ImageFont.load_default()
        except:
            small_font = ImageFont.load_default()
        
        # Add branding
        branding_text = "🗣️ Bharat Voices - Preserving Cultural Wisdom"
        
        # Calculate text position (centered at bottom)
        text_bbox = draw.textbbox((0, 0), branding_text, font=small_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (width - text_width) // 2
        text_y = height - 30
        
        draw.text((text_x, text_y), branding_text, fill=colors['secondary'], font=small_font)
    
    def _generate_fallback_card(self, story_data: Dict[str, Any]) -> bytes:
        """Generate a simple fallback card if main generation fails"""
        try:
            # Create simple card
            img = Image.new('RGB', (800, 600), '#667eea')
            draw = ImageDraw.Draw(img)
            
            # Add simple text
            title = story_data.get("title", "Cultural Story")
            draw.text((50, 50), title, fill='white')
            
            content = story_data.get("content", "")[:100] + "..."
            draw.text((50, 100), content, fill='white')
            
            draw.text((50, 550), "Bharat Voices", fill='white')
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            return img_bytes.getvalue()
            
        except Exception as e:
            st.error(f"Fallback card generation failed: {str(e)}")
            return b''
    
    def generate_qr_code(self, story_url: str) -> bytes:
        """
        Generate QR code for story sharing
        
        Args:
            story_url: URL to the story
            
        Returns:
            QR code image bytes
        """
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(story_url)
            qr.make(fit=True)
            
            # Create QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            qr_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            return img_bytes.getvalue()
            
        except Exception as e:
            st.error(f"QR code generation failed: {str(e)}")
            return b''
    
    def create_story_collage(self, stories: list, title: str = "Cultural Stories") -> bytes:
        """
        Create a collage of multiple stories
        
        Args:
            stories: List of story data dictionaries
            title: Title for the collage
            
        Returns:
            Collage image bytes
        """
        try:
            # Calculate grid dimensions
            num_stories = len(stories)
            if num_stories <= 4:
                cols = 2
                rows = 2
            elif num_stories <= 9:
                cols = 3
                rows = 3
            else:
                cols = 4
                rows = 4
                stories = stories[:16]  # Limit to 16 stories
            
            # Card dimensions
            card_width = 300
            card_height = 200
            margin = 20
            
            # Total image dimensions
            total_width = cols * card_width + (cols + 1) * margin
            total_height = rows * card_height + (rows + 1) * margin + 100  # Extra space for title
            
            # Create collage image
            collage = Image.new('RGB', (total_width, total_height), '#f8f9fa')
            draw = ImageDraw.Draw(collage)
            
            # Add title
            try:
                title_font = ImageFont.load_default()
            except:
                title_font = ImageFont.load_default()
            
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (total_width - title_width) // 2
            draw.text((title_x, 20), title, fill='#2c3e50', font=title_font)
            
            # Add story cards
            for i, story in enumerate(stories):
                if i >= cols * rows:
                    break
                
                row = i // cols
                col = i % cols
                
                x = margin + col * (card_width + margin)
                y = 80 + margin + row * (card_height + margin)
                
                # Create mini card for story
                card_img = self._create_mini_card(story, card_width, card_height)
                collage.paste(card_img, (x, y))
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            collage.save(img_bytes, format='PNG', quality=95)
            img_bytes.seek(0)
            
            return img_bytes.getvalue()
            
        except Exception as e:
            st.error(f"Collage generation failed: {str(e)}")
            return b''
    
    def _create_mini_card(self, story_data: Dict[str, Any], width: int, height: int) -> Image.Image:
        """Create a mini card for collage"""
        try:
            # Create mini card
            img = Image.new('RGB', (width, height), '#667eea')
            draw = ImageDraw.Draw(img)
            
            # Add border
            draw.rectangle([0, 0, width-1, height-1], outline='#764ba2', width=2)
            
            # Add content
            margin = 15
            
            try:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Title
            title = story_data.get("title", "Story")
            if len(title) > 25:
                title = title[:22] + "..."
            draw.text((margin, margin), title, fill='white', font=font)
            
            # Content preview
            content = story_data.get("content", "")
            if len(content) > 80:
                content = content[:77] + "..."
            
            content_wrapped = textwrap.fill(content, width=25)
            draw.text((margin, margin + 30), content_wrapped, fill='white', font=small_font)
            
            # Language
            language = story_data.get("language", "")
            if language:
                draw.text((margin, height - 30), f"🌍 {language}", fill='#f093fb', font=small_font)
            
            return img
            
        except Exception as e:
            # Return simple colored rectangle if mini card creation fails
            img = Image.new('RGB', (width, height), '#95a5a6')
            return img
    
    def get_sharing_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get available sharing templates"""
        return {
            "modern": {
                "name": "Modern",
                "description": "Clean, contemporary design with gradients",
                "preview_color": "#667eea"
            },
            "traditional": {
                "name": "Traditional",
                "description": "Classic design with decorative elements",
                "preview_color": "#8B4513"
            },
            "minimal": {
                "name": "Minimal",
                "description": "Simple, elegant design with focus on content",
                "preview_color": "#2c3e50"
            }
        }
    
    def generate_instagram_story(self, story_data: Dict[str, Any]) -> bytes:
        """Generate Instagram story format (9:16 aspect ratio)"""
        try:
            width = 1080
            height = 1920
            
            img = Image.new('RGB', (width, height), '#667eea')
            draw = ImageDraw.Draw(img)
            
            # Add gradient background
            for y in range(height):
                r = int(102 + (118 - 102) * y / height)
                g = int(126 + (75 - 126) * y / height)
                b = int(234 + (162 - 234) * y / height)
                color = (r, g, b)
                draw.line([(0, y), (width, y)], fill=color)
            
            # Add content with larger fonts for mobile
            margin = 80
            
            try:
                title_font = ImageFont.load_default()
                content_font = ImageFont.load_default()
            except:
                title_font = ImageFont.load_default()
                content_font = ImageFont.load_default()
            
            # Title
            title = story_data.get("title", "Cultural Story")
            title_wrapped = textwrap.fill(title, width=20)
            draw.text((margin, 200), title_wrapped, fill='white', font=title_font)
            
            # Content
            content = story_data.get("content", "")
            if len(content) > 300:
                content = content[:297] + "..."
            
            content_wrapped = textwrap.fill(content, width=35)
            draw.text((margin, 400), content_wrapped, fill='white', font=content_font)
            
            # Branding at bottom
            draw.text((margin, height - 200), "🗣️ Bharat Voices", fill='white', font=title_font)
            draw.text((margin, height - 150), "Preserving Cultural Wisdom", fill='white', font=content_font)
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG', quality=95)
            img_bytes.seek(0)
            
            return img_bytes.getvalue()
            
        except Exception as e:
            st.error(f"Instagram story generation failed: {str(e)}")
            return b''
