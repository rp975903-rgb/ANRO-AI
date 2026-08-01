import ollama


print("Testing Ollama...")

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "Say hello in one sentence."
        }
    ]
)


print("\nResponse Type:")
print(type(response))


print("\nFull Response:")
print(response)


print("\nMessage:")
print(response.message)


print("\nContent:")
print(response.message.content)