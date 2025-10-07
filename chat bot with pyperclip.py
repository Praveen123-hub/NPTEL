import google.generativeai as genai
import pyperclip

genai.configure(api_key="") #for gemini api key
model = genai.GenerativeModel("gemini-pro-latest")

print("Chatbot initiated. Type 'quit' or 'exit' to end the conversation.")

while True:
    message = input("Man : ")
    if message.lower() in ["quit", "exit"]:
        print("Bot : Goodbye!")
        break

    response = model.generate_content(f"Give a short paragraph answer: {message}")
    reply = response.text

    print("Bot :", reply)

    pyperclip.copy(reply)
    print("---------------Copied to clipboard! You can paste it directly in Word.------------------")


