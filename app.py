import streamlit as st
from agents import AgentManager
from agents.follow_up_agent import FollowUpAgent
from utils.logger import logger
import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Initialize session state for follow-up questions
if "follow_up_context" not in st.session_state:
    st.session_state.follow_up_context = None
if "follow_up_questions" not in st.session_state:
    st.session_state.follow_up_questions = None
if "follow_up_query" not in st.session_state:
    st.session_state.follow_up_query = ""

def handle_follow_up():
    if st.session_state.follow_up_query:
        try:
            follow_up_agent = AgentManager.get_agent("follow_up")
            st.session_state.follow_up_questions = follow_up_agent.execute(
                query=st.session_state.follow_up_query,
                context=st.session_state.follow_up_context
            )
            st.success("Follow-up questions generated!")
        except Exception as e:
            st.error(f"Error generating follow-up questions: {e}")
            logger.error(f"FollowUpAgent Error: {e}")

def main():
    # Set page configuration
    st.set_page_config(
        page_title="MediMind - Multi-Agent AI System",
        layout="wide",
        menu_items={
            "Get Help": "https://medimind-support.com",
            "Report a Bug": "https://medimind-support.com/bug-report",
            "About": """
            ## MediMind  
            **Version**: 1.0  
            **Developed by**: [Your Name]  
            **Contact**: support@medimind.com  
            **GitHub**: [MediMind Repo](https://github.com/your-repo/medimind)  
            """
        }
    )