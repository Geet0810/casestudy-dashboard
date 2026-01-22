
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
