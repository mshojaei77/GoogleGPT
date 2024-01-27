import g4f

prompt = input("Ask anything : ")

response2 = g4f.ChatCompletion.create(
    model= "",
    provider=g4f.Provider.GeekGpt,
    messages=[
        {"role": "user", "content": prompt}
    ],
    stream=True
)
for message in response2:
    print(message, flush=True, end='')
print()