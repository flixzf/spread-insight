#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Adobe Firefly API 테스트 - 공식 문서의 올바른 scope 사용

공식 문서:
scope=openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis
"""

import requests
import time
from utils.config import Config

print("=" * 70)
print("Adobe Firefly API Test - Correct Scope")
print("=" * 70)

client_id = Config.ADOBE_CLIENT_ID
client_secret = Config.ADOBE_CLIENT_SECRET
org_id = Config.ADOBE_ORG_ID

print(f"\nClient ID: {client_id}")
print(f"Org ID: {org_id}")

# Step 1: 올바른 scope으로 토큰 발급
print("\n[Step 1] Access Token 발급 (올바른 scope)...")
token_url = "https://ims-na1.adobelogin.com/ims/token/v3"

# 공식 문서의 scope
correct_scope = "openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis"

token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': correct_scope
}

print(f"Scope: {correct_scope}")

token_response = requests.post(token_url, data=token_data)
print(f"Token 응답 코드: {token_response.status_code}")

if token_response.status_code != 200:
    print(f"[FAIL] Token 발급 실패")
    print(f"응답: {token_response.text}")
    exit(1)

token_result = token_response.json()
access_token = token_result['access_token']
print("[OK] Access Token 발급 성공!")

# 토큰 디코딩해서 scope 확인
import base64
import json
parts = access_token.split('.')
if len(parts) >= 2:
    payload = parts[1]
    payload += '=' * (4 - len(payload) % 4)
    decoded = base64.b64decode(payload)
    payload_json = json.loads(decoded)
    print(f"\n[Token Scope] {payload_json.get('scope', 'N/A')}")

# Step 2: Firefly API 호출
print("\n[Step 2] Firefly API 호출...")

# v3 Async 엔드포인트
firefly_url = "https://firefly-api.adobe.io/v3/images/generate"

# 공식 문서의 헤더
headers = {
    'Authorization': f'Bearer {access_token}',
    'x-api-key': client_id,
    'Content-Type': 'application/json'
}

payload = {
    "prompt": "Photorealistic image of business professionals in modern office, vibrant colors, professional stock photo style, NO TEXT",
    "size": {"width": 1024, "height": 1024}
}

print(f"\nURL: {firefly_url}")
print(f"Headers: Authorization + x-api-key + Content-Type")

firefly_response = requests.post(firefly_url, headers=headers, json=payload, timeout=60)
print(f"\nAPI 응답 코드: {firefly_response.status_code}")

if firefly_response.status_code == 200:
    print("[OK] 성공!")
    result = firefly_response.json()
    print(f"\n응답:")
    print(result)

elif firefly_response.status_code == 202:
    print("[OK] 비동기 작업 시작!")
    result = firefly_response.json()
    print(f"\n응답:")
    print(result)

else:
    print(f"[FAIL] 실패")
    print(f"응답: {firefly_response.text}")

    # 진단
    if firefly_response.status_code == 403:
        print("\n[진단]")
        print("  여전히 403이면 Entitlement 미개통이 확실합니다.")
        print("  Adobe 담당자에게 Firefly API 권한 요청이 필요합니다.")

print("\n" + "=" * 70)
