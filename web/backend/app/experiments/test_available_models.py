from app.ai.client import client


models = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash",
]

for model in models:
    print(f"\nTesting {model}...")

    try:
        response = client.interactions.create(
            model=model,
            input="Respond with exactly: OK",
        )

        if response.output_text:
            print(f"SUCCESS: {response.output_text}")
            print(f"Working model: {model}")
            break

        print("FAILED: Empty response")

    except Exception as error:
        print(f"FAILED: {error}")

else:
    print("None of the tested models worked.")