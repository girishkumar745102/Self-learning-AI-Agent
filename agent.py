"""
agent.py
---------
This is the main agent that:
1. Takes the user's message
2. Finds relevant past memories
3. Generates a response using the LLM (using memory as context)
4. Saves the new message to memory as well (so it can be remembered next time)
"""


from memory import MemoryManager
from llm import generate_response

class SelfLearningAgent:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.memory = MemoryManager()

    def chat(self, user_message: str) -> str:
        relevant_memories = self.memory.search_memory(
            user_id= self.user_id, query=user_message
        )

        reply = generate_response(user_message , relevant_memories)

        self.memory.add_memory(self.user_id, user_message)

        return reply

if __name__ == "__main__":
    agent = SelfLearningAgent(user_id="girish_test")

    print("start chat(write exit to stop)\n")
    while True:
        msg = input("you: ")
        if msg.lower() == "exit":
            break
        reply = agent.chat(msg)
        print("Agent:", reply, "\n")
