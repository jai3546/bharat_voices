# 🚀 Deployment Guide for Bharat Voices

This guide covers different deployment options for the Bharat Voices platform.

## 📋 Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)
- Google Cloud account (for Google Sheets integration)
- Hugging Face account (optional, for better AI features)

## 🏠 Local Development

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd bharat-voices
```

2. **Run the setup script**
```bash
python setup.py
```

3. **Start the application**
```bash
python run.py
```

The application will be available at `http://localhost:8501`

### Manual Setup

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Set up Google Sheets (recommended)**
   - Create a Google Cloud Project
   - Enable Google Sheets API
   - Create a Service Account
   - Download credentials as `credentials.json`
   - Create a Google Sheet and share with service account email

4. **Run the application**
```bash
streamlit run main.py
```

## ☁️ Cloud Deployment

### Streamlit Cloud (Recommended)

1. **Fork the repository** on GitHub

2. **Connect to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Deploy from your forked repository

3. **Configure secrets**
   In Streamlit Cloud settings, add these secrets:
   ```toml
   [secrets]
   GOOGLE_CREDENTIALS_PATH = "credentials.json"
   HUGGINGFACE_API_KEY = "your-hf-api-key"
   COLLECTION_TARGET = "1000"
   ```

4. **Upload credentials**
   - Upload your `credentials.json` file to the secrets

### Heroku Deployment

1. **Create Heroku app**
```bash
heroku create your-app-name
```

2. **Set environment variables**
```bash
heroku config:set GOOGLE_CREDENTIALS_PATH=credentials.json
heroku config:set COLLECTION_TARGET=1000
```

3. **Create Procfile**
```
web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
```

4. **Deploy**
```bash
git push heroku main
```

### Google Cloud Platform

1. **Create App Engine app**
```bash
gcloud app create
```

2. **Create app.yaml**
```yaml
runtime: python39

env_variables:
  GOOGLE_CREDENTIALS_PATH: "credentials.json"
  COLLECTION_TARGET: "1000"

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

3. **Deploy**
```bash
gcloud app deploy
```

### AWS EC2

1. **Launch EC2 instance** (Ubuntu 20.04 LTS)

2. **Install dependencies**
```bash
sudo apt update
sudo apt install python3-pip nginx
pip3 install -r requirements.txt
```

3. **Configure nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

4. **Run with systemd**
Create `/etc/systemd/system/bharatvoices.service`:
```ini
[Unit]
Description=Bharat Voices
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/bharat-voices
ExecStart=/usr/bin/python3 -m streamlit run main.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DEBUG` | Enable debug mode | No | `False` |
| `GOOGLE_CREDENTIALS_PATH` | Path to Google credentials | Yes | `credentials.json` |
| `HUGGINGFACE_API_KEY` | Hugging Face API key | No | - |
| `COLLECTION_TARGET` | Target number of stories | No | `1000` |
| `WHISPER_MODEL` | Whisper model size | No | `base` |

### Google Sheets Setup

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable Google Sheets API

2. **Create Service Account**
   - Go to IAM & Admin > Service Accounts
   - Create new service account
   - Download JSON key file
   - Rename to `credentials.json`

3. **Create Google Sheet**
   - Create a new Google Sheet
   - Share with service account email (found in credentials.json)
   - Give "Editor" permissions

### Hugging Face Setup (Optional)

1. **Create account** at [huggingface.co](https://huggingface.co)
2. **Generate API token** in settings
3. **Add to environment** as `HUGGINGFACE_API_KEY`

## 🔒 Security Considerations

### Production Deployment

1. **Use HTTPS**
   - Configure SSL certificates
   - Use reverse proxy (nginx/Apache)

2. **Secure credentials**
   - Use environment variables
   - Don't commit credentials to git
   - Use cloud secret managers

3. **Rate limiting**
   - Implement API rate limits
   - Use CDN for static assets

4. **Monitoring**
   - Set up application monitoring
   - Configure error tracking
   - Monitor resource usage

### Data Privacy

1. **GDPR Compliance**
   - Implement data export
   - Allow data deletion
   - Clear privacy policy

2. **Content Moderation**
   - Review submitted content
   - Implement reporting system
   - Content filtering

## 📊 Monitoring & Analytics

### Application Monitoring

1. **Streamlit metrics**
   - Monitor app performance
   - Track user sessions
   - Error logging

2. **Database monitoring**
   - Google Sheets API usage
   - Response times
   - Error rates

### User Analytics

1. **Usage patterns**
   - Popular languages
   - Content categories
   - User engagement

2. **Growth metrics**
   - New submissions
   - User retention
   - Geographic distribution

## 🔄 Backup & Recovery

### Data Backup

1. **Google Sheets**
   - Automatic versioning
   - Export to CSV regularly
   - Multiple sheet backup

2. **Application backup**
   - Code repository backup
   - Configuration backup
   - User data export

### Disaster Recovery

1. **Service restoration**
   - Documented deployment process
   - Infrastructure as code
   - Automated deployments

2. **Data recovery**
   - Point-in-time recovery
   - Data validation
   - User notification

## 🚀 Performance Optimization

### Application Performance

1. **Caching**
   - Enable Streamlit caching
   - Cache API responses
   - Static asset caching

2. **Resource optimization**
   - Optimize images
   - Minimize API calls
   - Lazy loading

### Scalability

1. **Horizontal scaling**
   - Load balancing
   - Multiple instances
   - Database sharding

2. **Vertical scaling**
   - Increase server resources
   - Optimize memory usage
   - CPU optimization

## 📞 Support & Maintenance

### Regular Maintenance

1. **Updates**
   - Security patches
   - Dependency updates
   - Feature updates

2. **Monitoring**
   - Performance monitoring
   - Error tracking
   - User feedback

### Troubleshooting

1. **Common issues**
   - Import errors: Check dependencies
   - API errors: Verify credentials
   - Performance: Check resource usage

2. **Logs**
   - Application logs
   - Error logs
   - Access logs

## 📈 Scaling Considerations

### Traffic Growth

1. **Database scaling**
   - Consider migration to dedicated database
   - Implement caching layer
   - Optimize queries

2. **Application scaling**
   - Containerization (Docker)
   - Kubernetes deployment
   - Microservices architecture

### Feature Expansion

1. **API development**
   - REST API for mobile apps
   - GraphQL for complex queries
   - Webhook integrations

2. **Advanced features**
   - Real-time collaboration
   - Advanced search
   - Machine learning insights
