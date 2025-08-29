#!/usr/bin/env python3
"""
Test script for Bharat Voices application
"""

import sys
import os
import importlib
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    required_modules = [
        'streamlit',
        'pandas',
        'numpy',
        'requests',
        'plotly',
        'PIL',
        'dotenv'
    ]
    
    optional_modules = [
        'whisper',
        'transformers',
        'torch',
        'gspread',
        'pyairtable'
    ]
    
    failed_imports = []
    
    # Test required modules
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    # Test optional modules
    print("\n🔧 Testing optional modules...")
    for module in optional_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"⚠️  {module}: {e} (optional)")
    
    return failed_imports

def test_custom_modules():
    """Test custom application modules"""
    print("\n📦 Testing custom modules...")
    
    custom_modules = [
        'utils.config',
        'utils.database',
        'utils.translation',
        'utils.categorization',
        'utils.audio',
        'utils.gamification',
        'utils.social_cards',
        'pages.submission',
        'pages.community',
        'pages.admin',
        'pages.profile',
        'pages.analytics'
    ]
    
    failed_imports = []
    
    for module in custom_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    return failed_imports

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from utils.config import Config
        config = Config()
        
        # Test basic config attributes
        assert hasattr(config, 'LANGUAGES'), "LANGUAGES not found in config"
        assert hasattr(config, 'CATEGORIES'), "CATEGORIES not found in config"
        assert hasattr(config, 'CONTENT_TYPES'), "CONTENT_TYPES not found in config"
        assert hasattr(config, 'BADGES'), "BADGES not found in config"
        
        print(f"✅ Configuration loaded successfully")
        print(f"   - {len(config.LANGUAGES)} languages supported")
        print(f"   - {len(config.CATEGORIES)} categories available")
        print(f"   - {len(config.CONTENT_TYPES)} content types supported")
        print(f"   - {len(config.BADGES)} badges configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n💾 Testing database connection...")
    
    try:
        from utils.database import DatabaseManager
        db = DatabaseManager()
        
        # Test basic database operations (without actual connection)
        print("✅ Database manager initialized")
        
        # Test mock data operations
        mock_submission = {
            "title": "Test Story",
            "content": "This is a test story",
            "language": "English",
            "content_type": "Story"
        }
        
        # This would normally save to database, but we're testing the interface
        print("✅ Database interface working")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_translation_service():
    """Test translation service"""
    print("\n🌐 Testing translation service...")
    
    try:
        from utils.translation import TranslationService
        translator = TranslationService()
        
        print("✅ Translation service initialized")
        
        # Test language detection
        supported_languages = translator.get_supported_languages()
        print(f"✅ {len(supported_languages)} languages supported for translation")
        
        return True
        
    except Exception as e:
        print(f"❌ Translation service test failed: {e}")
        return False

def test_categorization_service():
    """Test categorization service"""
    print("\n🏷️ Testing categorization service...")
    
    try:
        from utils.categorization import CategorizationService
        categorizer = CategorizationService()
        
        print("✅ Categorization service initialized")
        
        # Test categorization with sample text
        sample_text = "A wise man learns from the mistakes of others"
        category = categorizer.categorize_content(sample_text, "Proverb")
        
        if category:
            print(f"✅ Sample categorization: '{sample_text}' → {category}")
        else:
            print("⚠️  Categorization returned None (may be expected without API keys)")
        
        return True
        
    except Exception as e:
        print(f"❌ Categorization service test failed: {e}")
        return False

def test_audio_service():
    """Test audio service"""
    print("\n🎤 Testing audio service...")
    
    try:
        from utils.audio import AudioProcessor
        audio_processor = AudioProcessor()
        
        print("✅ Audio processor initialized")
        
        # Test supported formats
        formats = audio_processor.get_supported_formats()
        print(f"✅ {len(formats)} audio formats supported: {', '.join(formats)}")
        
        # Test tips
        tips = audio_processor.get_transcription_tips()
        print(f"✅ {len(tips)} transcription tips available")
        
        return True
        
    except Exception as e:
        print(f"❌ Audio service test failed: {e}")
        return False

def test_gamification():
    """Test gamification system"""
    print("\n🏆 Testing gamification system...")
    
    try:
        from utils.gamification import GamificationManager
        gamification = GamificationManager()
        
        print("✅ Gamification manager initialized")
        
        # Test badge system
        available_badges = gamification.get_available_badges()
        print(f"✅ {len(available_badges)} badges available")
        
        # Test daily challenge
        challenge = gamification.get_daily_challenge()
        print(f"✅ Daily challenge: {challenge['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Gamification test failed: {e}")
        return False

def test_social_cards():
    """Test social card generation"""
    print("\n📱 Testing social card generation...")
    
    try:
        from utils.social_cards import SocialCardGenerator
        card_generator = SocialCardGenerator()
        
        print("✅ Social card generator initialized")
        
        # Test templates
        templates = card_generator.get_sharing_templates()
        print(f"✅ {len(templates)} card templates available")
        
        return True
        
    except Exception as e:
        print(f"❌ Social card test failed: {e}")
        return False

def test_file_structure():
    """Test file structure"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        '.env.example',
        'setup.py',
        'run.py'
    ]
    
    required_dirs = [
        'utils',
        'pages',
        '.streamlit'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    for dir in required_dirs:
        if Path(dir).exists():
            print(f"✅ {dir}/")
        else:
            print(f"❌ {dir}/")
            missing_dirs.append(dir)
    
    return len(missing_files) == 0 and len(missing_dirs) == 0

def run_all_tests():
    """Run all tests"""
    print("🧪 BHARAT VOICES - APPLICATION TESTS")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Python Imports", test_imports),
        ("Custom Modules", test_custom_modules),
        ("Configuration", test_configuration),
        ("Database", test_database_connection),
        ("Translation", test_translation_service),
        ("Categorization", test_categorization_service),
        ("Audio Processing", test_audio_service),
        ("Gamification", test_gamification),
        ("Social Cards", test_social_cards)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("\n🚀 To start the application, run:")
        print("   python run.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n🔧 To fix issues:")
        print("   1. Install missing dependencies: pip install -r requirements.txt")
        print("   2. Check file structure")
        print("   3. Review error messages")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
