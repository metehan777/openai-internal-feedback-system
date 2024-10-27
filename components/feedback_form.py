import streamlit as st
from utils.nlp import SafetyAnalyzer
from utils.database import Database
import os

def render_feedback_form():
    st.header("Submit Feedback")
    
    # Form inputs
    title = st.text_input("Feedback Title")
    description = st.text_area("Detailed Description")
    priority = st.slider("Priority Level (Your Assessment)", 1, 5, 3)
    
    # Tag selection
    available_tags = ['safety', 'alignment', 'performance', 'ethics', 'technical']
    selected_tags = st.multiselect("Tags", available_tags)
    
    if st.button("Submit Feedback"):
        if not title or not description:
            st.error("Please fill in all required fields")
            return
            
        try:
            print(f"Starting feedback submission process for: {title}")
            print("Database connection parameters available:", all(
                key in os.environ for key in ['PGHOST', 'PGDATABASE', 'PGUSER', 'PGPASSWORD', 'PGPORT']
            ))
            
            print("Initializing components...")
            safety_analyzer = SafetyAnalyzer()
            db = Database()
            
            print("Getting AI analysis...")
            ai_analysis = safety_analyzer.get_ai_safety_score(title, description)
            print("AI analysis complete:", bool(ai_analysis))
            
            print("Saving to database...")
            feedback_id = db.add_feedback(
                title=title,
                description=description,
                priority=priority,
                tags=selected_tags,
                ai_analysis=ai_analysis
            )
            print(f"Database save result: {feedback_id}")
            
            if not feedback_id:
                st.error("Failed to save feedback")
                return
                
            st.success("Feedback submitted successfully!")
            
            # Show AI analysis results
            st.subheader("AI Safety Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Your Priority Score", priority)
                st.write("Safety Category:", ai_analysis['safety_category'])
                
            with col2:
                st.metric("AI Priority Score", ai_analysis['priority_score'])
                if ai_analysis['is_safety_concern']:
                    st.warning("⚠️ Safety concerns detected!")
            
            st.write("AI Reasoning:", ai_analysis['reasoning'])
            
            if ai_analysis['key_concerns']:
                st.write("Key Safety Concerns:")
                for concern in ai_analysis['key_concerns']:
                    st.write(f"• {concern}")
                    
        except Exception as e:
            print(f"Detailed error in feedback submission: {str(e)}")
            st.error(f"Error submitting feedback: {str(e)}")
            return
