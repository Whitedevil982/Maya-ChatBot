from flask import Flask, request, jsonify
import google.generativeai as genai
import os
genai.configure(api_key="YOUR_GEMINI_API_KEY")

app = Flask(__name__)

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

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = get_gpt_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
