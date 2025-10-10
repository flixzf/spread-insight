# 버전 관리 시스템 - 게임 패치처럼!

## 🎮 개념

게임 업데이트처럼 **새로운 버전을 미리 만들어두고, 테스트 후 마음에 들면 적용**하는 시스템입니다.

## 📦 현재 버전

### v1 - Basic Format (Stable)
- 타이틀 → 이미지 → 텍스트 순서
- 마크다운 없음 (순수 텍스트)
- 쿠팡 파트너스 1개만
- 3초 딜레이

---

## 🛠️ 사용 방법

### 1. 현재 버전 확인
```bash
python version_manager.py info
```

### 2. 사용 가능한 버전 목록 보기
```bash
python version_manager.py list
```

### 3. 새 버전 테스트 (실제 전송 안함)
```bash
python version_manager.py test v2
```
→ 텔레그램에 전송하지 않고 미리보기만 보여줌

### 4. 버전 전환 (업데이트)
```bash
python version_manager.py switch v2
```
→ .env 파일 자동 업데이트, 다음 실행부터 적용

---

## 🚀 새 버전 만드는 방법

### Step 1: 새 포맷터 파일 생성
```bash
# publishers/telegram_formatters/v2_rich.py 만들기
cp publishers/telegram_formatters/v1_basic.py publishers/telegram_formatters/v2_rich.py
```

### Step 2: 클래스 이름 변경
```python
# v2_rich.py
class TelegramFormatterV2:
    """
    버전: v2.0
    상태: Experimental
    특징:
      - 마크다운 풍부
      - 이모지 많이 사용
      - 쿠팡 파트너스 3개
    """
    # ... 여기서 마음껏 수정
```

### Step 3: 레지스트리에 등록
```python
# publishers/telegram_formatters/__init__.py

from .v1_basic import TelegramFormatterV1
from .v2_rich import TelegramFormatterV2  # 추가

FORMATTERS = {
    'v1': TelegramFormatterV1,
    'v2': TelegramFormatterV2,  # 추가
}
```

### Step 4: 버전 정보 추가
```python
# publishers/telegram_formatters/__init__.py의 get_version_info()

def get_version_info():
    info = {
        'v1': {...},
        'v2': {  # 추가
            'name': 'Rich Format',
            'description': '마크다운 풍부, 이모지 많음, 쿠팡 3개',
            'status': 'experimental'
        },
    }
    return info
```

### Step 5: 테스트
```bash
python version_manager.py test v2
```

### Step 6: 마음에 들면 적용
```bash
python version_manager.py switch v2
python test_simple_card.py  # 실제 텔레그램 전송 테스트
```

### Step 7: 안 좋으면 롤백
```bash
python version_manager.py switch v1  # 언제든 되돌리기
```

---

## 💡 실험 아이디어

### v2 - Rich Format
- 마크다운 **볼드**, *이탤릭* 사용
- 이모지 많이 추가
- 쿠팡 파트너스 3개
- 인라인 버튼 추가

### v3 - Minimal Format
- 초미니멀 디자인
- 이모지 최소화
- 짧은 텍스트만

### v4 - Carousel Format
- 여러 이미지 슬라이드
- 각 섹션마다 이미지 첨부

### v5 - Interactive Format
- 텔레그램 인터랙티브 버튼
- "더 보기" 버튼으로 펼치기
- 링크 바로가기 버튼

---

## 📁 파일 구조

```
publishers/
  telegram_formatters/
    __init__.py          # 버전 레지스트리
    v1_basic.py          # 현재 버전
    v2_rich.py           # 실험 버전 (미구현)
    v3_minimal.py        # 실험 버전 (미구현)
  telegram_publisher.py  # 자동으로 버전 선택

version_manager.py       # 버전 관리 CLI
```

---

## ⚠️ 주의사항

1. **v1은 건드리지 마세요!**
   - v1은 안정 버전으로 유지
   - 새 실험은 항상 새 버전 번호로

2. **테스트 먼저!**
   - 실제 텔레그램 전송 전에 `test` 명령으로 확인

3. **.env 백업**
   - 버전 전환 시 .env 파일이 자동 수정됨
   - 필요하면 미리 백업

---

## 🎯 워크플로우 예시

```bash
# 1. 새 아이디어: "마크다운 더 화려하게!"
cp publishers/telegram_formatters/v1_basic.py publishers/telegram_formatters/v2_rich.py

# 2. v2_rich.py 수정
# - 클래스 이름: TelegramFormatterV2
# - 마크다운 **추가**, _강조_ 추가

# 3. 레지스트리 등록
# __init__.py에 v2 추가

# 4. 미리보기
python version_manager.py test v2

# 5. 괜찮으면 적용
python version_manager.py switch v2
python test_simple_card.py

# 6. 별로면 롤백
python version_manager.py switch v1
```

---

## 끝!

이제 **실험 → 테스트 → 적용 → 롤백**을 자유롭게 할 수 있습니다! 🎉
