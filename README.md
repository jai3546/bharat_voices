# 🗣️ Bharat Voices - Cultural Storytelling Platform

A lightweight, multilingual Streamlit application designed as a cultural storytelling platform that doubles as a corpus collection engine. Preserve and share cultural wisdom through proverbs, folk tales, sayings, and stories from around the world.

## ✨ Features

### 📝 Story Submission
- **Text Input**: Submit stories directly through a user-friendly form
- **Voice Input**: Record stories using speech-to-text (Whisper integration)
- **Multilingual Support**: Support for 60+ languages and dialects
- **No Login Required**: Anonymous submissions to encourage participation

### 🤖 AI-Powered Features
- **Auto Translation**: Automatic translation to English using Hugging Face models
- **Smart Categorization**: AI categorizes content into themes (wisdom, humor, nature, etc.)
- **Editable Suggestions**: Users can review and edit AI translations and categories

### 👥 Community Features
- **Community Wall**: Browse and discover stories from around the world
- **Social Engagement**: Upvote, like, and mark stories as "Featured of the Day"
- **Search & Filter**: Find stories by language, category, or content

### 🏆 Gamification
- **Badges System**: Earn badges like "Cultural Preserver", "Story Weaver", "Wisdom Keeper"
- **Streak Counters**: Track daily submission streaks
- **Leaderboards**: See top contributors and most liked stories

### 📱 Social Sharing
- **Story Cards**: Generate beautiful social media-ready cards
- **QR Codes**: Share stories via QR codes
- **Export Options**: Download stories as CSV or PDF

### 📊 Analytics & Admin
- **Admin Dashboard**: Comprehensive view of all submissions
- **Analytics**: Track platform growth, popular languages, and categories
- **Progress Tracking**: Visual progress bars for collection goals

### 🔄 Offline Support
- **Local Drafts**: Save drafts locally when offline
- **Auto Sync**: Sync when connection is restored
- **Low Bandwidth**: Optimized for slow internet connections

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
```bash
git clone <repository-url>
cd bharat-voices
```

2. **Run the setup script**
```bash
python setup.py
```

3. **Configure environment variables**
Edit the `.env` file with your API keys and settings:
```env
# Google Sheets (for data storage)
GOOGLE_CREDENTIALS_PATH=credentials.json

# AI Services (optional but recommended)
HUGGINGFACE_API_KEY=your-huggingface-api-key

# Airtable (alternative to Google Sheets)
AIRTABLE_API_KEY=your-airtable-api-key
AIRTABLE_BASE_ID=your-airtable-base-id
```

4. **Set up Google Sheets (recommended)**
- Create a Google Cloud Project
- Enable Google Sheets API
- Create a Service Account and download credentials
- Rename credentials to `credentials.json`
- Share your Google Sheet with the service account email

5. **Run the application**
```bash
streamlit run main.py
```

6. **Open your browser**
Navigate to `http://localhost:8501`

## 🛠️ Configuration

### Data Storage Options

#### Google Sheets (Recommended)
- Free and easy to set up
- Real-time collaboration
- Built-in backup and version control
- Easy data export

#### Airtable (Alternative)
- More advanced database features
- Better API performance
- Built-in forms and views
- Requires paid plan for larger datasets

### AI Services

#### Hugging Face (Recommended)
- Free tier available
- High-quality translation models
- Support for many languages
- Easy to set up

#### OpenAI (Alternative)
- Higher quality but paid
- Better for complex categorization
- Requires API key

### Audio Processing
- Uses OpenAI Whisper for speech-to-text
- Supports multiple audio formats
- Automatic audio preprocessing
- Works offline after model download

## 📁 Project Structure

```
bharat-voices/
├── main.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── setup.py               # Setup script
├── .env.example           # Environment variables template
├── README.md              # This file
├── utils/                 # Utility modules
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database management
│   ├── translation.py     # Translation services
│   ├── categorization.py  # AI categorization
│   ├── audio.py           # Audio processing
│   ├── gamification.py    # Badges and achievements
│   └── social_cards.py    # Social media card generation
├── pages/                 # Streamlit pages
│   ├── submission.py      # Story submission page
│   ├── community.py       # Community wall
│   ├── admin.py           # Admin dashboard
│   ├── profile.py         # User profile
│   └── analytics.py       # Analytics dashboard
├── data/                  # Data storage
├── uploads/               # File uploads
├── exports/               # Generated exports
├── cache/                 # Application cache
└── .streamlit/            # Streamlit configuration
    └── config.toml        # Streamlit settings
```

## 🌍 Supported Languages

The platform supports 60+ languages including:

**South Asian**: Hindi, Bengali, Telugu, Tamil, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Nepali, Sinhala

**East Asian**: Chinese, Japanese, Korean

**Southeast Asian**: Thai, Vietnamese, Indonesian, Malay, Filipino

**Middle Eastern**: Arabic, Persian, Turkish

**European**: English, Spanish, French, German, Italian, Portuguese, Russian, Polish, Dutch, Swedish, and many more.

## 🎯 Use Cases

### Cultural Preservation
- Document endangered languages and dialects
- Preserve traditional stories and wisdom
- Create digital archives of oral traditions

### Research & Academia
- Linguistic research and analysis
- Cultural studies and anthropology
- Comparative literature studies

### Education
- Language learning resources
- Cultural exchange programs
- Storytelling workshops

### Community Building
- Connect diaspora communities
- Share cultural heritage
- Intergenerational knowledge transfer

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Submit Stories**: Share your cultural stories and proverbs
2. **Improve Translations**: Review and improve AI translations
3. **Add Languages**: Help add support for more languages
4. **Report Issues**: Report bugs or suggest improvements
5. **Code Contributions**: Submit pull requests for new features

## 📊 Analytics & Insights

The platform provides rich analytics including:
- **Collection Progress**: Track towards corpus goals
- **Language Distribution**: See which languages are most represented
- **Category Analysis**: Understand themes and topics
- **User Engagement**: Monitor likes, shares, and contributions
- **Geographic Distribution**: See where stories come from

## 🔒 Privacy & Data

- **Anonymous Submissions**: No login required for basic use
- **Data Ownership**: Users retain rights to their stories
- **Open Access**: Stories are publicly accessible for research
- **Export Options**: Users can download their data anytime
- **GDPR Compliant**: Respects user privacy and data rights

## 🆘 Support

- **Documentation**: Check this README and inline help
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join community discussions
- **Email**: Contact the maintainers directly

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI Whisper** for speech-to-text capabilities
- **Hugging Face** for translation and AI models
- **Streamlit** for the amazing web framework
- **Google Sheets API** for data storage
- **All contributors** who share their cultural stories

---

**Made with ❤️ for preserving cultural wisdom and connecting communities worldwide.**
