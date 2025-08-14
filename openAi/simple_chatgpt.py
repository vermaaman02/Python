import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import threading
from openai import OpenAI

class SimpleChatGPT:
    def __init__(self):
        """Initialize the simple ChatGPT GUI"""
        self.root = tk.Tk()
        self.root.title("ChatGPT Clone")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")
        
        # Try to get API key
        self.api_key = self.get_api_key()
        if not self.api_key:
            self.root.destroy()
            return
            
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        self.conversation_history = []
        
        # Setup GUI
        self.setup_gui()
        
    def get_api_key(self):
        """Get API key from environment or ask user"""
        # First try environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            # Ask user for API key
            api_key = simpledialog.askstring(
                "API Key Required",
                "Please enter your OpenAI API key:",
                show='*'
            )
            
        if not api_key:
            messagebox.showerror(
                "No API Key", 
                "OpenAI API key is required to use this application."
            )
            return None
            
        return api_key
        
    def setup_gui(self):
        """Setup the GUI components"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="🤖 ChatGPT Clone", 
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=10)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Arial", 10),
            state=tk.DISABLED
        )
        self.chat_display.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(padx=20, pady=10, fill=tk.X)
        
        # Message input
        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 12)
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", self.send_message)
        
        # Send button
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Arial", 12),
            bg="#007acc",
            fg="white",
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Clear button
        clear_button = tk.Button(
            self.root,
            text="Clear Chat",
            font=("Arial", 10),
            bg="#dc3545",
            fg="white",
            command=self.clear_chat
        )
        clear_button.pack(pady=5)
        
        # Add welcome message
        self.add_message("🤖 Assistant", "Hello! I'm your AI assistant. How can I help you today?")
        
    def add_message(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{sender}:\n{message}\n")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def send_message(self, event=None):
        """Send message to ChatGPT"""
        message = self.message_entry.get().strip()
        
        if not message:
            return
            
        # Clear input
        self.message_entry.delete(0, tk.END)
        
        # Add user message
        self.add_message("🙋 You", message)
        
        # Disable send button
        self.send_button.config(state=tk.DISABLED, text="Sending...")
        
        # Get AI response in background
        threading.Thread(target=self.get_ai_response, args=(message,), daemon=True).start()
        
    def get_ai_response(self, user_message):
        """Get response from OpenAI API"""
        try:
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Create messages for API
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."}
            ] + self.conversation_history
            
            # Make API call
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            # Get response
            ai_response = response.choices[0].message.content
            
            # Add to history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Keep history manageable
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            # Update GUI
            self.root.after(0, lambda: self.display_ai_response(ai_response))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.display_ai_response(error_msg, is_error=True))
            
    def display_ai_response(self, response, is_error=False):
        """Display AI response in GUI"""
        sender = "❌ Error" if is_error else "🤖 Assistant"
        self.add_message(sender, response)
        
        # Re-enable send button
        self.send_button.config(state=tk.NORMAL, text="Send")
        self.message_entry.focus()
        
    def clear_chat(self):
        """Clear the chat"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state=tk.DISABLED)
        self.conversation_history = []
        self.add_message("🤖 Assistant", "Chat cleared! How can I help you?")
        
    def run(self):
        """Start the application"""
        if hasattr(self, 'client'):  # Only run if we have a valid client
            self.message_entry.focus()
            self.root.mainloop()

def main():
    """Main function"""
    try:
        app = SimpleChatGPT()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()
