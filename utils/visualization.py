import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def create_feedback_trend_chart(feedback_data):
    if not feedback_data:
        fig = go.Figure()
        fig.add_annotation(text='No feedback data available', showarrow=False)
        return fig
    
    df = pd.DataFrame(feedback_data)
    if 'created_at' not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text='Created date information not available', showarrow=False)
        return fig
    
    df['created_at'] = pd.to_datetime(df['created_at'])
    daily_counts = df.groupby(df['created_at'].dt.date).size().reset_index()
    daily_counts.columns = ['date', 'count']
    
    fig = px.line(daily_counts, x='date', y='count',
                  title='Feedback Submissions Over Time')
    return fig

def create_priority_distribution(feedback_data):
    if not feedback_data:
        fig = go.Figure()
        fig.add_annotation(text='No feedback data available', showarrow=False)
        return fig
    
    df = pd.DataFrame(feedback_data)
    if 'priority' not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text='Priority information not available', showarrow=False)
        return fig
    
    priority_counts = df['priority'].value_counts().sort_index()
    
    fig = px.pie(values=priority_counts.values,
                 names=priority_counts.index,
                 title='Feedback by Priority Level')
    return fig

def create_tag_distribution(feedback_data):
    if not feedback_data:
        fig = go.Figure()
        fig.add_annotation(text='No feedback data available', showarrow=False)
        return fig
    
    df = pd.DataFrame(feedback_data)
    if 'tags' not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text='Tag information not available', showarrow=False)
        return fig
    
    # Handle empty tags
    if df.empty or all(not tags for tags in df['tags']):
        fig = go.Figure()
        fig.add_annotation(text='No tags available', showarrow=False)
        return fig
        
    all_tags = [tag for tags in df['tags'] for tag in tags if tags]  # Only include non-empty tag lists
    if not all_tags:  # If no tags after filtering
        fig = go.Figure()
        fig.add_annotation(text='No tags available', showarrow=False)
        return fig
        
    tag_counts = pd.Series(all_tags).value_counts()
    
    fig = px.bar(x=tag_counts.index, y=tag_counts.values,
                 title='Distribution of Feedback Tags')
    return fig
