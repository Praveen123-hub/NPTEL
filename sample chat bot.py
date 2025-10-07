import google.generativeai as genai

genai.configure(api_key="")

model = genai.GenerativeModel("gemini-pro-latest")

print("Chatbot initiated. Type 'quit' or 'exit' to end the conversation.")

while True:
    message = input("Man : ")
    if message.lower() in ["quit", "exit"]:
        print("Bot : Goodbye!")
        break

    response = model.generate_content(message)
    reply = response.text
    print("Bot :", reply)





