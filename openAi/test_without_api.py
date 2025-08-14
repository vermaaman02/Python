"""
ChatGPT Clone - Demo Version (No API Key Required)
This demonstrates the interface without actually calling OpenAI
"""

import time
import random

class MockChatGPT:
    """Mock version of ChatGPT for testing without API key"""
    
    def __init__(self):
        self.responses = [
            "That's an interesting question! I'd be happy to help you with that.",
            "I understand what you're asking. Let me think about this...",
            "Great question! Here's what I think about that topic.",
            "That's a fascinating point. I can provide some insights on this.",
            "I see what you mean. Let me give you a detailed response.",
            "Excellent question! This is definitely worth exploring.",
            "I appreciate you asking about this. Here's my perspective.",
            "That's a really good question that many people wonder about."
        ]
        
    def get_response(self, user_input):
        """Simulate AI response with delay"""
        # Simulate thinking time
        time.sleep(1)
        
        # Return a mock response
        base_response = random.choice(self.responses)
        return f"{base_response}\n\n(This is a demo response - connect your real OpenAI API key for actual AI responses!)"

def main():
    print("🤖 ChatGPT Clone - DEMO MODE")
    print("=" * 50)
    print("This is a demo version that works WITHOUT an API key!")
    print("Responses are simulated. Set up your API key for real AI responses.")
    print("=" * 50)
    print("Commands: 'quit' to exit")
    print()
    
    chat = MockChatGPT()
    
    while True:
        try:
            user_input = input("🙋 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Thanks for trying the demo!")
                break
                
            if not user_input:
                continue
                
            print("🤔 AI is thinking...")
            response = chat.get_response(user_input)
            print(f"🤖 Demo AI: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Demo ended!")
            break

if __name__ == "__main__":
    main()
