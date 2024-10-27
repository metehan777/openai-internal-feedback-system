import os
import openai
from typing import Dict, List, Any

class SafetyAnalyzer:
    def __init__(self):
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        self.safety_keywords = {
            'alignment': [
                'misaligned', 'value alignment', 'goal alignment',
                'ethical concerns', 'safety concerns'
            ],
            'risks': [
                'catastrophic risk', 'existential risk', 'safety risk',
                'unintended consequences', 'control problem'
            ],
            'behavior': [
                'unexpected behavior', 'harmful behavior', 'deceptive',
                'manipulation', 'adversarial'
            ]
        }

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Perform basic keyword-based safety analysis."""
        text = text.lower()
        flags = []
        
        for category, keywords in self.safety_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    flags.append({
                        'category': category,
                        'keyword': keyword
                    })
        
        return {
            'is_safety_concern': len(flags) > 0,
            'flags': flags
        }

    def get_ai_safety_score(self, title: str, description: str) -> Dict[str, Any]:
        """Get AI-powered safety analysis and priority score."""
        prompt = f"""Analyze this AI safety feedback and rate its priority (1-5):
Title: {title}
Description: {description}

Consider these aspects:
1. Immediate safety implications
2. Potential risks and consequences
3. Alignment with AI safety goals
4. Time sensitivity
5. Scale of impact

Provide a JSON response with:
1. priority_score (1-5, where 5 is highest priority)
2. safety_category (e.g., immediate concern, potential risk, minor issue)
3. reasoning (brief explanation)
4. key_concerns (list of main safety implications)"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI safety expert analyzing feedback for potential risks and safety implications."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # Parse the response
            analysis = eval(response.choices[0].message.content)
            
            # Add keyword-based analysis
            basic_analysis = self.analyze_text(description)
            analysis['keyword_flags'] = basic_analysis['flags']
            analysis['is_safety_concern'] = basic_analysis['is_safety_concern']
            
            return analysis
        except Exception as e:
            # Fallback to basic analysis if AI scoring fails
            basic_analysis = self.analyze_text(description)
            return {
                'priority_score': len(basic_analysis['flags']) + 1,
                'safety_category': 'automatic_fallback',
                'reasoning': 'AI analysis failed, using keyword-based scoring',
                'key_concerns': [flag['category'] for flag in basic_analysis['flags']],
                'keyword_flags': basic_analysis['flags'],
                'is_safety_concern': basic_analysis['is_safety_concern']
            }

    def get_safety_score(self, text: str) -> float:
        """Legacy method for compatibility."""
        analysis = self.analyze_text(text)
        return len(analysis['flags']) * 0.2  # 20% per flag, max 100%
