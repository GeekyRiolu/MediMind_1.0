# agents/clinic_agent.py

from .agent_base import AgentBase
from .sanitize_data_tool import SanitizeDataTool
from .write_article_tool import WriteArticleTool
from .summarize_tool import SummarizeTool
from loguru import logger

class ClinicAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="ClinicAgent", max_retries=max_retries, verbose=verbose)
        self.sanitize_agent = SanitizeDataTool(max_retries=max_retries, verbose=verbose)
        self.write_agent = WriteArticleTool(max_retries=max_retries, verbose=verbose)
        self.summarize_agent = SummarizeTool(max_retries=max_retries, verbose=verbose)

    def execute(self, ehr_data):
        """
        Processes EHR data to provide medical advice and a summary.
        :param ehr_data: The patient's EHR data.
        :return: Sanitized data, medical advice, and a summary.
        """
        try:
            # Step 1: Sanitize the EHR data
            sanitized_data = self.sanitize_agent.execute(ehr_data)
            if self.verbose:
                logger.info(f"[{self.name}] Sanitized EHR data: {sanitized_data}")

            # Step 2: Generate medical advice
            medical_advice = self.generate_medical_advice(sanitized_data)
            if self.verbose:
                logger.info(f"[{self.name}] Medical advice: {medical_advice}")

            # Step 3: Summarize the results
            summary = self.summarize_agent.execute(medical_advice)
            if self.verbose:
                logger.info(f"[{self.name}] Summary: {summary}")

            return {
                "sanitized_data": sanitized_data,
                "medical_advice": medical_advice,
                "summary": summary,
            }

        except Exception as e:
            logger.error(f"[{self.name}] Error: {e}")
            raise

    def generate_medical_advice(self, sanitized_data):
        """
        Generates medical advice based on the sanitized EHR data.
        :param sanitized_data: The sanitized EHR data.
        :return: Medical advice in text format.
        """
        # Example: Use the Write and Refine Agent to generate advice
        prompt = (
            "You are a medical expert. Based on the following patient data, provide a detailed treatment plan or medication advice:\n\n"
            f"{sanitized_data}\n\n"
            "Medical Advice:"
        )
        messages = [
            {"role": "system", "content": "You are a medical expert."},
            {"role": "user", "content": prompt},
        ]
        medical_advice = self.write_agent.call_openai(messages, max_tokens=500)
        return medical_advice