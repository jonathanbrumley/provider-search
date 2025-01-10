from structured_chat import StructuredChatCompleter
from abc import ABC, abstractmethod
from models import ProviderSearchInputState, ProviderSearchAgentResponse, AgentGoalState
from typing import List, Dict

class ProviderSearchChatAgent(ABC):
    """
    Abstract base class for a ProviderSearchChatAgent.    
    Subclasses must implement the is_match(), constraints() and next_goal() methods.
    """
    @abstractmethod
    def is_match(self, input_state: ProviderSearchInputState) -> bool:
        """
        Abstract method to return whether this agent matches the current state
        Parameters:
            input_state (ProviderSearchInputState): The current state of the user's input.
        Returns:
            a boolean indicating whether this agent matches
        """
        return ""
    @abstractmethod
    def constraints(self) -> str:
        """
        Abstract method to return constraints specific to this agent
        Returns:
            a string describing additional constraints for this agent's outputs
        """
        return ""
    @abstractmethod
    def goal(self) -> str:
        """
        Abstract method to return the chat goal specific to this agent
        Returns:
            a string describing goals for this agent's chat message
        """
        return ""


class GeneralProviderSearchAgent(ProviderSearchChatAgent):
    def is_match(self, input_state: ProviderSearchInputState) -> bool:
        return (
            input_state.member_profile.gender is None and
            input_state.member_profile.age is None and
            input_state.member_profile.insurance is None and
            input_state.member_profile.language is None and
            input_state.provider_preferences.specialties is None and
            input_state.provider_preferences.therapy_types is None and 
            input_state.provider_preferences.gender is None and 
            input_state.provider_preferences.appointment_types is None
        )

    def goal(self) -> str:
        return '''
            Ask the user why they are seeking treatment.
        '''

    def constraints(self) -> str:
        return '''
            provider_preferences.specialties should contain a list of treatment specialties matching why the user is seeking treatment
            provider_preferences.therapy_types should contain a list therapy types matching why the user is seeking treatment
 
            If any information about the member or provider preferences is now known, the agent_state should be COMPLETE
            If the user does not want to provide additional information, agent_stage should be NO_MATCH
            If the member's age is still unknown or member's gender is still unknown, agent_state should be MATCH
        '''


class MemberDemographicsProviderSearchAgent(ProviderSearchChatAgent):
    def is_match(self, input_state: ProviderSearchInputState) -> bool:
        return input_state.member_profile.gender is None or input_state.member_profile.age is None

    def goal(self) -> str:
        return '''
            Ask the user about their insurance so you can populate member_profile.insurance
        '''

    def constraints(self) -> str:
        return '''
            If both the member's age and gender are now known, agent_state should be COMPLETE
            If the user does not want to provide this information, agent_stage should be COMPLETE
            If the member's age is still unknown OR member's gender is still unknown, agent_state should be MATCH
        '''


class MemberInsuranceProviderSearchAgent(ProviderSearchChatAgent):
    def is_match(self, input_state: ProviderSearchInputState) -> bool:
        return input_state.member_profile.insurance is None

    def goal(self) -> str:
        return '''
            Ask the user about their health insurance so you can populate the member_profile.insurance
        '''

    def constraints(self) -> str:
        return '''
            If the member's insurance is now known, agent_state should be COMPLETE
            If the user does not want to provide insurance information, agent_stage should be COMPLETE
            If the member's insurance is still unknown, agent_state should be MATCH
        '''


class MemberLanguangeProviderSearchAgent(ProviderSearchChatAgent):
    def is_match(self, input_state: ProviderSearchInputState) -> bool:
        return input_state.member_profile.language is None

    def goal(self) -> str:
        return '''
            Ask the user to confirm their preferred language, so you can populate the member_profile.language
        '''

    def constraints(self) -> str:
        return '''
            If the member's preferred language is now known, agent_state should be COMPLETE
            If the user does not want to provide their language, agent_stage should be COMPLETE
            If the member's preferred language is still unknown, agent_state should be MATCH
        '''


class ProviderSpecialtiesProviderSearchAgent(ProviderSearchChatAgent):
    def is_match(self, input_state: ProviderSearchInputState) -> bool:
        return input_state.provider_preferences.specialties is None or len(input_state.provider_preferences.specialties) == 0

    def goal(self) -> str:
        return '''
            Ask the user why they are seeking a provider, so that you can populate provider_preferences.specialties
        '''

    def constraints(self) -> str:
        return '''
            If preferred provider treatment specialties are known, agent_state should be COMPLETE
            If the user does not want to specify why they are seeking a provider, the agent_stage should be COMPLETE
            If preferred provider treatment specialties are still unknown is None or empty, agent_state should be MATCH
        '''


class TherapyTypeProviderSearchAgent(ProviderSearchChatAgent):
    def is_match(self, input_state: ProviderSearchInputState) -> bool:
        return input_state.provider_preferences.therapy_types is None or len(input_state.provider_preferences.therapy_types) == 0

    def goal(self) -> str:
        return '''
            Provide examples and ask the user what treatment types they prefer, so that you can populate provider_preferences.treatment_types
        '''

    def constraints(self) -> str:
        return '''
            If preferred provider treatment types are now known, agent_state should be COMPLETE
            If the user does not care or is unable to provide this information, the agent_stage should be COMPLETE
            If preferred provider treatment_types are still unknown, agent_state should be MATCH
        '''


class ProviderGenderProviderSearchAgent(ProviderSearchChatAgent):
    def is_match(self, input_state: ProviderSearchInputState) -> bool:
        return input_state.provider_preferences.gender is None

    def goal(self) -> str:
        return '''
            Ask the user if they prefer a provider of a specific gender, so you can populate provider_preferences.gender
        '''

    def constraints(self) -> str:
        return '''
            If preferred provider gender is now known, agent_state should be COMPLETE
            If the user does not want to provide this information, agent_state should be COMPLETE
            If preferred provider gender is still unknown, agent_state should be MATCH

        '''

class AppointmentTypeProviderSearchAgent(ProviderSearchChatAgent):
    def is_match(self, input_state: ProviderSearchInputState) -> bool:
        return input_state.provider_preferences.appointment_types is None or len(input_state.provider_preferences.appointment_types) == 0

    def goal(self) -> str:
        return '''
            Ask the user if they prefer an in-person or vitual appointment, so that you can populate provider_preferences.appointment_types
        '''

    def constraints(self) -> str:
        return '''
            If preferred appointment types are now known, agent_state should be COMPLETE
            If the user does not care or provide this information, the agent_stage should be COMPLETE
            If preferred appointment_types are still unknown, agent_state should be MATCH
        '''

class ConfirmationProviderSearchAgent(ProviderSearchChatAgent):
    def is_match(self, input_state: ProviderSearchInputState) -> bool:
        return True

    def goal(self) -> str:
        return '''
            Ask the user to confirm that the information you have collected is correct.
            Is there anything to add or correct?
        '''

    def constraints(self) -> str:
        return '''
            If the user confirms all information is correct, agent_state should be COMPLETE
            If the user adds or corrects information, the agent_stage should be MATCH
        '''
