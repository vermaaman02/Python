import os
from openai import OpenAI

# Initialize the OpenAI client
# You'll need to set your API key as an environment variable or replace with your actual key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Make sure to set this environment variable
)

def simple_chat():
    """Simple one-time chat with ChatGPT"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using gpt-3.5-turbo (gpt-5 doesn't exist yet)
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
            ]
        )
        
        print("ChatGPT Response:")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set your OPENAI_API_KEY environment variable")

if __name__ == "__main__":
    simple_chat()