# @title Define Agent Interaction Function
import asyncio
from google.genai import types # For creating message Content/Parts
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from agent import root_agent
from constants import *

async def call_agent_async(query: str, runner, user_id, session_id):
  """Sends a query to the agent and prints the final response."""
  print(f"\n>>> User Query: {query}")

  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
      # You can uncomment the line below to see *all* events during execution
      # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      # Key Concept: is_final_response() marks the concluding message for the turn.
      if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found

  print(f"<<< Agent Response: {final_response_text}")

if __name__=="__main__":
    # import litellm
    # litellm._turn_on_debug()

    session_service = InMemorySessionService()
    initial_state = {
        "user_preference_temperature_unit": "Celsius"
    }

    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )

    retrieved_session = session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    print("\n--- Initial Session State ---")
    if retrieved_session:
        print(retrieved_session.state)
    else:
        print("Error: Could not retrieve session.")

    runner_agent_team = Runner(
        agent=root_agent, # The agent we want to run
        app_name=APP_NAME,   # Associates runs with our app
        session_service=session_service, # Uses our session manager
    )

    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    print(f"Runner created for agent '{root_agent.name}'.")

    # We need an async function to await our interaction helper
    async def run_conversation():
        print("--- Turn 1: Requesting weather in London (expect Celsius) ---")
        await call_agent_async(
            query= "Londonの天気は何ですか?",
            runner=runner_agent_team,
            user_id=USER_ID,
            session_id=SESSION_ID
        )
        # 2. Manually update state preference to Fahrenheit - DIRECTLY MODIFY STORAGE
        print("\n--- Manually Updating State: Setting unit to Fahrenheit ---")
        try:
            # Access the internal storage directly - THIS IS SPECIFIC TO InMemorySessionService for testing
            stored_session = session_service.sessions[APP_NAME][USER_ID][SESSION_ID]
            stored_session.state["user_preference_temperature_unit"] = "Fahrenheit"
            print(f"--- Stored session state updated. Current 'user_preference_temperature_unit': {stored_session.state['user_preference_temperature_unit']} ---")
        except KeyError:
            print(f"--- Error: Could not retrieve session '{SESSION_ID}' from internal storage for user '{USER_ID}' in app '{APP_NAME}' to update state. Check IDs and if session was created. ---")
        except Exception as e:
            print(f"--- Error updating internal session state: {e} ---")

        # 3. Check weather again (Tool should now use Fahrenheit)
        # This will also update 'last_weather_report' via output_key
        print("\n--- Turn 2: Requesting weather in New York (expect Fahrenheit) ---")
        await call_agent_async(
            query= "New Yorkの天気を教えてください。",
            runner=runner_agent_team,
            user_id=USER_ID,
            session_id=SESSION_ID
        )
    
        # 4. Test basic delegation (should still work)
        # This will update 'last_weather_report' again, overwriting the NY weather report
        print("\n--- Turn 3: Sending a greeting ---")
        await call_agent_async(
            query= "こんにちは!",
            runner=runner_agent_team,
            user_id=USER_ID,
            session_id=SESSION_ID
        )

        print("\n--- Inspecting Final Session State ---")
        final_session = session_service.sessions[APP_NAME][USER_ID][SESSION_ID]
        if final_session:
            print(f"Final Preference: {final_session.state.get('user_preference_temperature_unit')}")
            print(f"Final Last Weather Report (from output_key): {final_session.state.get('last_weather_report')}")
            print(f"Final Last City Checked (by tool): {final_session.state.get('last_city_checked_stateful')}")
        else:
            print("\n❌ Error: Could not retrieve final session state.")

    asyncio.run(run_conversation())
