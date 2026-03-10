A secure AI gateway for multi-agent systems that enforces policy-driven authorization, tool brokering, and prompt security before allowing LLM agents to execute actions.
This project demonstrates how to build a Zero-Trust AI architecture using:
Kubernetes
FastAPI
Open Policy Agent (OPA)
LLM Agents
Secure Tool Execution
CVE Intelligence via NVD


The gateway acts as a control plane between users, AI agents, and sensitive tools.
🚀 Features
🔐 Secure AI Gateway
Central control point for all AI requests


Prevents agents from accessing tools directly


🧠 AI Agent Integration
Supports local models via Ollama


Supports cloud models (OpenAI / Anthropic)


🛡️ Policy Enforcement (OPA)
User → Agent authorization


Agent → Tool authorization


Prompt filtering


🔍 Vulnerability Intelligence
CVE lookup via NVD API


Expandable to internal vulnerability databases


☸️ Kubernetes Native
Deployed as microservices


Namespace isolation


Service discovery


🔄 Tool Brokering
Agents cannot execute tools directly.
All tools must go through the gateway.
                User / CLI
                     │
                     ▼
              MCP AI Gateway
            (FastAPI Control Plane)
                     │
     ┌───────────────┼───────────────┐
     ▼                               ▼
   OPA Policy Engine           Security Agent
  (Authorization)                (LLM)
                                     │
                                     ▼
                              Tool Execution
                                     │
                                     ▼
                              Vulnerability DB
                                   (NVD)
🔐 Security Model
Zero-Trust AI design:
Layer
Control
Prompt
Prompt injection detection
Policy
OPA authorization
Agent
Intent validation
Tool
Gateway brokering


