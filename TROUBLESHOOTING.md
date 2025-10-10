# 문제 해결 가이드 (Troubleshooting)

> 개발 과정에서 발생한 문제와 해결 방법을 기록합니다.

---

## 📅 2025-10-10: Phase 1 개발 환경 설정 및 스크래핑 구현

### 🔴 문제 1: lxml 라이브러리 설치 실패

**발생 단계:** Step 1.1 - 라이브러리 설치 중

**오류 메시지:**
```
error: Microsoft Visual C++ 14.0 or greater is required.
Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**원인 분석:**
- Python 3.13 환경에서 `lxml==5.1.0` 설치 시 C/C++ 컴파일이 필요
- lxml은 C로 작성된 libxml2/libxslt 라이브러리를 래핑하므로 빌드 도구 필요
- Windows에서 Visual C++ 14.0 이상의 빌드 툴이 설치되어 있지 않음

**해결 방법:**
1. **선택 1 (권장):** lxml 없이 진행
   - `requirements.txt`에서 lxml 제거
   ```
   # Phase 1: 뉴스 수집
   beautifulsoup4==4.12.3
   requests==2.31.0
   # lxml==5.1.0  # Python 3.13 호환성 문제로 제외
   python-dotenv==1.0.1
   ```

   - BeautifulSoup에서 `html.parser` 사용 (Python 내장)
   ```python
   # 변경 전
   soup = BeautifulSoup(response.text, 'lxml')

   # 변경 후
   soup = BeautifulSoup(response.text, 'html.parser')
   ```

2. **선택 2:** Visual C++ Build Tools 설치 (불필요)
   - 다운로드: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - 설치 시 "Desktop development with C++" 워크로드 선택
   - 설치 후 `pip install lxml` 재시도

**적용 결과:**
- ✅ lxml 없이 진행하여 추가 설치 없이 해결
- ✅ `html.parser`는 한글 뉴스 파싱에 충분한 성능 제공
- ✅ 의존성 감소로 배포 환경 단순화

**영향 받은 파일:**
- `requirements.txt` (Line 127)
- `scrapers/naver_scraper.py` (Line 303, 373)
- `scrapers/daum_scraper.py` (향후 작성 시 동일 적용)

**참고:**
- `html.parser`: Python 내장, 속도 중간, 관대한 파싱
- `lxml`: 가장 빠름, 엄격한 파싱, C 확장 필요
- `html5lib`: 가장 느림, 가장 관대함, 순수 Python

---

### 🔴 문제 2: Windows 콘솔 이모지 인코딩 오류

**발생 단계:** Step 1.2 - test_scraper.py 실행 중

**오류 메시지:**
```
UnicodeEncodeError: 'cp949' codec can't encode character '\u274c' in position 0:
illegal multibyte sequence
```

**원인 분석:**
- Windows 콘솔(cmd, PowerShell)의 기본 인코딩이 cp949 (한글 Windows)
- 이모지 문자(`❌`, `✅`, `🔍`, `💾` 등)는 Unicode Emoji 블록에 속함
- cp949는 한글과 ASCII만 지원하며 이모지를 인코딩할 수 없음

**해결 방법:**

1. **선택 1 (권장):** 이모지를 ASCII 텍스트 마커로 대체
   ```python
   # 변경 전
   print("✅ 스크래핑 성공!")
   print("❌ 오류 발생")
   print("🔍 스크래핑 중...")
   print("💾 저장 완료")
   print("⚠️ 경고")

   # 변경 후
   print("[OK] 스크래핑 성공!")
   print("[ERROR] 오류 발생")
   print("[검색중] 스크래핑 중...")
   print("[저장완료] 저장 완료")
   print("[!] 경고")
   ```

2. **선택 2:** 콘솔 인코딩을 UTF-8로 변경 (일시적)
   ```python
   import sys
   import io
   sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
   ```

3. **선택 3:** Windows Terminal 사용 (UTF-8 지원)
   - Microsoft Store에서 "Windows Terminal" 설치
   - 설정 → 기본 프로필 → PowerShell 선택

**적용 결과:**
- ✅ 모든 print 문에서 이모지를 텍스트 마커로 교체
- ✅ Windows 콘솔에서 정상 실행
- ✅ 가독성 유지 및 크로스 플랫폼 호환성 향상

**영향 받은 파일:**
- `test_scraper.py` (모든 print 문)
- 향후 작성할 모든 테스트 스크립트에 동일 적용 예정

**참고:**
- Linux/macOS는 기본적으로 UTF-8 사용하므로 이모지 출력 가능
- VS Code 통합 터미널은 UTF-8 사용하므로 이모지 출력 가능
- 배포 환경을 고려하여 ASCII 텍스트 마커가 더 안전한 선택

---

## 📊 작업 완료 내역

### ✅ Step 1.1: 프로젝트 초기 설정
- **완료 일자:** 2025-10-10
- **상태:** 완료
- **결과:**
  - 폴더 구조 생성 완료
  - 가상환경 설정 완료
  - 의존성 설치 완료 (lxml 제외)
  - .gitignore 작성 완료
  - .env 파일 템플릿 생성 완료

### ✅ Step 1.2: 단일 기사 스크래핑 (네이버)
- **완료 일자:** 2025-10-10
- **상태:** 완료
- **결과:**
  - `models/news_article.py` 작성 완료
  - `scrapers/base_scraper.py` 작성 완료
  - `scrapers/naver_scraper.py` 작성 완료 (html.parser 사용)
  - `test_scraper.py` 작성 및 실행 성공
  - 테스트 기사: "산업차관, 철강 관세 대응 등 수출 지원체계 확인…해상물류 점검"
  - 본문 길이: 2728자
  - JSON 저장 성공: `./data/raw/test_article.json`

---

## 🔧 환경 정보

- **운영체제:** Windows
- **Python 버전:** 3.13
- **콘솔 인코딩:** cp949 (Windows 기본)
- **프로젝트 경로:** `g:\내 드라이브\08.Programming\spread_insight`
- **가상환경:** venv (Python 3.13)

---

## 📝 교훈 및 베스트 프랙티스

### 1. 의존성 최소화
- 필수적이지 않은 C 확장 라이브러리는 피하기
- Python 내장 라이브러리 우선 사용 (`html.parser` vs `lxml`)
- 크로스 플랫폼 호환성 고려

### 2. 인코딩 고려
- Windows 콘솔의 cp949 인코딩 제한 인지
- 이모지 사용 자제, ASCII 텍스트 마커 사용
- 배포 환경의 다양성을 고려한 안전한 코딩

### 3. 문서화
- 발생한 문제와 해결 방법을 즉시 문서화
- 다른 개발자나 미래의 자신을 위한 가이드 작성
- 코드 주석에 중요한 결정 사항 기록

### 4. 테스트
- 각 단계별 독립적인 테스트 스크립트 작성
- 성공 기준을 명확히 정의
- 예상 오류 시나리오를 미리 문서화

---

## 🔜 다음 단계

- [ ] Step 1.3: 여러 기사 목록 수집
- [ ] Step 1.4: 데이터 저장 (JSON)
- [ ] Step 1.5: 다음(Daum) 스크래퍼 추가

---

## 📞 추가 지원이 필요한 경우

- 새로운 오류 발견 시 이 문서에 추가
- 각 Phase 완료 후 해당 섹션 업데이트
- 주요 결정 사항은 PROJECT_PLAN.md에도 반영
