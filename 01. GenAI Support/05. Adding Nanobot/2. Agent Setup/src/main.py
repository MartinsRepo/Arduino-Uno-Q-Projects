import sys
import os
import json
import time
import asyncio
from pathlib import Path
from nanobot.providers import LiteLLMProvider

# Setup Path
CONFIG_PATH = "/app/nanobot/config.json"

try:
    with open(CONFIG_PATH, 'r') as f:
        config_data = json.load(f)
    # Extract values from the JSON structure
    openai_key = config_data.get("providers", {}).get("openai", {}).get("apiKey")
    target_model = config_data.get("agents", {}).get("defaults", {}).get("model", "openai/gpt-4o-mini")

    # Initialize Provider with explicit keyword arguments
    # This prevents the model name from being treated as the API key
    provider = LiteLLMProvider(
        api_key=openai_key,
        default_model=target_model
    )
    print(f"AI Provider ready. Using model: {provider.default_model}")

except FileNotFoundError:
    print(f"Error: Could not find config at {CONFIG_PATH}")
    provider = None
except Exception as e:
    print(f"Initialization Error: {e}")
    provider = None

# Imports
from arduino.app_utils import Bridge
from nanobot.agent.loop import AgentLoop
from nanobot.bus import MessageBus, InboundMessage

# Initialization
print("Initializing Nanobot system...")

# Force LiteLLM to use OpenAI logic
os.environ["LITELLM_ALREADY_SET"] = "True"

bus = MessageBus()
workspace_path = Path("/app/nanobot/workspace")

agent_loop = None
try:
    agent_loop = AgentLoop(bus, provider, workspace_path)
    print("Nanobot AgentLoop successfully initialized!")
except Exception as e:
    print(f"Failed to initialize AgentLoop: {e}")

async def process_prompt(prompt):
    try:
        # Create the message with required metadata
        message = InboundMessage(
            content=prompt,
            channel="arduino",
            sender_id="physical_user",
            chat_id="arduino_serial"
        )
        
        # Publish to the specific 'inbound' method found in your queue.py
        await bus.publish_inbound(message)
        
        # Start the agent processing
        # We wrap this in a task so it doesn't block us from consuming the result
        loop_task = asyncio.create_task(agent_loop.run())
        
        # Wait for the agent to push a response to the outbound queue
        # This matches the 'consume_outbound' method in your queue.py
        print("Waiting for agent to process...")
        outbound_msg = await bus.consume_outbound()
        
        return str(outbound_msg.content)
    except Exception as e:
        return f"Agent Runtime Error: {e}"

def main():
    if Bridge is None or agent_loop is None:
        return

    prompt = Bridge.call("nanobot/get_prompt")

    if prompt and len(prompt.strip()) > 0:
        print(f"Arduino Prompt: {prompt}")
        
        try:
            # Run the async logic
            response_text = asyncio.run(process_prompt(prompt))
        except Exception as e:
            response_text = f"Bridge Async Error: {e}"

        print(f"Agent Response: {response_text}")
        Bridge.call("nanobot/set_response", response_text)

if __name__ == "__main__":
    print("Python Bridge monitoring active...")
    while True:
        try:
            main()
        except Exception as e:
            print(f"Loop error: {e}")
        time.sleep(1)