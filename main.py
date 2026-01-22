import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Import custom modules
from utils.document_processor import DocumentProcessor
from utils.ai_analyzer import AIAnalyzer
from utils.feedback_manager import FeedbackManager

# Page config
st.set_page_config(
    page_title="Civic AI Policy Bridge",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .feedback-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #28a745;
    }
    
    .concern-item {
        background: #fff5f5;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'document_text' not in st.session_state:
        st.session_state.document_text = ""
    if 'simplified_text' not in st.session_state:
        st.session_state.simplified_text = ""
    if 'demographic_analysis' not in st.session_state:
        st.session_state.demographic_analysis = {}
    if 'feedback_data' not in st.session_state:
        st.session_state.feedback_data = []
    if 'insights' not in st.session_state:
        st.session_state.insights = {}

def main():
    initialize_session_state()
    
    # Initialize components
    doc_processor = DocumentProcessor()
    ai_analyzer = AIAnalyzer()
    feedback_manager = FeedbackManager()
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ Civic AI Policy Bridge</h1>
        <p>Transforming complex policies into accessible insights for democratic participation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["📄 Policy Upload", "🔍 Analysis Dashboard", "💬 Citizen Feedback", "📊 Insights Report"]
    )
    
    if page == "📄 Policy Upload":
        policy_upload_page(doc_processor, ai_analyzer)
    elif page == "🔍 Analysis Dashboard":
        analysis_dashboard_page()
    elif page == "💬 Citizen Feedback":
        feedback_page(feedback_manager, ai_analyzer)
    elif page == "📊 Insights Report":
        insights_page()

def policy_upload_page(doc_processor, ai_analyzer):
    st.header("📄 Policy Document Upload & Analysis")
    
    # API Key input
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    if api_key:
        ai_analyzer.set_api_key(api_key)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Document")
        
        # File upload options
        upload_option = st.radio(
            "Choose input method:",
            ["Upload File", "Paste Text"]
        )
        
        document_text = ""
        
        if upload_option == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload policy document",
                type=['pdf', 'docx', 'txt'],
                help="Supported formats: PDF, DOCX, TXT"
            )
            
            if uploaded_file:
                with st.spinner("Processing document..."):
                    document_text = doc_processor.extract_text(uploaded_file)
                    st.session_state.document_text = document_text
        else:
            document_text = st.text_area(
                "Paste policy text here:",
                height=200,
                placeholder="Enter the policy document text..."
            )
            if document_text:
                st.session_state.document_text = document_text
        
        # Display original text
        if st.session_state.document_text:
            st.subheader("Original Document")
            st.text_area("Document Content", st.session_state.document_text, height=300, disabled=True)
    
    with col2:
        if st.session_state.document_text and api_key:
            st.subheader("AI Analysis Options")
            
            # Reading level selection
            reading_level = st.selectbox(
                "Choose reading level:",
                ["Middle School", "High School", "College", "Professional"]
            )
            
            # Language selection
            language = st.selectbox(
                "Select language:",
                ["English", "Hindi", "Spanish", "French", "German"]
            )
            
            # Analyze button
            if st.button("🔍 Analyze Document", type="primary"):
                with st.spinner("AI is analyzing the document..."):
                    # Simplify text
                    simplified = ai_analyzer.simplify_text(
                        st.session_state.document_text, 
                        reading_level.lower().replace(" ", "_")
                    )
                    st.session_state.simplified_text = simplified
                    
                    # Generate demographic analysis
                    demographics = ai_analyzer.analyze_demographic_impact(st.session_state.document_text)
                    st.session_state.demographic_analysis = demographics
                    
                    st.success("Analysis complete!")
                    st.rerun()
        
        # Display simplified text
        if st.session_state.simplified_text:
            st.subheader("Simplified Version")
            st.markdown(st.session_state.simplified_text)
            
            # Reading statistics
            st.subheader("📈 Readability Metrics")
            doc_stats = doc_processor.get_reading_stats(st.session_state.document_text)
            simple_stats = doc_processor.get_reading_stats(st.session_state.simplified_text)
            
            col_orig, col_simp = st.columns(2)
            with col_orig:
                st.metric("Original Reading Level", f"Grade {doc_stats['grade_level']}")
                st.metric("Word Count", doc_stats['word_count'])
            with col_simp:
                st.metric("Simplified Reading Level", f"Grade {simple_stats['grade_level']}")
                st.metric("Word Count", simple_stats['word_count'])

def analysis_dashboard_page():
    st.header("🔍 Policy Analysis Dashboard")
    
    if not st.session_state.demographic_analysis:
        st.warning("Please upload and analyze a document first!")
        return
    
    # Demographic impact analysis
    st.subheader("👥 Demographic Impact Analysis")
    
    demographics = st.session_state.demographic_analysis
    
    # Create columns for each demographic
    demo_names = list(demographics.keys())
    if len(demo_names) >= 3:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
    else:
        cols = st.columns(len(demo_names))
    
    for i, (demo, analysis) in enumerate(demographics.items()):
        with cols[i % len(cols)]:
            st.markdown(f"""
            <div class="metric-card">
                <h4>{demo.title()}</h4>
                <p><strong>Impact:</strong> {analysis.get('impact', 'N/A')}</p>
                <p><strong>Concerns:</strong> {analysis.get('concerns', 'None identified')}</p>
                <p><strong>Benefits:</strong> {analysis.get('benefits', 'None identified')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Key provisions breakdown
    st.subheader("📋 Key Provisions")
    if 'key_provisions' in demographics:
        for provision in demographics.get('key_provisions', []):
            st.markdown(f"• {provision}")

def feedback_page(feedback_manager, ai_analyzer):
    st.header("💬 Citizen Feedback Collection")
    
    if not st.session_state.simplified_text:
        st.warning("Please analyze a document first to collect feedback!")
        return
    
    # Display simplified policy for context
    with st.expander("📄 View Policy Summary"):
        st.markdown(st.session_state.simplified_text)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Submit Your Feedback")
        
        # Feedback form
        with st.form("feedback_form"):
            name = st.text_input("Name (optional)")
            demographic = st.selectbox(
                "I represent:",
                ["General Citizen", "Student", "Farmer", "Business Owner", 
                 "Senior Citizen", "Parent", "Teacher", "Healthcare Worker"]
            )
            
            feedback_type = st.radio(
                "Type of feedback:",
                ["Support", "Concern", "Suggestion", "Question"]
            )
            
            feedback_text = st.text_area(
                "Your feedback:",
                height=150,
                placeholder="Share your thoughts on this policy..."
            )
            
            submitted = st.form_submit_button("Submit Feedback", type="primary")
            
            if submitted and feedback_text:
                # Process feedback with AI
                processed_feedback = ai_analyzer.process_feedback(feedback_text, feedback_type)
                
                feedback_entry = {
                    'timestamp': datetime.now(),
                    'name': name or 'Anonymous',
                    'demographic': demographic,
                    'type': feedback_type,
                    'text': feedback_text,
                    'sentiment': processed_feedback.get('sentiment', 'neutral'),
                    'key_points': processed_feedback.get('key_points', []),
                    'category': processed_feedback.get('category', 'general')
                }
                
                st.session_state.feedback_data.append(feedback_entry)
                st.success("Thank you for your feedback!")
                st.rerun()
    
    with col2:
        st.subheader("📊 Live Feedback Stats")
        
        if st.session_state.feedback_data:
            df = pd.DataFrame(st.session_state.feedback_data)
            
            # Feedback type distribution
            type_counts = df['type'].value_counts()
            fig_pie = px.pie(values=type_counts.values, names=type_counts.index, 
                            title="Feedback Types")
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Sentiment distribution
            sentiment_counts = df['sentiment'].value_counts()
            colors = {'positive': 'green', 'negative': 'red', 'neutral': 'blue'}
            fig_bar = px.bar(x=sentiment_counts.index, y=sentiment_counts.values,
                           title="Sentiment Analysis",
                           color=sentiment_counts.index,
                           color_discrete_map=colors)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No feedback received yet.")
    
    # Display recent feedback
    if st.session_state.feedback_data:
        st.subheader("Recent Feedback")
        
        for feedback in st.session_state.feedback_data[-5:]:  # Show last 5
            sentiment_class = "feedback-item" if feedback['sentiment'] == 'positive' else "concern-item"
            st.markdown(f"""
            <div class="{sentiment_class}">
                <strong>{feedback['name']} ({feedback['demographic']})</strong> - {feedback['type']}<br>
                <em>{feedback['text']}</em><br>
                <small>Sentiment: {feedback['sentiment']} | {feedback['timestamp'].strftime('%Y-%m-%d %H:%M')}</small>
            </div>
            """, unsafe_allow_html=True)

def insights_page():
    st.header("📊 Policy Insights Report")
    
    if not st.session_state.feedback_data:
        st.warning("No feedback data available for insights!")
        return
    
    df = pd.DataFrame(st.session_state.feedback_data)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Feedback", len(df))
    with col2:
        support_pct = (df['sentiment'] == 'positive').mean() * 100
        st.metric("Support Rate", f"{support_pct:.1f}%")
    with col3:
        concern_pct = (df['sentiment'] == 'negative').mean() * 100
        st.metric("Concern Rate", f"{concern_pct:.1f}%")
    with col4:
        st.metric("Demographics Represented", df['demographic'].nunique())
    
    # Detailed analysis
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Feedback Trends")
        
        # Timeline chart
        df['hour'] = df['timestamp'].dt.hour
        hourly_counts = df.groupby('hour').size()
        fig_timeline = px.line(x=hourly_counts.index, y=hourly_counts.values,
                              title="Feedback Submission Timeline")
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Demographic breakdown
        demo_sentiment = df.groupby(['demographic', 'sentiment']).size().unstack(fill_value=0)
        fig_demo = px.bar(demo_sentiment, title="Sentiment by Demographic")
        st.plotly_chart(fig_demo, use_container_width=True)
    
    with col2:
        st.subheader("🔑 Key Insights")
        
        # Top concerns
        concerns = df[df['sentiment'] == 'negative']['text'].tolist()
        if concerns:
            st.markdown("**Top Concerns:**")
            for concern in concerns[:3]:
                st.markdown(f"• {concern[:100]}...")
        
        # Top support points
        support = df[df['sentiment'] == 'positive']['text'].tolist()
        if support:
            st.markdown("**Strong Support For:**")
            for point in support[:3]:
                st.markdown(f"• {point[:100]}...")
    
    # Actionable recommendations
    st.subheader("💡 AI-Generated Recommendations")
    
    if len(df) > 0:
        # Generate recommendations based on feedback patterns
        recommendations = generate_recommendations(df)
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}.** {rec}")
    
    # Export functionality
    st.subheader("📥 Export Data")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Download Feedback CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"policy_feedback_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Generate Report"):
            report = generate_summary_report(df)
            st.download_button(
                label="Download Report",
                data=report,
                file_name=f"policy_insights_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

def generate_recommendations(df):
    """Generate actionable recommendations based on feedback analysis"""
    recommendations = []
    
    # Analyze sentiment distribution
    negative_pct = (df['sentiment'] == 'negative').mean()
    if negative_pct > 0.3:
        recommendations.append("Consider addressing the high level of concerns (30%+) before policy implementation.")
    
    # Analyze demographic concerns
    demo_concerns = df[df['sentiment'] == 'negative']['demographic'].value_counts()
    if len(demo_concerns) > 0:
        top_concerned = demo_concerns.index[0]
        recommendations.append(f"Focus stakeholder engagement on {top_concerned} group, which shows highest concern levels.")
    
    # Analyze feedback types
    suggestion_count = (df['type'] == 'Suggestion').sum()
    if suggestion_count > 0:
        recommendations.append(f"Review {suggestion_count} citizen suggestions for potential policy improvements.")
    
    return recommendations

def generate_summary_report(df):
    """Generate a comprehensive summary report"""
    total_feedback = len(df)
    support_rate = (df['sentiment'] == 'positive').mean() * 100
    concern_rate = (df['sentiment'] == 'negative').mean() * 100
    
    report = f"""
POLICY FEEDBACK ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY STATISTICS
==================
Total Feedback Received: {total_feedback}
Support Rate: {support_rate:.1f}%
Concern Rate: {concern_rate:.1f}%
Demographics Represented: {df['demographic'].nunique()}

DEMOGRAPHIC BREAKDOWN
====================
{df['demographic'].value_counts().to_string()}

SENTIMENT ANALYSIS
==================
{df['sentiment'].value_counts().to_string()}

FEEDBACK TYPES
==============
{df['type'].value_counts().to_string()}

TOP CONCERNS
============
"""
    
    concerns = df[df['sentiment'] == 'negative']['text'].head(5).tolist()
    for i, concern in enumerate(concerns, 1):
        report += f"{i}. {concern}\n"
    
    report += "\nTOP SUPPORT POINTS\n================\n"
    
    support = df[df['sentiment'] == 'positive']['text'].head(5).tolist()
    for i, point in enumerate(support, 1):
        report += f"{i}. {point}\n"
    
    return report

if __name__ == "__main__":
    main()
