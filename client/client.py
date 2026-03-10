import requests
import subprocess
import json

GATEWAY_URL = "http://localhost:8080/invoke"

def chat_with_ollama(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def ask_gateway(prompt):
    response = requests.post(
        "http://localhost:8080/invoke",
        json={
            "user": "security_engineer",
            "agent": "security-agent",
            "prompt": prompt
        },
        timeout=30
    )

    # 🔒 Handle non-200 responses explicitly
    if response.status_code != 200:
        try:
            return {
                "error": response.json()
            }
        except ValueError:
            return {
                "error": response.text or f"HTTP {response.status_code}"
            }

    # ✅ Safe JSON parse
    try:
        return response.json()
    except ValueError:
        return {
            "error": "Invalid JSON from gateway",
            "raw": response.text
        }


if __name__ == "__main__":
    while True:
        user_input = input("🧑 You: ")
        if user_input.lower() in ("exit", "quit"):
            break

        print("🤖 Thinking...\n")

        result = ask_gateway(user_input)
        print("🛡️ Secure AI:\n", json.dumps(result, indent=2))
