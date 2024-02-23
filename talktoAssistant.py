from openai import OpenAI
import time
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
api_key = os.environ.get("API_KEY")
print(api_key)
assistant_id = os.environ.get("ASSISTANT_ID")
print(assistant_id)

df = pd.read_excel("test.xlsx")
excel_content = df.to_string(index=False)

client = OpenAI(api_key = api_key)

thread = client.beta.threads.create()
print(thread)

message = client.beta.threads.create(
    messages = [
        {
            "role": "user",
            "content": f"Here is the excel content: {excel_content}",
        }
    ]
)

run = client.beta.threads.runs.create(

  thread_id=thread.id,
  assistant_id=assistant_id,
)

print(f"Run created: {run.id}")


while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print(f"Run Status: {run.status}")
    time.sleep(1)
else:
    print("Run Completed")

message_response = client.beta.threads.messages.list(thread_id = thread.id)
messages = message_response.data

latest_message = messages[0]
print(f"Response: {latest_message.content[0].text.value}")