package mcp.authz

default allow = false

################################
# Allow invoking the agent
################################
allow {
  input.user == "security_engineer"
  input.agent == "security-agent"
}

################################
# Allow tool usage
################################
allow {
  input.user == "security_engineer"
  input.tool == "vuln_lookup"
}
