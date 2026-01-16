import json
import hmac
import hashlib
import datetime
import urllib.request

SIGNING_SECRET = b"hello-there-from-b12"
URL = "https://b12.io/apply/submission"

payload = {
    "action_run_link": "https://github.com/your-org/your-repo/actions/runs/123456789",
    "email": "adbansal99@gmail.com",
    "name": "Aditya Bansal",
    "repository_link": "https://github.com/aditya2499/b12_submission",
    "resume_link": "https://drive.google.com/file/d/10-wF2ChddSMLbcuIPrZN7BXafOx1AzQa/view?usp=sharing",
    "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
}

body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

digest = hmac.new(SIGNING_SECRET, body, hashlib.sha256).hexdigest()
signature = f"sha256={digest}"

request = urllib.request.Request(
    URL,
    data=body,
    headers={
        "Content-Type": "application/json",
        "X-Signature-256": signature,
    },
    method="POST",
)

with urllib.request.urlopen(request) as response:
    response_body = response.read().decode("utf-8")
    result = json.loads(response_body)

    if result.get("success"):
        print("receipt")
        print(result["receipt"])
    else:
        raise RuntimeError("Submission failed")
