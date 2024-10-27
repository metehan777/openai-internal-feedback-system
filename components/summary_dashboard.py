import streamlit as st
from datetime import datetime
from utils.summary import SummaryGenerator
from utils.database import Database

def render_summary_dashboard():
    st.header("Executive Summary Dashboard")
    
    try:
        # Initialize components
        db = Database()
        summary_gen = SummaryGenerator()
        
        # Get feedback data
        feedback_data = db.get_all_feedback()
        
        # Generate summary
        summary = summary_gen.generate_executive_summary(feedback_data)
        
        # Display generation time
        st.caption(f"Last updated: {datetime.fromisoformat(summary['generated_at']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Display metrics
        metrics = summary['metrics']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Feedback", metrics['total_feedback'])
        with col2:
            st.metric("Recent Feedback (7d)", metrics['recent_feedback'])
        with col3:
            st.metric("High Priority Items", metrics['high_priority'])
        with col4:
            st.metric("Safety Concerns", metrics['safety_concerns'])
            
        # Display executive summary
        st.subheader("Executive Summary")
        st.write(summary['executive_summary'])
        
        # Display recommendations and risk assessment
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Key Recommendations")
            for idx, rec in enumerate(summary['key_recommendations'], 1):
                st.write(f"{idx}. {rec}")
                
        with col2:
            st.subheader("Risk Assessment")
            st.write(summary['risk_assessment'])
            
        # Display focus areas
        st.subheader("Focus Areas")
        for idx, area in enumerate(summary['focus_areas'], 1):
            st.write(f"{idx}. {area}")
            
        # Display top tags if available
        if metrics['top_tags']:
            st.subheader("Top Tags")
            for tag, count in metrics['top_tags'].items():
                st.write(f"• {tag}: {count}")
                
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
