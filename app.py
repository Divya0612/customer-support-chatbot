import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from persona import CUSTOMER_SUPPORT_PROMPT
from rag import build_index, retrieve
from tool_definitions import TOOL_DEFINITIONS
import tools
import time

load_dotenv()

HISTORY_FILE = "chat_history.json"

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
            return [
                msg for msg in data
                if msg.get("parts") and msg["parts"][0].get("text")
            ]
        except Exception as e:
            print(f"Could not load history: {e}")
    return []


def save_history(chat_history):
    data = []
    for msg in chat_history:
        if not msg.parts:
            continue
        text = msg.parts[0].text
        if not text:
            continue
        data.append({"role": msg.role, "parts": [{"text": text}]})
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Could not save history: {e}")


history = load_history()

print("Building knowledge base index...")
knowledge_index = build_index()
print(f"Ready. Indexed {len(knowledge_index)} knowledge chunks.\n")


def search_knowledge_base(query: str) -> str:
    chunks = retrieve(query, knowledge_index, top_k=3)
    return "\n\n".join(
        f"[{chunk['source']}]\n{chunk['text']}" for chunk in chunks
    )


chat = client.chats.create(
    model="gemini-3.6-flash",
    config=dict(system_instruction=CUSTOMER_SUPPORT_PROMPT, tools=TOOL_DEFINITIONS),
    history=history,
)

TOOL_FUNCTIONS = {
    "track_order": tools.track_order,
    "cancel_order": tools.cancel_order,
    "check_refund_status": tools.check_refund_status,
    "connect_human_agent": tools.connect_human_agent,
    "search_knowledge_base": search_knowledge_base,
}


def get_response(user_input):
    user_input = user_input.strip()

    if user_input.lower() in ["exit", "quit"]:
        return None

    try:
        response = chat.send_message(user_input)

        # Loop until the model stops calling tools and returns a text reply.
        while response.candidates[0].content.parts[0].function_call:
            func_call = response.candidates[0].content.parts[0].function_call
            func_name = func_call.name
            func_args = dict(func_call.args)

            tool_result = TOOL_FUNCTIONS[func_name](**func_args)

            response = chat.send_message(
                types.Part(
                    function_response=types.FunctionResponse(
                        name=func_name,
                        response={"result": tool_result},
                    )
                )
            )

        current_history = getattr(chat, "history", getattr(chat, "get_history", lambda: [])())
        if callable(current_history):
            current_history = current_history()
        save_history(current_history)

        return response.text
    except Exception as e:
        return f"An error occurred: {e}"


def main():
    print("Chatbot started! Type your message to talk, or 'quit' to exit.")
    if history:
        print(f"(Loaded {len(history)} past messages from memory)")
    print("-" * 50)

    while True:
        try:
            user_input = input("You: ")
            if not user_input.strip():
                continue

            start = time.time()

            response = get_response(user_input)
            
            end = time.time()
            elapsed = time.time() - start
            print(f"API call took {elapsed:.3f} seconds")

            if response is None:
                print("Bot: Goodbye!")
                break

            print(f"Bot: {response}")

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye!")
            break


if __name__ == "__main__":
    main()
