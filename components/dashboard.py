import streamlit as st
from utils.visualization import (
    create_feedback_trend_chart,
    create_priority_distribution,
    create_tag_distribution
)

def render_dashboard(feedback_data):
    st.header("Feedback Dashboard")
    
    # Create metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Feedback", len(feedback_data))
    
    with col2:
        high_priority = sum(1 for item in feedback_data if item['priority'] >= 4)
        st.metric("High Priority Items", high_priority)
    
    with col3:
        safety_concerns = sum(1 for item in feedback_data if item['safety_flag'])
        st.metric("Safety Concerns", safety_concerns)
    
    # Display charts with unique keys
    st.plotly_chart(create_feedback_trend_chart(feedback_data), key="trend_chart")
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_priority_distribution(feedback_data), key="priority_chart")
    
    with col2:
        st.plotly_chart(create_tag_distribution(feedback_data), key="tag_chart")
