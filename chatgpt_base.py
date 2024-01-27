from openai import OpenAI

prompt = input("Ask anything : ")

client = OpenAI(api_key='YOUR API HERE')

response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': prompt}
    ],
    temperature=0,
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, flush=True, end="")
print()

