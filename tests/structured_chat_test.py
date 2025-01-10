from structured_chat import StructuredChatCompleter
from typing import List
from pydantic import BaseModel, Field

class IcdCodeInfo(BaseModel):
    code: str
    description: str

class ChatResponse(BaseModel):
    response: List[IcdCodeInfo] = Field(..., description="This field is required")

def test_chat():
    chat_completer = StructuredChatCompleter()
    messages = [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Please generate a list of 2 common ICD codes"}
    ]
    try:
        response = chat_completer.complete(messages, ChatResponse)
        assert(isinstance(response.response, list), "The response field must be a list")
        assert(len(response.response) == 2, "List must have length 2")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        assert(False)

