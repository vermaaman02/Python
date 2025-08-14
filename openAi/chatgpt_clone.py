import os
import sys
from openai import OpenAI
from datetime import datetime

class ChatGPTClone:
    def __init__(self):
        """Initialize the ChatGPT clone with OpenAI client"""
        # You need to set your OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("⚠️  OPENAI_API_KEY environment variable not found!")
            print("Please set your OpenAI API key:")
            print("1. Get your API key from: https://platform.openai.com/api-keys")
            print("2. Set environment variable: $env:OPENAI_API_KEY='your-api-key'")
            sys.exit(1)
            
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []
        self.model = "gpt-3.5-turbo"  # You can change to "gpt-4" if you have access
        
        # System message to set the assistant's behavior
        self.system_message = {
            "role": "system", 
            "content": "You are a helpful, friendly, and knowledgeable AI assistant. Provide clear, accurate, and helpful responses."
        }
        
    def display_welcome(self):
        """Display welcome message"""
        print("🤖 Welcome to ChatGPT Clone!")
        print("=" * 50)
        print("Type your messages and press Enter to chat.")
        print("Commands:")
        print("  - 'quit' or 'exit' to end the conversation")
        print("  - 'clear' to clear conversation history")
        print("  - 'history' to view conversation history")
        print("  - 'model' to change AI model")
        print("=" * 50)
        print()
        
    def get_response(self, user_input):
        """Get response from OpenAI API"""
        try:
            # Add user message to conversation
            user_message = {"role": "user", "content": user_input}
            
            # Create messages list with system message and conversation history
            messages = [self.system_message] + self.conversation_history + [user_message]
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            # Extract the assistant's response
            assistant_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append(user_message)
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Keep conversation history manageable (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
                
            return assistant_response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("🧹 Conversation history cleared!")
        
    def show_history(self):
        """Display conversation history"""
        if not self.conversation_history:
            print("📝 No conversation history yet.")
            return
            
        print("\n📝 Conversation History:")
        print("-" * 30)
        for i, message in enumerate(self.conversation_history):
            role = "🙋 You" if message["role"] == "user" else "🤖 Assistant"
            print(f"{role}: {message['content'][:100]}{'...' if len(message['content']) > 100 else ''}")
        print("-" * 30)
        
    def change_model(self):
        """Change the AI model"""
        print("\nAvailable models:")
        print("1. gpt-3.5-turbo (faster, cheaper)")
        print("2. gpt-4 (more capable, requires access)")
        print("3. gpt-4-turbo (latest GPT-4 model)")
        
        choice = input("Choose model (1-3): ").strip()
        
        models = {
            "1": "gpt-3.5-turbo",
            "2": "gpt-4", 
            "3": "gpt-4-turbo"
        }
        
        if choice in models:
            self.model = models[choice]
            print(f"✅ Model changed to: {self.model}")
        else:
            print("❌ Invalid choice. Model unchanged.")
    
    def chat(self):
        """Main chat loop"""
        self.display_welcome()
        
        while True:
            try:
                # Get user input
                user_input = input("🙋 You: ").strip()
                
                if not user_input:
                    continue
                    
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye! Thanks for chatting!")
                    break
                    
                elif user_input.lower() == 'clear':
                    self.clear_history()
                    continue
                    
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                    
                elif user_input.lower() == 'model':
                    self.change_model()
                    continue
                
                # Get and display AI response
                print("🤖 Assistant: ", end="")
                response = self.get_response(user_input)
                print(response)
                print()  # Add spacing
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")

def main():
    """Main function to run the ChatGPT clone"""
    chat_app = ChatGPTClone()
    chat_app.chat()

if __name__ == "__main__":
    main()
