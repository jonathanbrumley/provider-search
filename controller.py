import agents
from structured_chat import StructuredChatCompleter
from models import ProviderSearchInputState, MemberProfile, ProviderPreferences, AgentGoalState, ProviderSearchAgentResponse
from typing import Optional

class ChatController:
    def __init__(self):
        self.completer = StructuredChatCompleter()
        self.messages = [
            {"role": "developer", "content": "You are a helpful assistant."},
        ]
        self.agent_state = AgentGoalState.MATCHED
        self.agent = None
        self.search_input_state = ProviderSearchInputState(
            member_profile=MemberProfile(),
            provider_preferences=ProviderPreferences(),
        )
        self.unused_agents = list(reversed([
            agents.ProviderSpecialtiesProviderSearchAgent(),
            agents.AppointmentTypeProviderSearchAgent(),
            agents.ProviderGenderProviderSearchAgent(),
            agents.TherapyTypeProviderSearchAgent(),
            agents.MemberDemographicsProviderSearchAgent(),
            agents.MemberLanguangeProviderSearchAgent(),
            agents.MemberInsuranceProviderSearchAgent(),
        ]))

    def get_unused_agent(self) -> Optional[agents.ProviderSearchChatAgent]:
        unused_agents = [agent for agent in self.unused_agents if agent.is_match(self.search_input_state)]
        if len(unused_agents) > 0:
            self.agent = unused_agents.pop()
            self.unused_agents.remove(self.agent)
            return self.agent
        return None

    def get_agent(self) -> agents.ProviderSearchChatAgent:
        if self.agent == None:
            self.agent = agents.GeneralProviderSearchAgent()
        if self.agent_state == AgentGoalState.MATCHED and self.agent.is_match(self.search_input_state):
            pass
        elif self.get_unused_agent() is not None:
            pass
        else:
            self.agent = agents.GeneralProviderSearchAgent()
        return self.agent

    def get_prompt(self) -> Optional[str]:
        agent = self.get_agent()
        return f'''
                You assist the user to find a mental health provider in the provider directory.
                Your goal is to prompt the user to answer questions about themselves and their preferred provider
                so you can populate fields in their member profile and in provider preferences.

                You can ask one or two questions at a time.
    
            <GOAL>
                {agent.goal()}
                Note: you plan to collect additional information after you achieve this goal.
            </GOAL>
            <CONSTRAINTS>
                MemberProfile must always be populated with a dictionary.
                ProviderPreferences must always be populated with a dictionary.
                MemberProfile and ProviderPreferences fields should be null or empty list if not specified by the user.

                YOUR RESPONSE SHOULD NOT SAY "LASTLY" or "LAST" BECAUSE THIS IS NOT THE LAST QUESTION
                {agent.constraints()}
            </CONSTRAINTS>
        '''

    def get_response_from_matching_agent(self) -> ProviderSearchAgentResponse:
        prompt = self.get_prompt()
        self.messages[0] = {"role": "developer", "content": prompt}
        return self.completer.complete(self.messages, ProviderSearchAgentResponse)

    def get_next_assistant_response(self) -> ProviderSearchAgentResponse:
        # TODO - summarize chat history before input length exceeds max input token count
        
        # call the current agent to extract any new provider search information
        response = self.get_response_from_matching_agent()
        self.search_input_state = response.provider_search_information

        # if the extracted state no longer matches the current agent, then find the next matching agent
        if (not self.agent.is_match(self.search_input_state)) or response.agent_state == AgentGoalState.COMPLETE:
            response = self.get_response_from_matching_agent()
    
        self.search_input_state = response.provider_search_information
        self.agent_state = response.agent_state
        self.messages.append({"role": "assistant", "content": response.model_dump_json()})
        # For debugging
        print(response.provider_search_information.model_dump_json())
        if response.agent_state == AgentGoalState.COMPLETE and self.get_unused_agent is None:
            return response
        response.agent_state = AgentGoalState.MATCHED
        return response        
    
    def add_user_message(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
