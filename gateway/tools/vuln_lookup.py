import requests
import time
import re

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

CACHE = {}
CACHE_TTL = 3600  # 1 hour

def lookup(cve_id: str):
    # Strict validation (security-critical)
    if not re.match(r"^CVE-\d{4}-\d{4,}$", cve_id):
        return {"error": "Invalid CVE format"}

    now = time.time()

    # Cache hit
    if cve_id in CACHE:
        entry = CACHE[cve_id]
        if now - entry["ts"] < CACHE_TTL:
            return entry["data"]

    # Fetch from NVD
    r = requests.get(
        NVD_API,
        params={"cveId": cve_id},
        timeout=10
    )
    r.raise_for_status()
    data = r.json()

    if not data.get("vulnerabilities"):
        return {"error": "CVE not found"}

    cve = data["vulnerabilities"][0]["cve"]
    metrics = cve.get("metrics", {})
    cvss = metrics.get("cvssMetricV31", [{}])[0].get("cvssData", {})

    result = {
        "cve": cve_id,
        "severity": cvss.get("baseSeverity"),
        "score": cvss.get("baseScore"),
        "description": cve["descriptions"][0]["value"]
    }

    CACHE[cve_id] = {"ts": now, "data": result}
    return result
