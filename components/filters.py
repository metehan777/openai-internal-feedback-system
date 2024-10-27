import streamlit as st
import pandas as pd

def apply_filters(feedback_data):
    st.sidebar.header("Filters")
    
    # Handle empty feedback data
    if not feedback_data:
        st.sidebar.warning("No feedback data available")
        return []
    
    try:
        # Convert to DataFrame for easier filtering
        df = pd.DataFrame(feedback_data)
        
        # Check for required columns
        required_columns = ['priority', 'tags', 'safety_flag']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.sidebar.error(f"Missing required columns: {', '.join(missing_columns)}")
            return feedback_data
        
        # Priority filter with default values
        unique_priorities = sorted(df['priority'].unique()) if not df.empty else [1, 2, 3, 4, 5]
        priority_filter = st.sidebar.multiselect(
            "Priority Level",
            options=unique_priorities,
            default=unique_priorities
        )
        
        # Safety concerns filter
        show_safety_only = st.sidebar.checkbox("Show Safety Concerns Only")
        
        # Tag filter
        all_tags = set([tag for tags in df['tags'] for tag in tags]) if not df.empty else set()
        selected_tags = st.sidebar.multiselect(
            "Tags",
            options=list(all_tags)
        )
        
        # Apply filters
        if not priority_filter:  # If no priorities selected, show all
            priority_filter = unique_priorities
            
        mask = df['priority'].isin(priority_filter)
        
        if show_safety_only:
            mask = mask & df['safety_flag']
            
        if selected_tags:
            mask = mask & df['tags'].apply(lambda x: any(tag in x for tag in selected_tags))
        
        return df[mask].to_dict('records')
        
    except Exception as e:
        st.sidebar.error(f"Error applying filters: {str(e)}")
        return feedback_data  # Return original data if filtering fails
