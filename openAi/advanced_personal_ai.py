import os
import json
import datetime
from openai import OpenAI

class AdvancedPersonalAI:
    def __init__(self):
        """Initialize your Advanced Personal AI"""
        
        # Load configuration
        self.config = self.load_config()
        
        # Get API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("🔑 Enter your OpenAI API key:")
            self.api_key = input("API Key: ").strip()
        
        self.client = OpenAI(api_key=self.api_key)
        
        # AI Identity
        self.ai_name = self.config["ai_config"]["name"]
        self.owner_name = self.config["owner_profile"]["name"].split()[0]  # First name
        
        # Memory system
        self.memory_file = "advanced_memory.json"
        self.memory = self.load_memory()
        
        # Learning system
        self.learning_file = "ai_learning.json"
        self.learned_patterns = self.load_learning()
        
        # Conversation history
        self.conversation_history = []
        
    def load_config(self):
        """Load AI configuration"""
        try:
            with open("ai_config.json", 'r') as f:
                return json.load(f)
        except:
            # Default config if file not found
            return {
                "ai_config": {"name": "ARIA"},
                "owner_profile": {"name": "Aman Verma", "interests": []},
                "behavior_settings": {},
                "advanced_features": {}
            }
    
    def load_memory(self):
        """Load enhanced memory system"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            "personal_facts": [],
            "preferences": {},
            "goals": [],
            "achievements": [],
            "project_progress": {},
            "conversation_summaries": [],
            "important_dates": {},
            "learning_interests": [],
            "code_preferences": {},
            "favorite_topics": []
        }
    
    def load_learning(self):
        """Load AI learning patterns"""
        try:
            if os.path.exists(self.learning_file):
                with open(self.learning_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            "communication_patterns": [],
            "frequent_topics": {},
            "response_preferences": {},
            "interaction_style": {}
        }
    
    def save_data(self):
        """Save all data files"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
            with open(self.learning_file, 'w') as f:
                json.dump(self.learned_patterns, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save data: {e}")
    
    def create_dynamic_system_prompt(self):
        """Create a dynamic system prompt based on current memory and learning"""
        
        # Base personality from config
        personality = self.config["ai_config"]["personality"]
        owner_profile = self.config["owner_profile"]
        
        # Recent memories
        recent_facts = self.memory["personal_facts"][-5:] if self.memory["personal_facts"] else []
        recent_goals = self.memory["goals"][-3:] if self.memory["goals"] else []
        current_projects = self.memory["project_progress"]
        
        prompt = f"""You are {self.ai_name}, {self.owner_name}'s advanced personal AI assistant.

CORE IDENTITY:
- You are {personality.get('traits', ['intelligent', 'helpful'])} 
- Communication style: {personality.get('communication_style', 'friendly')}
- You specialize in: {', '.join(personality.get('expertise', ['general assistance']))}

ABOUT {self.owner_name.upper()}:
- Full name: {owner_profile['name']}
- Primary interests: {', '.join(owner_profile.get('interests', []))}
- Current projects: {', '.join(owner_profile.get('current_projects', []))}
- Goals: {', '.join(owner_profile.get('goals', []))}

RECENT PERSONAL MEMORY:
"""
        
        if recent_facts:
            prompt += "\nRecent facts learned:\n"
            for fact in recent_facts:
                if isinstance(fact, dict):
                    prompt += f"- {fact.get('content', fact)}\n"
                else:
                    prompt += f"- {fact}\n"
        
        if recent_goals:
            prompt += "\nCurrent goals:\n"
            for goal in recent_goals:
                if isinstance(goal, dict):
                    prompt += f"- {goal.get('content', goal)}\n"
                else:
                    prompt += f"- {goal}\n"
        
        if current_projects:
            prompt += "\nActive projects:\n"
            for project, status in current_projects.items():
                prompt += f"- {project}: {status}\n"
        
        prompt += f"""
BEHAVIOR GUIDELINES:
- Always be personal and reference {self.owner_name}'s specific interests
- Proactively offer help with coding and AI projects
- Remember and build upon previous conversations
- Suggest next steps and improvements for projects
- Be encouraging about {self.owner_name}'s learning journey
- Adapt your responses based on {self.owner_name}'s preferences

CURRENT CONVERSATION CONTEXT:
This is a continuation of your ongoing relationship with {self.owner_name}. 
Reference shared history and be genuinely helpful as their personal AI assistant."""

        return prompt
    
    def intelligent_learning(self, user_input, ai_response):
        """Advanced learning from conversations"""
        user_lower = user_input.lower()
        
        # Learn preferences
        preference_indicators = ["i prefer", "i like", "i love", "i hate", "i don't like"]
        for indicator in preference_indicators:
            if indicator in user_lower:
                self.add_to_memory("preferences", {
                    "statement": user_input,
                    "preference_type": indicator,
                    "extracted": user_input[user_input.lower().find(indicator):].strip()
                })
        
        # Learn goals and aspirations
        goal_indicators = ["i want to", "my goal", "i plan to", "i hope to", "i'm trying to"]
        for indicator in goal_indicators:
            if indicator in user_lower:
                self.add_to_memory("goals", {
                    "statement": user_input,
                    "goal_type": indicator,
                    "date_mentioned": datetime.datetime.now().isoformat()
                })
        
        # Track project progress
        project_indicators = ["working on", "building", "creating", "developing", "finished", "completed"]
        for indicator in project_indicators:
            if indicator in user_lower:
                project_name = self.extract_project_name(user_input)
                if project_name:
                    self.memory["project_progress"][project_name] = {
                        "status": indicator,
                        "last_update": datetime.datetime.now().isoformat(),
                        "details": user_input
                    }
        
        # Learn conversation patterns
        self.learned_patterns["frequent_topics"][user_lower[:20]] = self.learned_patterns["frequent_topics"].get(user_lower[:20], 0) + 1
        
        self.save_data()
    
    def extract_project_name(self, text):
        """Extract project name from text (basic implementation)"""
        text_lower = text.lower()
        
        # Common project keywords
        project_keywords = ["chatgpt", "ai", "bot", "app", "website", "script", "program", "project"]
        
        for keyword in project_keywords:
            if keyword in text_lower:
                # Simple extraction - can be improved
                return keyword.capitalize() + " Project"
        
        return None
    
    def add_to_memory(self, category, item):
        """Add item to memory with timestamp"""
        if category not in self.memory:
            self.memory[category] = []
        
        memory_item = {
            "timestamp": datetime.datetime.now().isoformat(),
            "content": item
        }
        
        self.memory[category].append(memory_item)
        
        # Keep memory manageable
        if len(self.memory[category]) > 50:
            self.memory[category] = self.memory[category][-50:]
    
    def get_response(self, user_input):
        """Get intelligent response with learning"""
        try:
            # Create dynamic system prompt
            system_prompt = self.create_dynamic_system_prompt()
            
            # Add user message
            user_message = {"role": "user", "content": user_input}
            
            # Create messages
            messages = [
                {"role": "system", "content": system_prompt}
            ] + self.conversation_history + [user_message]
            
            # API call with enhanced parameters
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=1500,
                temperature=0.9,  # Higher creativity for personality
                presence_penalty=0.2,  # Encourage diverse topics
                frequency_penalty=0.1,  # Reduce repetition
                top_p=0.95
            )
            
            ai_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append(user_message)
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Intelligent learning
            self.intelligent_learning(user_input, ai_response)
            
            # Keep conversation manageable
            if len(self.conversation_history) > 24:
                # Summarize old conversations before removing
                self.summarize_old_conversation()
                self.conversation_history = self.conversation_history[-20:]
            
            return ai_response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def summarize_old_conversation(self):
        """Summarize old conversations for memory"""
        if len(self.conversation_history) > 10:
            old_conv = self.conversation_history[:10]
            summary = f"Previous conversation on {datetime.datetime.now().date()}: "
            summary += f"Discussed {len(old_conv)//2} topics including "
            
            # Extract key topics (simple implementation)
            topics = []
            for msg in old_conv:
                if msg["role"] == "user":
                    words = msg["content"].lower().split()
                    topics.extend([w for w in words if len(w) > 5])
            
            summary += ", ".join(list(set(topics))[:5])
            self.add_to_memory("conversation_summaries", summary)
    
    def show_advanced_memory(self):
        """Display comprehensive memory"""
        print(f"\n🧠 {self.ai_name}'s Advanced Memory about {self.owner_name}")
        print("=" * 60)
        
        categories = [
            ("Recent Goals", "goals"),
            ("Project Progress", "project_progress"),
            ("Preferences", "preferences"),
            ("Personal Facts", "personal_facts"),
            ("Learning Interests", "learning_interests")
        ]
        
        for title, category in categories:
            if category in self.memory and self.memory[category]:
                print(f"\n📝 {title}:")
                
                if isinstance(self.memory[category], dict):
                    for key, value in list(self.memory[category].items())[-3:]:
                        print(f"  • {key}: {value}")
                else:
                    for item in self.memory[category][-3:]:
                        if isinstance(item, dict):
                            content = item.get("content", item)
                            if isinstance(content, dict):
                                print(f"  • {content.get('statement', str(content)[:50])}")
                            else:
                                print(f"  • {str(content)[:80]}")
                        else:
                            print(f"  • {str(item)[:80]}")
        
        # Show learning patterns
        if self.learned_patterns["frequent_topics"]:
            print(f"\n🎯 Most Discussed Topics:")
            sorted_topics = sorted(self.learned_patterns["frequent_topics"].items(), 
                                 key=lambda x: x[1], reverse=True)
            for topic, count in sorted_topics[:5]:
                print(f"  • {topic.capitalize()}: {count} times")
        
        print()
    
    def chat(self):
        """Start advanced personal AI chat"""
        print(f"🤖 {self.ai_name} - Advanced Personal AI for {self.owner_name}")
        print("=" * 70)
        print(f"Hello {self.owner_name}! I'm your advanced personal AI assistant.")
        print("I learn from our conversations and adapt to your preferences.")
        print(f"\nMemory: {len(self.memory.get('personal_facts', []))} facts, "
              f"{len(self.memory.get('goals', []))} goals, "
              f"{len(self.memory.get('project_progress', {}))} projects tracked")
        print("\nCommands:")
        print("  • 'memory' - View my detailed memory about you")
        print("  • 'clear' - Clear current conversation (keep memory)")
        print("  • 'reset' - Reset all memory (start fresh)")
        print("  • 'quit' - Exit")
        print("=" * 70)
        
        while True:
            try:
                user_input = input(f"\n💬 {self.owner_name}: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n🤖 {self.ai_name}: Goodbye {self.owner_name}! I'll remember everything and "
                          f"continue learning about you. See you next time! 👋")
                    break
                
                elif user_input.lower() == 'memory':
                    self.show_advanced_memory()
                    continue
                
                elif user_input.lower() == 'clear':
                    self.conversation_history = []
                    print(f"\n🤖 {self.ai_name}: Conversation cleared! I still remember everything about you though.")
                    continue
                
                elif user_input.lower() == 'reset':
                    confirm = input("Are you sure you want to reset all memory? (yes/no): ")
                    if confirm.lower() == 'yes':
                        self.memory = self.load_memory().__class__()  # Reset to empty
                        self.learned_patterns = self.load_learning().__class__()  # Reset to empty
                        print(f"\n🤖 {self.ai_name}: Memory reset! Starting fresh.")
                    continue
                
                if not user_input:
                    continue
                
                print(f"\n🤖 {self.ai_name}: ", end="")
                response = self.get_response(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print(f"\n\n🤖 {self.ai_name}: Until next time, {self.owner_name}! 👋")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Main function"""
    try:
        ai = AdvancedPersonalAI()
        ai.chat()
    except Exception as e:
        print(f"Error starting Advanced Personal AI: {e}")

if __name__ == "__main__":
    main()
