from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
messages=[
    {"role":"system",
      "content":"You are a helpful assistant."}
]

print("welcome to chatgpt")
while True:
    user=input("You: ")

    if user.lower()=="exit":
        print("Exiting the chat. Goodbye!")
        break
    
    messages.append({"role":"user",
                     "content":user})


    response=client.responses.create(
        model="gpt-4o-mini",
        input=messages
    )

    assistant=response.output_text
    print("\nBot: ",assistant,"\n")
    messages.append({"role":"assistant",
                     "content":assistant})




#exlore github, gitlab, bitbucket, grrit,ngrok,heroku,postman- study about all that online
