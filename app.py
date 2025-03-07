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

    # Custom CSS for better styling
    st.markdown("""
    <style>
        /* Customize the sidebar */
        .css-1d391kg {
            padding: 1rem;
            background-color: #f0f2f6;
        }
        .css-1d391kg h1 {
            color: #4CAF50;  /* Green */
        }
        .css-1d391kg h2 {
            color: #2E86C1;  /* Blue */
        }
        .css-1d391kg h3 {
            color: #4CAF50;  /* Green */
        }
        /* Add hover effects to buttons */
        .stButton button:hover {
            background-color: #45a049;  /* Darker green */
        }
        /* Change cursor to pointer for task selection */
        div[data-baseweb="select"] > div:first-child {
        cursor: pointer;
    }
    /* Change cursor to pointer for dropdown options */
    div[data-baseweb="menu"] > div > div {
        cursor: pointer;
    }
        /* Style for copy button */
        .copy-button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
        }
        .copy-button.copied {
            background-color: #45a049;
        }
    </style>
    """, unsafe_allow_html=True)

    # Title and welcome message
    st.title("MediMind - Multi-Agent AI System")
    st.markdown("""
    Welcome to **MediMind**! This application leverages advanced AI agents to perform tasks such as:
    - Summarizing medical text
    - Writing and refining research articles
    - Sanitizing medical data (PHI)
    
    Select a task from the sidebar to get started.
    """)

    # Sidebar improvements
    st.sidebar.markdown("""
    <div style="text-align: center;">
        <h1>🧠 MediMind</h1>
        <p>Your AI-powered healthcare assistant</p>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")

    # Task Selection
    st.sidebar.title("Task Selection")
    st.sidebar.markdown("Select a task from the list below to begin.")

    # Define the task options
    task_options = [
        "Summarize Medical Text",
        "Write and Refine Research Article",
        "Sanitize Medical Data (PHI)"
    ]

    # Use st.selectbox with a unique key
    task = st.sidebar.selectbox(
        "Choose a task:",
        options=task_options,
        index=0,  # Default selection
        key="task_selectbox",  # Unique key to prevent typing
        format_func=lambda x: x,  # Display the task name as is
    )

    # Add additional sidebar links
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔗 Quick Links")
    st.sidebar.markdown("""
    - [Documentation](https://medimind-docs.com)
    - [GitHub Repository](https://github.com/your-repo/medimind)
    - [Report a Bug](https://medimind-support.com/bug-report)
    - [Contact Support](mailto:support@medimind.com)
    """)

    # Initialize AgentManager
    agent_manager = AgentManager(max_retries=2, verbose=True)

    # Task-specific sections
    if task == "Summarize Medical Text":
        summarize_section(agent_manager)
    elif task == "Write and Refine Research Article":
        write_and_refine_article_section(agent_manager)
    elif task == "Sanitize Medical Data (PHI)":
        sanitize_data_section(agent_manager)

    # Footer
    st.markdown("---")
    st.markdown("""
    **MediMind**  
    Developed by [Your Name] | Version 1.0  
    [Contact Support](mailto:support@example.com)
    """)

def follow_up_section(agent_manager, context):
    """Handles follow-up questions for any section"""
    st.markdown("---")
    st.subheader("❓ Ask Follow-Up Questions")

    # Store context in session state
    st.session_state.follow_up_context = context

    # Input for follow-up question
    follow_up_query = st.text_input("Enter your follow-up question:", key="follow_up_input", value=st.session_state.follow_up_query)

    if st.button("Ask Follow-Up", key="follow_up_button"):
        if follow_up_query:
            with st.spinner("Generating follow-up questions..."):
                try:
                    follow_up_agent = agent_manager.get_agent("follow_up")
                    follow_up_questions = follow_up_agent.execute(
                        query=follow_up_query,
                        context=st.session_state.follow_up_context
                    )
                    st.session_state.follow_up_questions = follow_up_questions
                    st.success("Follow-up questions generated!")
                except Exception as e:
                    st.error(f"Error generating follow-up questions: {e}")
                    logger.error(f"FollowUpAgent Error: {e}")
        else:
            st.warning("Please enter a question for follow-up")

    # Display follow-up questions if they exist in session state
    if st.session_state.follow_up_questions:
        st.markdown("#### Suggested Follow-Ups:")
        st.write(st.session_state.follow_up_questions)

def summarize_section(agent_manager):
    st.header("📝 Summarize Medical Text")
    col1, col2 = st.columns([3, 2])

    with col1:
        text = st.text_area("Enter medical text to summarize:", height=200, placeholder="Paste your medical text here...")
        if st.button("Summarize"):
            if text:
                main_agent = agent_manager.get_agent("summarize")
                validator_agent = agent_manager.get_agent("summarize_validator")
                with st.spinner("Summarizing..."):
                    try:
                        summary = main_agent.execute(text)
                        st.success("Summarization complete!")
                        
                        st.markdown("---")
                        st.subheader("Summary:")
                        st.write(summary)
                        
                        # Validation
                        with st.spinner("Validating summary..."):
                            try:
                                validation = validator_agent.execute(original_text=text, summary=summary)
                                with st.expander("View Validation Details"):
                                    st.write(validation)
                            except Exception as e:
                                st.error(f"Validation Error: {e}")
                                logger.error(f"SummarizeValidatorAgent Error: {e}")
                        
                        # Follow-up questions
                        context = f"Original Text: {text}\n\nSummary: {summary}"
                        follow_up_section(agent_manager, context)
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
                        logger.error(f"SummarizeAgent Error: {e}")
            else:
                st.warning("Please enter some text to summarize.")

    with col2:
        st.markdown("### 🧠 Example Medical Text")
        example_text = """
        Patient Name: John Doe
        Diagnosis: Hypertension
        Treatment Plan: Prescribed Lisinopril 10mg daily.
        Notes: Patient advised to monitor blood pressure regularly and maintain a low-sodium diet.
        """
        st.code(example_text, language="plaintext")

        # Copy button for example text
        if st.button("Copy Example", key="copy_summarize_example"):
            st.session_state.copied_summarize = True
            st.write("✅ Copied to clipboard!")
        else:
            st.session_state.copied_summarize = False

        st.markdown("### 📝 Tips for Summarization")
        st.markdown("""
        - Ensure the text is clear and concise.
        - Avoid overly complex sentences.
        - Highlight key points for better summarization.
        """)

        st.markdown("### ❓ FAQs")
        st.markdown("""
        **Q: What types of text can I summarize?**  
        A: You can summarize medical reports, research articles, or any healthcare-related text.

        **Q: How accurate is the summarization?**  
        A: The summarization is highly accurate but always review the output for critical details.

        **Q: Can I use this for clinical purposes?**  
        A: This tool is designed for informational purposes only. Always consult a healthcare professional for clinical decisions.
        """)

def write_and_refine_article_section(agent_manager):
    st.header("📄 Write and Refine Research Article")
    col1, col2 = st.columns([3, 2])

    with col1:
        topic = st.text_input("Enter the topic for the research article:", placeholder="e.g., AI in Healthcare")
        outline = st.text_area("Enter an outline (optional):", height=150, placeholder="Provide a brief outline if available...")
        if st.button("Write and Refine Article"):
            if topic:
                writer_agent = agent_manager.get_agent("write_article")
                refiner_agent = agent_manager.get_agent("refiner")
                validator_agent = agent_manager.get_agent("validator")
                with st.spinner("Writing article..."):
                    try:
                        draft = writer_agent.execute(topic, outline)
                        st.success("Draft created successfully!")
                        
                        st.markdown("---")
                        st.subheader("Draft Article:")
                        st.write(draft)
                    except Exception as e:
                        st.error(f"Error: {e}")
                        logger.error(f"WriteArticleAgent Error: {e}")
                        return

                with st.spinner("Refining article..."):
                    try:
                        refined_article = refiner_agent.execute(draft)
                        st.success("Article refined successfully!")
                        
                        st.markdown("---")
                        st.subheader("Refined Article:")
                        st.write(refined_article)
                    except Exception as e:
                        st.error(f"Refinement Error: {e}")
                        logger.error(f"RefinerAgent Error: {e}")
                        return

                with st.spinner("Validating article..."):
                    try:
                        validation = validator_agent.execute(topic=topic, article=refined_article)
                        with st.expander("View Validation Details"):
                            st.write(validation)
                    except Exception as e:
                        st.error(f"Validation Error: {e}")
                        logger.error(f"ValidatorAgent Error: {e}")
                
                # Follow-up questions
                context = f"Topic: {topic}\n\nDraft: {draft}\n\nRefined Article: {refined_article}"
                follow_up_section(agent_manager, context)
            else:
                st.warning("Please enter a topic for the research article.")
                st.info("Tip: Provide a clear and specific topic for better results.")

    with col2:
        st.markdown("### 🧠 Example Topics")
        example_topics = """
        - The role of AI in diagnosing diseases.
        - Advances in telemedicine for rural healthcare.
        - Ethical considerations in genetic engineering.
        """
        st.code(example_topics, language="plaintext")

        # Copy button for example topics
        if st.button("Copy Example", key="copy_write_example"):
            st.session_state.copied_write = True
            st.write("✅ Copied to clipboard!")
        else:
            st.session_state.copied_write = False

        st.markdown("### 📝 Tips for Writing")
        st.markdown("""
        - Be specific about the topic.
        - Provide a clear outline if possible.
        - Use bullet points for better structure.
        """)

        st.markdown("### ❓ FAQs")
        st.markdown("""
        **Q: Can I use this tool for academic writing?**  
        A: Yes, this tool is ideal for drafting and refining academic articles.

        **Q: How long does it take to generate an article?**  
        A: The process typically takes a few minutes, depending on the complexity of the topic.

        **Q: Can I edit the output?**  
        A: Absolutely! The refined article is a starting point—feel free to make further edits.
        """)

def sanitize_data_section(agent_manager):
    st.header("🔒 Sanitize Medical Data (PHI)")
    col1, col2 = st.columns([3, 2])

    with col1:
        medical_data = st.text_area("Enter medical data to sanitize:", height=200, placeholder="Paste medical data here...")
        if st.button("Sanitize Data"):
            if medical_data:
                main_agent = agent_manager.get_agent("sanitize_data")
                validator_agent = agent_manager.get_agent("sanitize_data_validator")
                with st.spinner("Sanitizing data..."):
                    try:
                        sanitized_data = main_agent.execute(medical_data)
                        st.success("Data sanitized successfully!")
                        
                        st.markdown("---")
                        st.subheader("Sanitized Data:")
                        st.write(sanitized_data)
                    except Exception as e:
                        st.error(f"Error: {e}")
                        logger.error(f"SanitizeDataAgent Error: {e}")
                        return

                with st.spinner("Validating sanitized data..."):
                    try:
                        validation = validator_agent.execute(original_data=medical_data, sanitized_data=sanitized_data)
                        with st.expander("View Validation Details"):
                            st.write(validation)
                    except Exception as e:
                        st.error(f"Validation Error: {e}")
                        logger.error(f"SanitizeDataValidatorAgent Error: {e}")
                
                # Follow-up questions
                context = f"Original Data: {medical_data}\n\nSanitized Data: {sanitized_data}"
                follow_up_section(agent_manager, context)
            else:
                st.warning("Please enter medical data to sanitize.")
                st.info("Tip: Ensure the data contains PHI for accurate sanitization.")

    with col2:
        st.markdown("### 🧠 Example Medical Data")
        example_data = """
        Patient Name: John Doe
        Address: 123 Main St, Springfield, IL
        Phone: (555) 123-4567
        Date of Birth: 1985-07-15
        Medical Record Number: 987654321
        Diagnosis: Hypertension
        Treatment Plan: Prescribed Lisinopril 10mg daily.
        """
        st.code(example_data, language="plaintext")

        # Copy button for example data
        if st.button("Copy Example", key="copy_sanitize_example"):
            st.session_state.copied_sanitize = True
            st.write("✅ Copied to clipboard!")
        else:
            st.session_state.copied_sanitize = False

        st.markdown("### 📝 Step-by-Step Instructions")
        st.markdown("""
        1. **Paste Data**: Copy and paste medical data into the text area on the left.
        2. **Click Sanitize**: Click the **Sanitize Data** button to process the data.
        3. **Review Output**: Check the sanitized output for accuracy.
        4. **Validate**: View validation details to ensure compliance.
        """)

        st.markdown("### ❓ FAQs")
        st.markdown("""
        **Q: What is PHI?**  
        A: PHI (Protected Health Information) includes any data that can identify a patient, such as names, addresses, or medical record numbers.

        **Q: Is this tool HIPAA-compliant?**  
        A: Yes, this tool is designed to help you comply with HIPAA regulations by removing or anonymizing PHI.

        **Q: Can I use this for research purposes?**  
        A: Absolutely! This tool is ideal for sanitizing data before using it in research studies.
        """)

if __name__ == "__main__":
    main()