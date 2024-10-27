import streamlit as st
from utils.database import Database
from components.dashboard import render_dashboard
from components.feedback_form import render_feedback_form
from components.filters import apply_filters
from components.summary_dashboard import render_summary_dashboard

st.set_page_config(
    page_title="OpenAI Feedback System",
    page_icon="🤖",
    layout="wide"
)

def main():
    st.title("OpenAI Internal Feedback System")
    
    try:
        # Initialize database connection
        db = Database()
        
        # Sidebar navigation
        page = st.sidebar.radio("Navigation", ["Dashboard", "Executive Summary", "Submit Feedback"])
        
        # Get all feedback data
        feedback_data = db.get_all_feedback()
        
        # Apply filters
        filtered_feedback = apply_filters(feedback_data)
        
        if page == "Dashboard":
            render_dashboard(filtered_feedback)
            
            # Display filtered feedback items
            st.header("Feedback Items")
            for item in filtered_feedback:
                with st.expander(f"{item['title']} (Priority: {item['priority']})"):
                    st.write(item['description'])
                    st.write(f"Tags: {', '.join(item['tags'])}")
                    if st.button(f"Upvote ({item['upvotes']})", key=f"upvote_{item['id']}"):
                        db.upvote_feedback(item['id'])
                        st.rerun()
                        
        elif page == "Executive Summary":
            render_summary_dashboard()
            
        else:
            render_feedback_form()
            
    except Exception as e:
        st.error("Application Error")
        st.error(str(e))
        print(f"Detailed error: {str(e)}")
        st.stop()

if __name__ == "__main__":
    main()
