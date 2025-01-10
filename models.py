from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class TreatmentSpecialty(str, Enum):
    ADHD = "ADHD"
    ANXIETY = "ANXIETY"
    AUTISM = "AUTISM"
    BIPOLAR = "BIPOLAR"
    STRESS = "STRESS"
    BORDERLINE_PERSONALITY = "BORDERLINE_PERSONALITY" 
    DEPRESSION = "DEPRESSION"
    INSOMNIA = "INSOMNIA"
    OCD = "OCD"
    PTSD = "PTSD"
    PSYCHOSIS = "PSYCHOSIS"
    ADDICTION = "ADDICTION"
    SELF_HARM = "SELF_HARM"
    DEMENTIA = "DEMENTIA"
    DYSLEXIA = "DYSLEXIA"
    DIVORCE = "DIVORCE"
    PANIC_ATTACKS = "PANIC_ATTACKS"
    BIPOLAR_DISORDER = "BIPOLAR_DISORDER" 
    EATING_DISORDER = "EATING_DISORDER" 
    MARRIAGE_COUNSELING = "MARRIAGE_COUNSELING"
    LIFE_COACHING = "LIFE_COACHING"

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class TreatmentAge(str, Enum):
    TODDLER = "TODDLER"
    CHILD = "CHILD"
    ADOLESCENT = "ADOLESCENT"
    ADULT = "ADULT"
    ELDER = "ELDER"

class Insurance(str, Enum):
    NO_INSURANCE = "NO_INSURANCE"
    AETNA = "AETNA"
    UNITED_HEALTHCARE = "UNITED_HEALTHCARE"
    BLUE_CROSS = "BLUE_CROSS"
    CIGNA = "CIGNA"
    HUMANA = "HUMANA"
    MEDICARE = "MEDICARE"

class TherapyType(str, Enum):
    COGNITIVE_BEHAVIORAL = "COGNITIVE_BEHAVIORAL"
    FAMILY = "FAMILY"
    TRAUMA = "TRAUMA"
    COUPLES = "COUPLES"

class Language(str, Enum):
    ARABIC = "ARABIC"
    SPANISH = "SPANISH"
    ENGLISH = "ENGLISH"
    FRENCH = "FRENCH"
    ITALIAN = "ITALIAN"
    GERMAN = "GERMAN"
    RUSSIAN = "RUSSIAN"
    VIETNAMESE = "VIETNAMESE"
    MANDORIN="MANDORIN"
    CANTONESE = "CANTONESE"
    HINDI="HINDI"

class AppointmentType(str, Enum):
    IN_PERSON = "IN_PERSON"
    ONLINE = "ONLINE"

class Name(BaseModel):
    first: Optional[str] = Field(default=None, description="first name")
    last: Optional[str] = Field(default=None, description="last name")
    class Config:
        extra = "forbid"  # This ensures additionalProperties is set to false


class MemberProfile(BaseModel):
    '''
        This member profile is stored in the chat state and collected during the chat
        It ultimately is an input to the provider matching
    '''
    gender: Optional[Gender] = Field(default=None, description="member gender")
    age: Optional[int] = Field(default=None, description="member age in years")
    insurance: Optional[Insurance] = Field(default=None, description="member's insurance")
    language: Optional[Language] = Field(default=None, description="member's preferred language")
    class Config:
        extra = "forbid"  # This ensures additionalProperties is set to false


class ProviderPreferences(BaseModel):
    '''
        These provider preferences are stored in the chat state and collected during the chat
        It ultimately is an input to the provider matching
    '''
    specialties: Optional[List[TreatmentSpecialty]] = Field(None, description="Preference for provider treatment specialties")
    therapy_types: Optional[List[TherapyType]] = Field(None, description="Preference for therapy type")
    gender: Optional[Gender] = Field(default=None, description="Preference for provider gender")
    appointment_types: Optional[List[AppointmentType]] = Field(None, description="Preferences for appointment type")
    class Config:
        extra = "forbid"  # This ensures additionalProperties is set to false


class ProviderInformation(BaseModel):
    '''
        This provider information comes from the provider roster and is stored in the provider database before chat begins
    '''
    name: Name
    specialties: List[TreatmentSpecialty]
    ages_treated: List[TreatmentAge]
    insurance_accepted: List[Insurance]
    languages_spoken: List[Language]
    genders_treated: List[Gender]
    appointment_types: List[AppointmentType]
    therapy_types: List[TherapyType]
    class Config:
        extra = "forbid"  # This ensures additionalProperties is set to false


class ProviderSearchInputState(BaseModel):
    member_profile: MemberProfile = Field(..., description="member information needed for provider search")
    provider_preferences: ProviderPreferences = Field(..., description="member's preferences about a provider")
    class Config:
        extra = "forbid"  # This ensures additionalProperties is set to false

class AgentGoalState(str, Enum):
    NO_MATCH = "NO_MATCH"
    MATCHED = "MATCHED"
    COMPLETE = "COMPLETE"

class ProviderSearchAgentResponse(BaseModel):
    assistant_response: str
    provider_search_information: ProviderSearchInputState = Field(..., description="all user responses relevant to provider search")
    agent_state: AgentGoalState = Field(..., description="whether the user message is relevant to this agent, and if so, whether the goal is complete")
    class Config:
        extra = "forbid"  # This ensures additionalProperties is set to false
