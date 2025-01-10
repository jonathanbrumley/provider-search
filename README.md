# Provider Search Chat

## About
This is a console provider search chat application to guide a user in specifying information for a mental health provider search.

## Installing on MacOS
Create a python virtual environment and install dependencies
1. python3 -m venv .
2. source ./bin/activate
3. pip install pydantic
4. pip install openai

For running tests, install pytest
1. brew install pytest

## Running
From the project root directory:
> python3 main.py

## Testing
From the project root directory:
> pytest

## Design
The job of the chat controller is to collect enough information about the member's profile and provider preferences in order to conduct a provider search.

1. Member profile and provider preference models are stored in search input state, along with chat history.
2. The ProviderSearchController chooses a ProviderSearchAgent for the next set of questions, based on state.
3. When no data has been collected, it chooses the GeneralProviderSearchAgent as a starting agent
4. If required information is not yet answered, it will choose an individual agent, such as MemberDemographicsProviderSearchAgent
5. If the individual agent has completed its questioning, it will not be selected again
6. If an individual agent returns no match, the GeneralProviderSearchAgent will try a general response.
7. After all data has been collected and confirmed, the GeneralProviderSearchAgent will respond with a list of matching providers
   (this last part is not yet implemented)

## File organization
* main.py - executes console input/output and calls the controller in a loop
* contoller.py - tracks the search state and chat history and selects the next agent
* agents.py - individual agents which specify what state they match on, prompt goal and constraints
* models.py - Pydantic models for the search input and provider data
* structured_chat.py - a helper for OpenAI chat completions returning structured outputs

## Observations
* gpt-4o-mini has somewhat inconsistent performance compared with gpt-4o.  It is not great at matching provider specialties
to why the user is present.

## Future improvements
If provider data is initially unstructured (e.g. scraped from web sites), we could use the LLM to structure it.
Ideally the provider data and search input are structured

* structured matching is far more scalable than LLM matching for large datasets.
* LLM will not be able to match efficiently if the amount of data to match is larger than max tokens
* structured matching can support matching against a large set of provider data (1M entries or more) using a SQL database or ES cluster
* It might be nice to support some unstructured matching for "other" provider information.
* The way this is work is that the structured search would first identify a small count of providers (e.g. 50), then an LLM matching operation would run on the small set

