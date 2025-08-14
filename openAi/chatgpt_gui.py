import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
from openai import OpenAI

class ChatGPTGUI:
    def __init__(self):
        """Initialize the GUI ChatGPT application"""
        self.root = tk.Tk()
        self.root.title("ChatGPT Clone - GUI Version")
        self.root.geometry("800x600")
        self.root.configure(bg="#2b2b2b")
        
        # Initialize OpenAI client
        self.setup_openai()
        
        # Conversation history
        self.conversation_history = []
        
        # Setup GUI
        self.setup_gui()
        
    def setup_openai(self):
        """Setup OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            messagebox.showerror(
                "API Key Missing", 
                "Please set your OPENAI_API_KEY environment variable!\n\n"
                "1. Get your API key from: https://platform.openai.com/api-keys\n"
                "2. Set environment variable: $env:OPENAI_API_KEY='your-api-key'\n"
                "3. Restart the application"
            )
            self.root.destroy()
            return
            
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"
        
    def setup_gui(self):
        """Setup the GUI components"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="🤖 ChatGPT Clone", 
            font=("Arial", 16, "bold"),
            bg="#2b2b2b", 
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=("Arial", 10),
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            state=tk.DISABLED
        )
        self.chat_display.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg="#2b2b2b")
        input_frame.pack(padx=20, pady=10, fill=tk.X)
        
        # Message input
        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="#3c3c3c",
            fg="white",
            insertbackground="white"
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", self.send_message)
        
        # Send button
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Arial", 12, "bold"),
            bg="#007acc",
            fg="white",
            cursor="hand2",
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg="#2b2b2b")
        control_frame.pack(padx=20, pady=5, fill=tk.X)
        
        # Clear button
        clear_button = tk.Button(
            control_frame,
            text="Clear Chat",
            font=("Arial", 10),
            bg="#dc3545",
            fg="white",
            cursor="hand2",
            command=self.clear_chat
        )
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Model selection
        model_label = tk.Label(control_frame, text="Model:", bg="#2b2b2b", fg="white")
        model_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.model_var = tk.StringVar(value="gpt-3.5-turbo")
        model_combo = ttk.Combobox(
            control_frame,
            textvariable=self.model_var,
            values=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            state="readonly",
            width=15
        )
        model_combo.pack(side=tk.LEFT)
        model_combo.bind("<<ComboboxSelected>>", self.change_model)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to chat! Type your message and press Enter or click Send.",
            bg="#2b2b2b",
            fg="#888888",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=5)
        
        # Add welcome message
        self.add_message("🤖 Assistant", "Hello! I'm your AI assistant. How can I help you today?", "#007acc")
        
    def add_message(self, sender, message, color="#white"):
        """Add a message to the chat display"""
        self.chat_display.configure(state=tk.NORMAL)
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        # Add sender and message
        self.chat_display.insert(tk.END, f"\n[{timestamp}] {sender}:\n", "sender")
        self.chat_display.insert(tk.END, f"{message}\n", "message")
        
        # Configure tags for styling
        self.chat_display.tag_configure("sender", foreground=color, font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("message", foreground="white")
        
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def send_message(self, event=None):
        """Send message to ChatGPT"""
        message = self.message_entry.get().strip()
        
        if not message:
            return
            
        # Clear input
        self.message_entry.delete(0, tk.END)
        
        # Add user message to display
        self.add_message("🙋 You", message, "#28a745")
        
        # Update status
        self.status_label.config(text="🤔 AI is thinking...")
        self.send_button.config(state=tk.DISABLED, text="Sending...")
        
        # Get AI response in separate thread to prevent GUI freezing
        threading.Thread(target=self.get_ai_response, args=(message,), daemon=True).start()
        
    def get_ai_response(self, user_message):
        """Get response from OpenAI API"""
        try:
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Create messages for API
            messages = [
                {"role": "system", "content": "You are a helpful, friendly, and knowledgeable AI assistant."}
            ] + self.conversation_history
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model_var.get(),
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            # Get response content
            ai_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Keep conversation manageable
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            # Update GUI in main thread
            self.root.after(0, lambda: self.display_ai_response(ai_response))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.display_ai_response(error_msg, is_error=True))
            
    def display_ai_response(self, response, is_error=False):
        """Display AI response in the GUI"""
        color = "#dc3545" if is_error else "#007acc"
        sender = "❌ Error" if is_error else "🤖 Assistant"
        
        self.add_message(sender, response, color)
        
        # Reset status and button
        self.status_label.config(text="Ready for your next message!")
        self.send_button.config(state=tk.NORMAL, text="Send")
        self.message_entry.focus()
        
    def clear_chat(self):
        """Clear the chat display and history"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state=tk.DISABLED)
        
        self.conversation_history = []
        
        # Add welcome message back
        self.add_message("🤖 Assistant", "Chat cleared! How can I help you?", "#007acc")
        
    def change_model(self, event=None):
        """Handle model change"""
        model = self.model_var.get()
        self.status_label.config(text=f"Model changed to: {model}")
        
    def run(self):
        """Start the GUI application"""
        self.message_entry.focus()
        self.root.mainloop()

def main():
    """Main function to run the GUI ChatGPT clone"""
    app = ChatGPTGUI()
    app.run()

if __name__ == "__main__":
    main()
