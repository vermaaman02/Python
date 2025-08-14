import os
from openai import OpenAI

def main():
    """Simple command-line ChatGPT clone"""
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("🔑 Enter your OpenAI API key:")
        api_key = input("API Key: ").strip()
        
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return
    
    # Initialize client
    try:
        client = OpenAI(api_key=api_key)
        print("✅ Connected to OpenAI!")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return
    
    print("\n🤖 ChatGPT Clone - Command Line Version")
    print("=" * 50)
    print("Type 'quit' to exit, 'clear' to clear history")
    print("=" * 50)
    
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = input("\n🙋 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
                
            if user_input.lower() == 'clear':
                conversation_history = []
                print("🧹 History cleared!")
                continue
                
            if not user_input:
                continue
            
            # Add to history
            conversation_history.append({"role": "user", "content": user_input})
            
            # Create messages
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."}
            ] + conversation_history
            
            print("🤔 AI is thinking...")
            
            # Make API call
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            # Get response
            ai_response = response.choices[0].message.content
            conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Keep history manageable
            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]
            
            print(f"\n🤖 Assistant: {ai_response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            if "insufficient_quota" in str(e):
                print("💳 Please add billing info at: https://platform.openai.com/account/billing")

if __name__ == "__main__":
    main()
