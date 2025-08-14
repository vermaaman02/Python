import os
from openai import OpenAI

def test_haiku():
    """Test the exact same request as your curl command"""
    
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No API key found!")
        return
    
    print("🤖 Testing OpenAI API with Haiku Request")
    print("=" * 50)
    print(f"API Key: {api_key[:15]}...")
    print("Model: gpt-4o-mini")
    print("Request: write a haiku about ai")
    print("=" * 50)
    
    try:
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "write a haiku about ai"}
            ],
            max_tokens=50
        )
        
        haiku = response.choices[0].message.content
        print("✅ SUCCESS! Here's your AI haiku:")
        print("-" * 30)
        print(haiku)
        print("-" * 30)
        
        # Show usage info
        usage = response.usage
        print(f"\n📊 Token Usage:")
        print(f"Input tokens: {usage.prompt_tokens}")
        print(f"Output tokens: {usage.completion_tokens}")
        print(f"Total tokens: {usage.total_tokens}")
        
        # Estimate cost (rough)
        input_cost = (usage.prompt_tokens / 1_000_000) * 0.15
        output_cost = (usage.completion_tokens / 1_000_000) * 0.60
        total_cost = input_cost + output_cost
        print(f"Estimated cost: ${total_cost:.6f}")
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error: {error_msg}")
        
        if "insufficient_quota" in error_msg:
            print("\n💳 BILLING SETUP REQUIRED:")
            print("1. Go to: https://platform.openai.com/account/billing")
            print("2. Add a payment method")
            print("3. Set a usage limit (recommended: $10/month)")
            print("4. The API is pay-per-use but very affordable!")
            
        elif "invalid_api_key" in error_msg:
            print("\n🔑 API KEY ISSUE:")
            print("1. Check your API key is correct")
            print("2. Make sure it hasn't expired")
            print("3. Get a new one: https://platform.openai.com/api-keys")

if __name__ == "__main__":
    test_haiku()
