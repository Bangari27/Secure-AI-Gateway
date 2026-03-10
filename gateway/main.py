from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

from security import validate_prompt
from tools.vuln_lookup import lookup as vuln_lookup

OPA_URL = "http://opa.policy.svc.cluster.local:8181/v1/data/mcp/authz/allow"


AGENT_MAP = {
    "security-agent": "http://security-agent.ai-agents.svc.cluster.local:8000/run"
}

app = FastAPI(title="MCP AI Gateway")


class InvokeRequest(BaseModel):
    user: str
    agent: str
    prompt: str


@app.post("/invoke")
def invoke(req: InvokeRequest):
    # 1. Prompt security
    validate_prompt(req.prompt)

    # 2. Phase 1: authorize user → agent
    decision = requests.post(
        OPA_URL,
        json={
            "input": {
                "user": req.user,
                "agent": req.agent,
                "prompt": req.prompt
            }
        },
        timeout=5
    ).json()

    if not decision.get("result"):
        raise HTTPException(status_code=403, detail="Denied by policy")

    # 3. Call agent
    resp = requests.post(
        AGENT_MAP[req.agent],
        json={"prompt": req.prompt},
        timeout=60
    )

    agent_raw = resp.json().get("raw", "")
    agent_decision = None  # 🔒 defensive initialization

    # 4. Try to parse structured intent
    try:
        agent_decision = json.loads(agent_raw)
    except json.JSONDecodeError:
        # Plain text response → safe to return
        return {
            "user": req.user,
            "agent": req.agent,
            "response": agent_raw
        }

    # 5. Tool execution path (WITH OPA AUTHZ)
    if agent_decision.get("action") == "vuln_lookup":
        tool_decision = requests.post(
            OPA_URL,
            json={
                "input": {
                    "user": req.user,
                    "agent": req.agent,
                    "tool": "vuln_lookup",
                    "prompt": req.prompt
                }
            },
            timeout=5
        ).json()

        if not tool_decision.get("result"):
            raise HTTPException(status_code=403, detail="Tool use denied by policy")

        cve = agent_decision.get("cve")
        vuln = vuln_lookup(cve)

        return {
            "user": req.user,
            "agent": req.agent,
            "cve": cve,
            "vulnerability": vuln
        }

    # 6. Structured response without tool
    return {
        "user": req.user,
        "agent": req.agent,
        "response": agent_decision.get("text", agent_raw)
    }
