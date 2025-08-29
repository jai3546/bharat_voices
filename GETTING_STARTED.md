# 🚀 Getting Started with Bharat Voices

Welcome to Bharat Voices! This guide will help you get the platform up and running quickly.

## ⚡ Quick Start (5 minutes)

### 1. Download and Setup
```bash
# Clone or download the project files
cd bharat-voices

# Run the automated setup
python setup.py

# Start the application
python run.py
```

### 2. Open Your Browser
Navigate to `http://localhost:8501` and start sharing cultural stories!

## 📋 What You Get

### ✨ Core Features
- **📝 Story Submission**: Text and voice input for cultural stories
- **🌐 Auto Translation**: AI translates stories to English
- **🏷️ Smart Categories**: AI organizes stories by themes
- **👥 Community Wall**: Browse and discover stories from around the world
- **🏆 Gamification**: Earn badges and track your contributions
- **📱 Social Sharing**: Create beautiful story cards for social media
- **📊 Analytics**: Track platform growth and engagement

### 🎯 Perfect For
- **Cultural Preservation**: Document traditional stories and wisdom
- **Language Learning**: Practice with authentic cultural content
- **Research**: Build linguistic and cultural corpora
- **Community Building**: Connect people through shared stories
- **Education**: Teach cultural diversity and heritage

## 🛠️ Setup Options

### Option 1: Basic Setup (No API Keys)
Works immediately with:
- ✅ Story submission and browsing
- ✅ Basic categorization
- ✅ Community features
- ✅ Social sharing
- ⚠️ Limited translation (free services only)

### Option 2: Enhanced Setup (With API Keys)
Get better features with:
- 🔑 **Hugging Face API**: Better translations and categorization
- 🔑 **Google Sheets**: Persistent data storage
- 🔑 **Airtable**: Advanced database features

## 🔧 Configuration

### Environment Variables
Edit `.env` file for customization:

```env
# Basic Settings
DEBUG=False
COLLECTION_TARGET=1000
WHISPER_MODEL=base

# Optional API Keys (for enhanced features)
HUGGINGFACE_API_KEY=your-key-here
GOOGLE_CREDENTIALS_PATH=credentials.json
AIRTABLE_API_KEY=your-key-here
```

### Google Sheets Integration
1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create Service Account credentials
4. Download as `credentials.json`
5. Create a Google Sheet and share with service account

## 📱 Using the Platform

### For Contributors
1. **Submit Stories**: Share proverbs, folk tales, and cultural wisdom
2. **Use Voice Input**: Record stories in your native language
3. **Add Context**: Provide cultural background for your stories
4. **Engage**: Like and share stories from others
5. **Earn Badges**: Complete challenges and unlock achievements

### For Researchers
1. **Browse Collections**: Explore stories by language and category
2. **Export Data**: Download stories in CSV or PDF format
3. **Analyze Trends**: Use the analytics dashboard
4. **Search Content**: Find specific themes or topics

### For Administrators
1. **Manage Content**: Review and feature stories
2. **Monitor Growth**: Track platform statistics
3. **Export Data**: Generate reports and backups
4. **Configure Settings**: Adjust platform parameters

## 🌍 Supported Languages

**60+ languages including:**
- **South Asian**: Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Nepali, Sinhala
- **East Asian**: Chinese, Japanese, Korean
- **Southeast Asian**: Thai, Vietnamese, Indonesian, Malay, Filipino
- **European**: English, Spanish, French, German, Italian, Portuguese, Russian, Polish, Dutch, Swedish
- **Middle Eastern**: Arabic, Persian, Turkish
- **And many more...**

## 🎯 Content Types

- **📜 Proverbs**: Traditional sayings with wisdom
- **📚 Folk Tales**: Traditional stories and legends
- **💭 Sayings**: Common expressions and phrases
- **📖 Short Stories**: Brief narrative pieces
- **🎵 Poems**: Verse and poetic expressions
- **🎶 Songs**: Traditional songs and lyrics
- **🧩 Riddles**: Traditional puzzles and brain teasers
- **⚡ Legends**: Mythical and historical tales

## 🏆 Achievement System

### Badges You Can Earn
- 🌱 **First Steps**: Submit your first story
- 🏛️ **Cultural Preserver**: Submit 10 stories
- 🧵 **Story Weaver**: Submit 25 stories
- 📚 **Wisdom Keeper**: Submit 50 stories
- 🌍 **Multilingual Master**: Submit in 3+ languages
- ❤️ **Community Favorite**: Receive 100+ likes
- 🔥 **Streak Master**: 7-day submission streak

### Daily Challenges
- Share a proverb from your culture
- Record a story using voice input
- Submit in a new language
- Engage with community stories
- Add cultural context to submissions

## 📊 Analytics Dashboard

Track platform growth with:
- **📈 Growth Metrics**: Daily submissions and user growth
- **🌍 Language Distribution**: Popular languages and trends
- **🏷️ Category Analysis**: Content themes and popularity
- **👥 Community Stats**: User engagement and activity
- **📍 Geographic Insights**: Story origins and distribution

## 🔒 Privacy & Data

- **Anonymous Submissions**: No login required
- **Data Ownership**: Contributors retain rights to their stories
- **Open Access**: Stories are publicly accessible for research
- **Export Rights**: Download your data anytime
- **GDPR Compliant**: Respects privacy regulations

## 🆘 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Install missing dependencies
pip install -r requirements.txt
```

**Translation Not Working**
- Add Hugging Face API key to `.env`
- Check internet connection
- Verify API key is valid

**Voice Input Issues**
- Allow microphone permissions in browser
- Check audio device settings
- Try different browsers (Chrome recommended)

**Database Errors**
- Verify Google Sheets credentials
- Check sheet permissions
- Ensure service account has access

### Getting Help
- 📖 Check the README.md for detailed documentation
- 🧪 Run `python test_app.py` to diagnose issues
- 🔧 Review error messages in the terminal
- 💬 Create an issue on GitHub for support

## 🚀 Deployment Options

### Local Development
- Run on your computer for testing
- Perfect for small communities
- No hosting costs

### Cloud Deployment
- **Streamlit Cloud**: Free hosting for public projects
- **Heroku**: Easy deployment with custom domains
- **Google Cloud**: Scalable enterprise deployment
- **AWS**: Full control and customization

## 🌟 Next Steps

1. **Start Contributing**: Share your first cultural story
2. **Invite Others**: Spread the word in your community
3. **Customize**: Adapt the platform for your specific needs
4. **Scale Up**: Deploy to the cloud for wider access
5. **Contribute**: Help improve the platform with feedback and code

## 📞 Support & Community

- **Documentation**: Comprehensive guides and tutorials
- **GitHub Issues**: Report bugs and request features
- **Community Forum**: Connect with other users
- **Email Support**: Direct contact for urgent issues

---

**Ready to preserve cultural wisdom? Start your journey with Bharat Voices today!**

🗣️ **"Every story shared is a piece of culture preserved for future generations."**
