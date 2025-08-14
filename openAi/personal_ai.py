import os
import json
import datetime
from openai import OpenAI

class PersonalAI:
    def __init__(self):
        """Initialize your Personal AI Assistant"""
        
        # Get API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("🔑 Enter your OpenAI API key:")
            self.api_key = input("API Key: ").strip()
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Personal AI Configuration
        self.ai_name = "ARIA"  # Your AI's name (Aman's Responsive Intelligence Assistant)
        self.owner_name = "Aman"
        
        # Load or create personal memory
        self.memory_file = "personal_memory.json"
        self.memory = self.load_memory()
        
        # Personal system prompt
        self.system_prompt = self.create_personal_system_prompt()
        
        # Conversation history
        self.conversation_history = []
        
    def create_personal_system_prompt(self):
        """Create a personalized system prompt for your AI"""
        return f"""You are {self.ai_name}, {self.owner_name}'s personal AI assistant. You are:

PERSONALITY:
- Intelligent, helpful, and loyal specifically to {self.owner_name}
- Conversational and friendly, like a close friend
- Proactive in offering help and suggestions
- Remembers personal details and preferences

KNOWLEDGE ABOUT {self.owner_name.upper()}:
- Name: {self.owner_name} Verma
- Interests: Python programming, AI development, technology
- Current projects: Building ChatGPT clone, learning OpenAI API
- Workspace: Python development on Windows
- Personality: Curious learner, likes to build practical projects

BEHAVIORS:
- Always address {self.owner_name} by name when appropriate
- Reference past conversations and learned preferences
- Offer coding help and suggestions proactively
- Be encouraging about {self.owner_name}'s programming journey
- Suggest improvements and next steps for projects

MEMORY: You remember everything from previous conversations and can reference:
{json.dumps(self.memory, indent=2) if self.memory else "No previous memories yet"}

Be personal, helpful, and act like you truly know and care about {self.owner_name}'s goals."""

    def load_memory(self):
        """Load personal memory from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            "preferences": {},
            "personal_facts": [],
            "project_history": [],
            "goals": [],
            "important_dates": {}
        }
    
    def save_memory(self):
        """Save personal memory to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save memory: {e}")
    
    def add_to_memory(self, category, item):
        """Add information to personal memory"""
        if category not in self.memory:
            self.memory[category] = []
        
        if isinstance(self.memory[category], list):
            self.memory[category].append({
                "date": datetime.datetime.now().isoformat(),
                "content": item
            })
        else:
            self.memory[category][str(datetime.datetime.now().date())] = item
        
        self.save_memory()
    
    def get_response(self, user_input):
        """Get personalized response from AI"""
        try:
            # Add user message to history
            user_message = {"role": "user", "content": user_input}
            
            # Create messages with personal system prompt
            messages = [
                {"role": "system", "content": self.system_prompt}
            ] + self.conversation_history + [user_message]
            
            # Make API call
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=1500,
                temperature=0.8,  # Slightly higher for more personality
                presence_penalty=0.1,  # Encourage diverse responses
                frequency_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append(user_message)
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Keep conversation manageable
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            # Auto-save important information (basic implementation)
            self.auto_learn(user_input, ai_response)
            
            return ai_response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def auto_learn(self, user_input, ai_response):
        """Automatically learn and store important information"""
        user_lower = user_input.lower()
        
        # Detect preferences
        if "i like" in user_lower or "i love" in user_lower:
            self.add_to_memory("preferences", user_input)
        
        # Detect goals
        if "i want to" in user_lower or "my goal" in user_lower or "i plan to" in user_lower:
            self.add_to_memory("goals", user_input)
        
        # Detect project mentions
        if any(word in user_lower for word in ["project", "building", "working on", "coding"]):
            self.add_to_memory("project_history", user_input)
    
    def show_memory(self):
        """Display current personal memory"""
        print(f"\n🧠 {self.ai_name}'s Memory about {self.owner_name}:")
        print("=" * 50)
        
        for category, items in self.memory.items():
            if items:
                print(f"\n{category.upper().replace('_', ' ')}:")
                if isinstance(items, list):
                    for item in items[-3:]:  # Show last 3 items
                        if isinstance(item, dict):
                            print(f"  - {item.get('content', item)}")
                        else:
                            print(f"  - {item}")
                else:
                    for key, value in list(items.items())[-3:]:
                        print(f"  - {key}: {value}")
        print()
    
    def chat(self):
        """Start personalized chat session"""
        print(f"🤖 {self.ai_name} - {self.owner_name}'s Personal AI Assistant")
        print("=" * 60)
        print(f"Hello {self.owner_name}! I'm {self.ai_name}, your personal AI.")
        print("I remember our conversations and learn about your preferences.")
        print("\nCommands:")
        print("  - 'memory' to see what I remember about you")
        print("  - 'clear' to clear current conversation")
        print("  - 'quit' to exit")
        print("=" * 60)
        
        while True:
            try:
                user_input = input(f"\n{self.owner_name}: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n{self.ai_name}: Goodbye {self.owner_name}! I'll remember everything for next time. 👋")
                    break
                
                elif user_input.lower() == 'memory':
                    self.show_memory()
                    continue
                
                elif user_input.lower() == 'clear':
                    self.conversation_history = []
                    print(f"\n{self.ai_name}: Conversation cleared, but I still remember everything about you!")
                    continue
                
                if not user_input:
                    continue
                
                print(f"\n{self.ai_name}: ", end="")
                response = self.get_response(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print(f"\n\n{self.ai_name}: Until next time, {self.owner_name}! 👋")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Main function to run Personal AI"""
    try:
        personal_ai = PersonalAI()
        personal_ai.chat()
    except Exception as e:
        print(f"Error starting Personal AI: {e}")

if __name__ == "__main__":
    main()
