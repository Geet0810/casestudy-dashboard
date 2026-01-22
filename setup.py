#!/usr/bin/env python3
"""
Setup script for Civic AI Policy Bridge
"""

import os
import sys
import subprocess

def create_directory_structure():
    """Create the required directory structure"""
    directories = [
        'utils',
        'data',
        'static',
        'tests'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
    
    # Create __init__.py files
    init_files = [
        'utils/__init__.py',
    ]
    
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Init file\n")
            print(f"Created: {init_file}")

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Error installing packages. Please install manually:")
        print("pip install -r requirements.txt")

def download_nltk_data():
    """Download required NLTK data"""
    print("Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        print("✅ NLTK data downloaded successfully!")
    except ImportError:
        print("⚠️  NLTK not installed yet. Will download data on first run.")

def create_sample_policy():
    """Create a sample policy document for testing"""
    sample_policy = """
DIGITAL PRIVACY PROTECTION ACT 2025

SECTION 1: PURPOSE AND SCOPE
This Act establishes comprehensive regulations for the protection of personal digital information and privacy rights of citizens in the digital age.

SECTION 2: DEFINITIONS
2.1 "Personal Data" means any information relating to an identified or identifiable natural person.
2.2 "Data Controller" means the entity which determines the purposes and means of processing personal data.
2.3 "Data Subject" means the natural person whose personal data is being processed.

SECTION 3: RIGHTS OF DATA SUBJECTS
3.1 Right to Information: Data subjects have the right to know what personal data is being collected and how it is used.
3.2 Right to Access: Data subjects can request access to their personal data held by organizations.
3.3 Right to Rectification: Data subjects can request correction of inaccurate personal data.
3.4 Right to Erasure: Data subjects can request deletion of their personal data under certain circumstances.
3.5 Right to Data Portability: Data subjects can request their data in a machine-readable format.

SECTION 4: OBLIGATIONS OF DATA CONTROLLERS
4.1 Lawful Basis: Personal data shall only be processed with valid legal basis and consent.
4.2 Data Minimization: Only data necessary for the specified purpose shall be collected.
4.3 Accuracy: Data controllers must ensure personal data is accurate and up-to-date.
4.4 Storage Limitation: Personal data shall not be kept longer than necessary.
4.5 Security: Appropriate technical and organizational measures must be implemented.

SECTION 5: ENFORCEMENT AND PENALTIES
5.1 The Data Protection Authority is established as the supervisory body.
5.2 Violations may result in fines up to 4% of annual global turnover or $20 million, whichever is higher.
5.3 Repeated violations may result in suspension of data processing activities.

SECTION 6: IMPLEMENTATION
This Act shall come into effect 180 days from the date of publication, allowing organizations time to ensure compliance.

SECTION 7: EXEMPTIONS
7.1 National security and law enforcement activities are exempt under specific conditions.
7.2 Household activities and purely personal use are exempt from most provisions.
"""
    
    # Save to data directory
    with open('data/sample_policy.txt', 'w') as f:
        f.write(sample_policy)
    print("✅ Sample policy document created: data/sample_policy.txt")

def create_config_template():
    """Create configuration template"""
    config_content = """
# Civic AI Policy Bridge Configuration

# OpenAI Configuration
OPENAI_API_KEY = "your-api-key-here"
OPENAI_MODEL = "gpt-4o-mini"

# App Configuration  
APP_TITLE = "Civic AI Policy Bridge"
MAX_FILE_SIZE = 10  # MB
SUPPORTED_LANGUAGES = ["English", "Hindi", "Spanish", "French", "German"]

# Reading Levels
READING_LEVELS = ["Middle School", "High School", "College", "Professional"]

# Demographics
DEMOGRAPHICS = [
    "General Citizen",
    "Student", 
    "Farmer",
    "Business Owner",
    "Senior Citizen",
    "Parent",
    "Teacher",
    "Healthcare Worker"
]

# Feedback Types
FEEDBACK_TYPES = ["Support", "Concern", "Suggestion", "Question"]
"""
    
    with open('config.py', 'w') as f:
        f.write(config_content)
    print("✅ Configuration template created: config.py")

def create_readme():
    """Create README file"""
    readme_content = """
# 🏛️ Civic AI Policy Bridge

An AI-powered platform that translates complex policy documents into accessible language and collects structured citizen feedback for policymakers.

## Features

- 📄 **Document Processing**: Upload PDF, DOCX, or text policy documents
- 🧠 **AI Simplification**: Convert complex legal language to plain English
- 👥 **Demographic Analysis**: Understand policy impact on different groups  
- 💬 **Feedback Collection**: Gather and analyze citizen opinions
- 📊 **Real-time Dashboard**: Live insights and sentiment analysis
- 📈 **Analytics Report**: Comprehensive feedback analysis

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Setup**:
   ```bash
   python setup.py
   ```

3. **Start the Application**:
   ```bash
   streamlit run main.py
   ```

4. **Open Browser**: Navigate to `http://localhost:8501`

## Configuration

1. Get your OpenAI API key from https://platform.openai.com
2. Enter the API key in the application when prompted
3. Upload a policy document or use the sample document provided

## Project Structure

```
civic-ai-policy-bridge/
├── main.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── setup.py               # Setup script
├── config.py              # Configuration settings
├── utils/                 # Utility modules
│   ├── document_processor.py  # Document handling
│   ├── ai_analyzer.py         # AI analysis
│   └── feedback_manager.py    # Feedback management
├── data/                  # Data storage
│   └── sample_policy.txt     # Sample policy document
└── tests/                 # Test files

```

## Usage Guide

### 1. Upload Policy Document
- Navigate to "📄 Policy Upload" 
- Enter your OpenAI API key
- Upload a document or paste text
- Select reading level and language
- Click "Analyze Document"

### 2. View Analysis
- Go to "🔍 Analysis Dashboard"
- Review simplified text and demographic impact analysis
- Check readability improvements

### 3. Collect Feedback  
- Visit "💬 Citizen Feedback"
- Citizens can submit feedback with their demographic info
- Real-time sentiment analysis and categorization

### 4. Generate Insights
- Check "📊 Insights Report"
- View aggregated feedback analysis
- Download CSV data or summary reports

## API Requirements

- OpenAI API key (GPT-4 or GPT-3.5)
- Recommended: GPT-4o-mini for cost efficiency

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use for hackathons and civic projects!

## Support

For questions or issues:
- Check the troubleshooting section below
- Create an issue on GitHub
- Contact the development team

## Troubleshooting

**API Key Issues**: Make sure your OpenAI API key is valid and has sufficient credits

**File Upload Problems**: Ensure files are under 10MB and in supported formats (PDF, DOCX, TXT)

**Performance Issues**: For large documents, consider breaking them into smaller sections

**NLTK Errors**: Run `python -c "import nltk; nltk.download('punkt')"` if you see NLTK-related errors
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    print("✅ README.md created")

def main():
    """Main setup function"""
    print("🏛️  Setting up Civic AI Policy Bridge...")
    print("=" * 50)
    
    # Create directory structure
    create_directory_structure()
    
    # Install requirements
    install_requirements()
    
    # Download NLTK data
    download_nltk_data()
    
    # Create sample files
    create_sample_policy()
    create_config_template()
    create_readme()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n🚀 To start the application, run:")
    print("   streamlit run main.py")
    print("\n📝 Don't forget to:")
    print("   1. Get your OpenAI API key from https://platform.openai.com")
    print("   2. Enter the API key in the application")
    print("   3. Try uploading the sample policy document!")

if __name__ == "__main__":
    main()
