from models import AgentGoalState
from controller import ChatController

controller = ChatController()
agent_state = AgentGoalState.MATCHED
while(agent_state == AgentGoalState.MATCHED):
    response = controller.get_next_assistant_response()
    print()
    print(response.assistant_response)
    print()
    agent_state = response.agent_state
    if agent_state == AgentGoalState.MATCHED:
        user_input = input()
        controller.add_user_message(user_input)
