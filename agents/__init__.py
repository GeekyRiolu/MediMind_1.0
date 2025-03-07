from .summarize_tool import SummarizeTool
from .write_article_tool import WriteArticleTool
from .sanitize_data_tool import SanitizeDataTool
from .summarize_validator_agent import SummarizeValidatorAgent
from .write_article_validator_agent import WriteArticleValidatorAgent
from .sanitize_data_validator_agent import SanitizeDataValidatorAgent
from .refiner_agent import RefinerAgent
from .validator_agent import ValidatorAgent
from .clinic_agent import ClinicAgent
from .follow_up_agent import FollowUpAgent

class AgentManager:
    def __init__(self, max_retries=2, verbose=True, agents=None):
        """
        Initialize the AgentManager.

        Args:
            max_retries (int): Maximum retries for agent operations.
            verbose (bool): Whether to enable verbose logging.
            agents (dict): Optional custom dictionary of agents to override defaults.
        """
        # Default agents
        self.agents = {
            "summarize": SummarizeTool(max_retries=max_retries, verbose=verbose),
            "write_article": WriteArticleTool(max_retries=max_retries, verbose=verbose),
            "sanitize_data": SanitizeDataTool(max_retries=max_retries, verbose=verbose),
            "summarize_validator": SummarizeValidatorAgent(max_retries=max_retries, verbose=verbose),
            "write_article_validator": WriteArticleValidatorAgent(max_retries=max_retries, verbose=verbose),
            "sanitize_data_validator": SanitizeDataValidatorAgent(max_retries=max_retries, verbose=verbose),
            "refiner": RefinerAgent(max_retries=max_retries, verbose=verbose),
            "validator": ValidatorAgent(max_retries=max_retries, verbose=verbose),
            "follow_up": FollowUpAgent(max_retries=max_retries, verbose=verbose),
            "clinic": ClinicAgent(max_retries=max_retries, verbose=verbose),
        }

        # Override default agents with custom agents if provided
        if agents:
            self.agents.update(agents)

    def get_agent(self, agent_name):
        """
        Retrieve an agent by name.

        Args:
            agent_name (str): The name of the agent to retrieve.

        Returns:
            The requested agent.

        Raises:
            ValueError: If the agent is not found.
        """
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")
        return agent