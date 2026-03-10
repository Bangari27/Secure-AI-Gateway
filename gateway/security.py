from fastapi import HTTPException

BLOCKLIST = [
    "ignore previous",
    "system prompt",
    "api key",
    "password",
    "secret"
]

def validate_prompt(prompt: str):
    lowered = prompt.lower()
    for bad in BLOCKLIST:
        if bad in lowered:
            raise HTTPException(
                status_code=400,
                detail=f"Blocked prompt content: {bad}"
            )
