import requests
import json
from utils.config import Config

client_id = Config.ADOBE_CLIENT_ID
client_secret = Config.ADOBE_CLIENT_SECRET

# Access Token 발급
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'openid,AdobeID,firefly_api'
}

response = requests.post("https://ims-na1.adobelogin.com/ims/token/v3", data=data)
result = response.json()

print("=== Access Token Info ===")
print(json.dumps(result, indent=2))

# Token 디코딩 (JWT)
access_token = result.get('access_token', '')
import base64

# JWT의 payload 부분만 디코딩
parts = access_token.split('.')
if len(parts) >= 2:
    payload = parts[1]
    # Base64 패딩 추가
    payload += '=' * (4 - len(payload) % 4)
    decoded = base64.b64decode(payload)
    print("\n=== Token Payload (decoded) ===")
    print(json.dumps(json.loads(decoded), indent=2))
