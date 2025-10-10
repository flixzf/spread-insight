#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Adobe Firefly API v3 Async 테스트 (Org ID 헤더 포함)

추천받은 방법대로 x-gw-ims-org-id 헤더 추가
"""

import requests
import time
from utils.config import Config

print("=" * 70)
print("Adobe Firefly API v3 Async Test (with Org ID)")
print("=" * 70)

# 설정 확인
client_id = Config.ADOBE_CLIENT_ID
client_secret = Config.ADOBE_CLIENT_SECRET
org_id = Config.ADOBE_ORG_ID

print(f"\nClient ID: {client_id}")
print(f"Org ID: {org_id}")
print(f"Client Secret: {'*' * 20}")

if not client_id or not client_secret or not org_id:
    print("\n[ERROR] Adobe API 키가 설정되지 않았습니다.")
    print("  .env 파일에 ADOBE_CLIENT_ID, ADOBE_CLIENT_SECRET, ADOBE_ORG_ID를 설정하세요.")
    exit(1)

# Step 1: Access Token 발급
print("\n[Step 1] Access Token 발급...")
token_url = "https://ims-na1.adobelogin.com/ims/token/v3"

token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'openid,AdobeID,firefly_enterprise'
}

token_response = requests.post(token_url, data=token_data)
print(f"Token 응답 코드: {token_response.status_code}")

if token_response.status_code != 200:
    print(f"[FAIL] Token 발급 실패")
    print(f"응답: {token_response.text}")
    exit(1)

token_result = token_response.json()
access_token = token_result['access_token']
print("[OK] Access Token 발급 성공!")

# Step 2: Firefly v3 Async API 호출
print("\n[Step 2] Firefly v3 Async API 호출...")
print("추천받은 방법대로 x-gw-ims-org-id 헤더 추가")

firefly_url = "https://firefly-api.adobe.io/v3/images/generate-async"

# 필수 헤더 (추천받은 방법)
headers = {
    'Authorization': f'Bearer {access_token}',
    'x-api-key': client_id,
    'x-gw-ims-org-id': org_id,  # ⭐ 이게 핵심!
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

payload = {
    "prompt": "Photorealistic image of business professionals in a modern corporate office discussing tariffs, steel, exports. Scene: executives analyzing economic data on large monitors, financial charts and graphs visible in background. Style: professional stock photo aesthetic, vibrant but natural colors. Important: NO TEXT or LETTERS visible anywhere in the image.",
    "size": {"width": 1024, "height": 1024}
}

print(f"\nURL: {firefly_url}")
print(f"Headers:")
print(f"  Authorization: Bearer {access_token[:30]}...")
print(f"  x-api-key: {client_id}")
print(f"  x-gw-ims-org-id: {org_id}")
print(f"\nPayload: {payload}")

firefly_response = requests.post(firefly_url, headers=headers, json=payload, timeout=60)
print(f"\nAPI 응답 코드: {firefly_response.status_code}")

if firefly_response.status_code == 202:
    print("[OK] 비동기 작업 시작 성공!")
    result = firefly_response.json()
    print(f"\n응답 JSON:")
    print(result)

    # 폴링 URL 확인
    if 'href' in result or '_links' in result:
        status_url = result.get('href') or result.get('_links', {}).get('self', {}).get('href')
        print(f"\n[Step 3] 작업 상태 폴링...")
        print(f"Status URL: {status_url}")

        # 최대 60초 폴링
        for i in range(30):
            time.sleep(2)
            status_response = requests.get(status_url, headers=headers)
            print(f"  폴링 {i+1}/30: {status_response.status_code}")

            if status_response.status_code == 200:
                status_result = status_response.json()
                status = status_result.get('status', 'unknown')
                print(f"    Status: {status}")

                if status == 'succeeded':
                    print("\n[OK] 이미지 생성 성공!")
                    print(f"\n최종 결과:")
                    print(status_result)

                    # 이미지 URL 추출
                    if 'outputs' in status_result:
                        for idx, output in enumerate(status_result['outputs']):
                            image_url = output.get('image', {}).get('url') or output.get('image', {}).get('presignedUrl')
                            if image_url:
                                print(f"\n[이미지 {idx+1}] {image_url}")
                    break
                elif status == 'failed':
                    print("\n[FAIL] 작업 실패")
                    print(status_result)
                    break
        else:
            print("\n[TIMEOUT] 60초 내 완료되지 않음")
    else:
        print("\n응답에 status URL이 없습니다.")

elif firefly_response.status_code == 200:
    print("[OK] 동기 응답 성공!")
    result = firefly_response.json()
    print(f"\n응답:")
    print(result)

else:
    print(f"[FAIL] API 호출 실패")
    print(f"응답: {firefly_response.text}")

    # 상세 진단
    print("\n[진단]")
    if firefly_response.status_code == 401:
        print("  → 토큰 만료/잘못된 토큰")
    elif firefly_response.status_code == 403:
        print("  → Org 권한 문제 / Entitlement 미개통")
        print("  → Admin Console에서 Firefly Services 권한 확인 필요")
    elif firefly_response.status_code == 404:
        print("  → 잘못된 엔드포인트 URL")

print("\n" + "=" * 70)
