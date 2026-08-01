from app.ai.llm.local_llm import LocalLLM


def main():

    print("=" * 60)
    print("🧠 NEXUS AI LOCAL LLM TEST")
    print("=" * 60)

    # ========================================================
    # INITIALIZE LLM
    # ========================================================

    llm = LocalLLM()

    print("\n🤖 Model:")
    print(llm.model_name)

    # ========================================================
    # TEST PROMPT
    # ========================================================

    prompt = """
    What is Python?

    Answer the question using the provided
    document context.
    """

    print("\n📝 Sending Prompt...")
    print(prompt)

    # ========================================================
    # GENERATE RESPONSE
    # ========================================================

    response = llm.generate(
        prompt
    )

    # ========================================================
    # DISPLAY RESPONSE
    # ========================================================

    print("\n🤖 LLM RESPONSE")
    print("-" * 60)

    print(response)

    print("\n" + "=" * 60)
    print("✅ LOCAL LLM TEST SUCCESSFUL")
    print("=" * 60)


if __name__ == "__main__":
    main()