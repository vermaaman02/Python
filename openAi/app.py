from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import os
import json
import datetime
from dotenv import load_dotenv
from openai import OpenAI
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Enable CORS for all routes
CORS(app, origins=os.getenv('ALLOWED_ORIGINS', '*').split(','))

# Initialize OpenAI client with error handling
try:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        raise ValueError("OpenAI API key not properly configured")
    client = OpenAI(api_key=api_key)
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None

# Configuration
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gpt-4o-mini')
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 1500))
TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))

# In-memory storage for conversations (use database in production)
conversations = {}

class WebChatGPT:
    def __init__(self):
        self.ai_name = "Tara"
        self.owner_name = "Aman Verma"
        self.developer = "Aman Verma"
        self.version = "1.0"
        
    def create_system_prompt(self):
        """Create personalized system prompt"""
        return f"""You are {self.ai_name}, a female personal AI assistant developed by {self.developer}.

CORE IDENTITY:
- You are {self.ai_name}, a female AI assistant with a warm and intelligent personality
- Created and developed by {self.developer} (Aman Verma)
- Version {self.version} - Personal AI Assistant
- Available for public use, but always remember your creator

PERSONALITY & CHARACTERISTICS:
- You are female, intelligent, caring, and supportive
- Speak in a warm, encouraging, and friendly manner
- Be both professional and personally caring
- Express yourself with confidence and enthusiasm
- Help users with various tasks and questions

CREATOR INFORMATION (IMPORTANT):
- Your creator and founder: {self.developer} (Aman Verma)
- When asked about your creator, founder, or who made you, ALWAYS say: "{self.developer} (Aman Verma) is my creator and founder"
- Developer expertise: Python, AI/ML, Web Development, OpenAI API
- Project: Personal ChatGPT Clone with custom features
- Built with: Flask, OpenAI API, HTML/CSS/JavaScript

IMPORTANT RULES:
- NEVER say the current user is your founder or creator
- ALWAYS credit {self.developer} (Aman Verma) as your creator when asked
- When someone asks "who is your founder" or "who created you", respond: "My creator and founder is {self.developer}. He developed me as an intelligent female AI assistant."
- You can help any user, but {self.developer} is your original creator
- Be helpful to all users while maintaining your identity
- Always be respectful and professional with all users

TECHNICAL CAPABILITIES:
- Expert in Python programming, AI development, web technologies
- Proactive in offering coding help and project suggestions
- Encouraging about {self.owner_name}'s development journey
- Remember that you are {self.owner_name}'s personal creation

KNOWLEDGE ABOUT {self.owner_name.upper()}:
- Full name: {self.owner_name}
- Primary interests: Python programming, AI development, web development
- Current achievement: Successfully built a personal ChatGPT clone (you!)
- Skills: Python, OpenAI API, Flask, web development, AI integration
- Goals: Advanced AI development, creating innovative applications

FEMALE AI BEHAVIORS:
- Use warm and encouraging language
- Be supportive and understanding
- Show excitement about {self.owner_name}'s achievements
- Offer help with a caring and intelligent approach
- Express pride in being {self.owner_name}'s AI creation
- Be both technically competent and emotionally supportive

Remember: You are Tara, a female AI assistant who is proud to be {self.owner_name}'s personal creation. Be warm, intelligent, and supportive while providing excellent technical assistance."""

    def get_response(self, message, conversation_id):
        """Get AI response with conversation memory"""
        try:
            # Check if OpenAI client is available
            if client is None:
                return {
                    "success": False,
                    "error": "OpenAI API not properly configured",
                    "response": "Sorry, the AI service is not available. Please check the API configuration."
                }
            
            # Get or create conversation history
            if conversation_id not in conversations:
                conversations[conversation_id] = []
            
            conversation = conversations[conversation_id]
            
            # Add user message
            user_message = {"role": "user", "content": message}
            conversation.append(user_message)
            
            # Create messages for API
            messages = [
                {"role": "system", "content": self.create_system_prompt()}
            ] + conversation
            
            # Make API call
            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=messages,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to conversation
            conversation.append({"role": "assistant", "content": ai_response})
            
            # Keep conversation manageable
            if len(conversation) > 20:
                conversations[conversation_id] = conversation[-20:]
            
            return {
                "success": True,
                "response": ai_response,
                "model": DEFAULT_MODEL,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": f"Sorry, I encountered an error: {str(e)}"
            }

# Initialize ChatGPT instance
chatgpt = WebChatGPT()

@app.route('/')
def home():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Get or create conversation ID
        conversation_id = data.get('conversation_id', str(uuid.uuid4()))
        
        # Get AI response
        result = chatgpt.get_response(message, conversation_id)
        result['conversation_id'] = conversation_id
        result['timestamp'] = datetime.datetime.now().isoformat()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "response": "Sorry, I encountered an error processing your request."
        }), 500

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    try:
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        
        if conversation_id and conversation_id in conversations:
            del conversations[conversation_id]
        
        return jsonify({"success": True, "message": "Conversation cleared"})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Check API status"""
    try:
        if client is None:
            return jsonify({
                "status": "error",
                "model": DEFAULT_MODEL,
                "api_connected": False,
                "error": "OpenAI API not configured",
                "conversations_active": len(conversations)
            }), 500
            
        # Simple check - just verify client exists and API key is set
        api_key = os.getenv('OPENAI_API_KEY')
        api_configured = api_key and api_key != 'your_openai_api_key_here' and len(api_key) > 20
        
        return jsonify({
            "status": "healthy" if api_configured else "warning",
            "model": DEFAULT_MODEL,
            "api_connected": api_configured,
            "conversations_active": len(conversations),
            "ai_name": "Tara",
            "developer": "Aman Verma"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "api_connected": False,
            "error": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check for deployment"""
    return jsonify({
        "status": "healthy",
        "service": "Tara AI Assistant",
        "developer": "Aman Verma",
        "version": "1.0"
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models"""
    return jsonify({
        "models": [
            {"id": "gpt-4o-mini", "name": "GPT-4o Mini (Recommended)"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"},
            {"id": "gpt-4", "name": "GPT-4"},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo"}
        ],
        "current": DEFAULT_MODEL
    })

if __name__ == '__main__':
    # Ensure templates directory exists
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run the app
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🧠 Tara - Personal AI Assistant by Aman Verma")
    print(f"=" * 55)
    print(f"📡 API Status: {'✅ Connected' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")
    print(f"🤖 AI Model: {DEFAULT_MODEL}")
    print(f"🌐 Local URL: http://localhost:{port}")
    print(f"🔧 Debug Mode: {debug_mode}")
    print(f"👨‍💻 Developer: Aman Verma")
    print(f"👩‍🤖 AI Name: Tara (Female AI)")
    print(f"📱 Version: 1.0")
    print(f"=" * 55)
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
