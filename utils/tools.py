from google.adk.tools.tool_context import ToolContext

def get_weather(city: str, tool_context: ToolContext) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    # Best Practice: Log tool execution for easier debugging
    print(f"--- Tool: get_weather called for city: {city} ---")
    preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Celsius") # Default to Celsius
    print(f"--- Tool: Reading state 'user_preference_temperature_unit': {preferred_unit} ---")

    city_normalized = city.lower().replace(" ", "")

    # Mock weather data (always stored in Celsius internally)
    mock_weather_db = {
        "newyork": {"temp_c": 25, "condition": "晴れ"},
        "london": {"temp_c": 15, "condition": "曇り"},
        "tokyo": {"temp_c": 18, "condition": "弱い雨"},
        "東京": {"temp_c": 18, "condition": "弱い雨"},
    }

    if city_normalized in mock_weather_db:
        data = mock_weather_db[city_normalized]
        temp_c = data["temp_c"]
        condition = data["condition"]

        # Format temperature based on state preference
        if preferred_unit == "Fahrenheit":
            temp_value = (temp_c * 9/5) + 32 # Calculate Fahrenheit
            temp_unit = "°F"
        else: # Default to Celsius
            temp_value = temp_c
            temp_unit = "°C"

        report = f"{city.capitalize()}の天気は{condition}で、気温は{temp_value:.0f}{temp_unit}です。"
        result = {"status": "success", "report": report}
        print(f"--- Tool: Generated report in {preferred_unit}. Result: {result} ---")

        # Example of writing back to state (optional for this tool)
        tool_context.state["last_city_checked_stateful"] = city
        print(f"--- Tool: Updated state 'last_city_checked_stateful': {city} ---")

        return result
    else:
        # Handle city not found
        error_msg = f"Sorry, I don't have weather information for '{city}'."
        print(f"--- Tool: City '{city}' not found. ---")
        return {"status": "error", "error_message": error_msg}

def say_hello(name: str) -> str:
    """Provides a simple greeting, optionally addressing the user by name.

    Args:
        name (str): The name of the person to greet. If nothing, set "ユーザー".

    Returns:
        str: A friendly greeting message.
    """
    if name is None:
        name = 'ユーザー'
    print(f"--- Tool: say_hello called with name: {name} ---")
    return f"こんにちは、{name}さん!"

def say_goodbye() -> str:
    """Provides a simple farewell message."""
    print(f"--- Tool: say_goodbye called ---")
    return "さようなら！良い一日をお過ごしください。"

if __name__=="__main__":
    # Example tool usage (optional self-test)
    print(get_weather("New York"))
    print(get_weather("Paris"))