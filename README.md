# OpenAI, Claude, Llama Internal Feedback System

A sophisticated feedback management system focused on AI safety and alignment discussions for OpenAI's leadership team.

## Features
- AI-powered safety analysis and priority scoring
- Interactive dashboard with real-time visualizations
- Safety-focused feedback categorization
- Tag-based filtering and organization
- Upvoting system for feedback prioritization

## Technology Stack
- Frontend: Streamlit
- Backend: Python, PostgreSQL
- AI Analysis: OpenAI GPT-4 API

## Requirements
- Python 3.11+
- PostgreSQL database
- OpenAI API key

## Environment Variables
Required environment variables:
- OPENAI_API_KEY
- PGHOST
- PGDATABASE
- PGUSER
- PGPASSWORD
- PGPORT

## Setup Instructions
1. Clone the repository
2. Set up environment variables
3. Install dependencies
4. Run `streamlit run main.py`

## Project Structure
- /components: UI components and views
- /utils: Database, NLP, and visualization utilities
- main.py: Application entry point

## Usage
1. Navigate to Dashboard to view feedback analytics
2. Use Submit Feedback to provide new feedback
3. Filter feedback by priority, tags, and safety concerns
4. Upvote important feedback items

## Safety Analysis Features
- Automatic safety implication detection
- Priority scoring based on AI analysis
- Safety category classification
- Detailed reasoning for safety concerns
