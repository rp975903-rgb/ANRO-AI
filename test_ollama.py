import ollama


print("=" * 60)
print("OLLAMA DIRECT TEST")
print("=" * 60)

try:

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": "Say hello in one sentence."
            }
        ]
    )

    print("\nRAW RESPONSE:")
    print(response)

    print("\nRESPONSE TYPE:")
    print(type(response))

    print("\nMESSAGE:")
    print(response.message)

    print("\nMESSAGE TYPE:")
    print(type(response.message))

    print("\nCONTENT:")
    print(response.message.content)

except Exception as error:

    print("\nERROR:")
    print(type(error).__name__)
    print(str(error))