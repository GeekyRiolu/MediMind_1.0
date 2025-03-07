# agents/follow_up_agent.py

from .agent_base import AgentBase

class FollowUpAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="FollowUpAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, query, context):
        messages = [
            {"role": "system", "content": "You are an AI assistant that asks follow-up questions to better understand the user's query."},
            {"role": "user", "content": f"Query: {query}\nContext: {context}\n\nFollow-Up Questions:"}
        ]
        return self.call_openai(messages, max_tokens=200)