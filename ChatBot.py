from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__) 

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

CHATBOT_NAME = "Maya"
conversation = []

Custom_Inputs = {
    "your name": "My name is Maya",
    "your creator": "My creator is Mridul Gupta",
    "made you": "I was made by Mridul Gupta",
    "create you": "I was created by Mridul Gupta",
    "who are you": "I am Maya the chatbot"
}

def get_gpt_response(user_input):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    
    for key in Custom_Inputs:
        if key in user_input.lower():
            return Custom_Inputs[key]
    
    conversation.append(f"User: {user_input}")
    chat_history = "\n".join(conversation)
    
    response = model.generate_content(chat_history)
    conversation.append(f"{CHATBOT_NAME}: {response.text}")
    
    return response.text

@app.route("/")
def home():
    return "Maya Chatbot is running! Use the /chat endpoint to interact."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    
    if not user_input:
        return jsonify({"response": "Please send a message to chat."})
    
    response = get_gpt_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway uses port 8080
    app.run(host="0.0.0.0", port=port)
