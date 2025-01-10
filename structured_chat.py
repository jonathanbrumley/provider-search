from pydantic import BaseModel
from openai import OpenAI
from typing import List


class StructuredChatCompleter:
    """
        This StructuredChatCompleter supports a complete() method
        which returns structured JSON from the openai chat completions endpoint
    """

    def __init__(self, temperature=0.65, model="gpt-4o-mini"):
        """
            Initializes an OpenAI client to the specified model with the specified temperature
            The API key must be specified in OPENAI_API_KEY

            Parameters:
                temperature (float): Controls randomness of the model's responses. Default is 0.7.
                model (str): Specifies the model to be used for the completion request. Default is "gpt-4o-mini".
        """
        self.client = OpenAI()
        self.temperature = temperature
        self.model = model

    def complete(self, messages, response_model: BaseModel):
        """
        Sends a list of messages to the OpenAI Chat Completion API and returns the structured JSON response.
        
        This method will verify that the response returned from the API matches the expected structure 
        defined by the provided Pydantic model.

        Parameters:
            messages (List[dict]): A list of message objects, where each message is a dictionary with 'role' and 'content'.
            response_model (BaseModel): A Pydantic model that defines the expected structure of the API response.

        Returns:
            dict or str: If the response is valid, returns the structured JSON as a Pydantic model instance.
                        If the response does not match the expected format, returns a validation error message.
        """
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            temperature=self.temperature,
            messages=messages,
            response_format=response_model,
        )
        return completion.choices[0].message.parsed
