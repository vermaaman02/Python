import os
from openai import OpenAI

def check_api_status():
    """Check if the OpenAI API is working and provide helpful error messages"""
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No API key found!")
        print("Please set your API key:")
        print('$env:OPENAI_API_KEY = "your-api-key"')
        return False
    
    print("✅ API key found!")
    print(f"Key starts with: {api_key[:10]}...")
    
    # Test the API connection
    try:
        client = OpenAI(api_key=api_key)
        
        # Try a minimal API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        print("✅ API connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ API Error: {error_msg}")
        
        if "insufficient_quota" in error_msg:
            print("\n🔧 SOLUTION:")
            print("1. Check your usage: https://platform.openai.com/usage")
            print("2. Add billing info: https://platform.openai.com/account/billing")
            print("3. You might have used up your free credits")
            print("4. API usage costs money, but it's very affordable")
            
        elif "invalid_api_key" in error_msg:
            print("\n🔧 SOLUTION:")
            print("1. Check your API key is correct")
            print("2. Get a new key: https://platform.openai.com/api-keys")
            
        elif "model_not_found" in error_msg:
            print("\n🔧 SOLUTION:")
            print("1. You might not have access to this model")
            print("2. Try with gpt-3.5-turbo")
            
        return False

def main():
    print("🔍 OpenAI API Status Checker")
    print("=" * 40)
    
    if check_api_status():
        print("\n🎉 Your API is ready! You can now use:")
        print("- chatgpt_clone.py (command line)")
        print("- chatgpt_gui.py (GUI version)")
    else:
        print("\n⚠️  Please fix the issues above before using the ChatGPT clone")

if __name__ == "__main__":
    main()
