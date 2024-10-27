import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import pandas as pd
from openai import OpenAI

class SummaryGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    def generate_metrics_summary(self, feedback_data: List[Dict]) -> Dict[str, Any]:
        """Generate key metrics from feedback data."""
        if not feedback_data:
            return {
                'total_feedback': 0,
                'high_priority': 0,
                'safety_concerns': 0,
                'avg_priority': 0
            }

        df = pd.DataFrame(feedback_data)
        
        # Calculate time-based metrics
        df['created_at'] = pd.to_datetime(df['created_at'])
        last_week = datetime.now() - timedelta(days=7)
        recent_df = df[df['created_at'] >= last_week]

        return {
            'total_feedback': len(df),
            'recent_feedback': len(recent_df),
            'high_priority': len(df[df['priority'] >= 4]),
            'safety_concerns': len(df[df['safety_flag'] == True]),
            'avg_priority': round(df['priority'].mean(), 2),
            'top_tags': df['tags'].explode().value_counts().head(5).to_dict() if 'tags' in df else {}
        }

    def generate_executive_summary(self, feedback_data: List[Dict]) -> Dict[str, Any]:
        """Generate an AI-powered executive summary of feedback."""
        metrics = self.generate_metrics_summary(feedback_data)
        
        # Prepare data for AI analysis
        high_priority_items = [
            f"{item['title']}: {item['description'][:200]}..."
            for item in feedback_data
            if item['priority'] >= 4
        ]
        
        safety_items = [
            f"{item['title']}: {item['description'][:200]}..."
            for item in feedback_data
            if item.get('safety_flag', False)
        ]

        prompt = f"""Generate an executive summary of AI safety feedback data with the following structure:
Key Metrics:
- Total Feedback: {metrics['total_feedback']}
- Recent Feedback (7 days): {metrics['recent_feedback']}
- High Priority Items: {metrics['high_priority']}
- Safety Concerns: {metrics['safety_concerns']}
- Average Priority: {metrics['avg_priority']}

High Priority Feedback:
{', '.join(high_priority_items[:5]) if high_priority_items else 'None'}

Safety Concerns:
{', '.join(safety_items[:5]) if safety_items else 'None'}

Generate a JSON response with:
1. executive_summary (2-3 paragraphs highlighting key insights)
2. key_recommendations (list of 3-5 actionable items)
3. risk_assessment (brief assessment of identified safety risks)
4. focus_areas (list of 2-3 areas needing immediate attention)"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI safety expert analyzing feedback trends and generating executive summaries."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            ai_summary = eval(response.choices[0].message.content)
            return {
                **ai_summary,
                'metrics': metrics,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'error': f"Failed to generate AI summary: {str(e)}",
                'metrics': metrics,
                'generated_at': datetime.now().isoformat()
            }
