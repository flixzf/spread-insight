# Phase 4: 웹 페이지 생성 및 배포 (Week 3-4)

> HTML 페이지 생성 및 GitHub Pages 배포

---

## ✅ Step 4.1: HTML 템플릿 디자인
**목표:** 보기 좋은 반응형 HTML 템플릿 작성
**소요 시간:** 2시간

### 📝 체크리스트
- [ ] `templates/base.html` 작성
- [ ] CSS 스타일링
- [ ] 반응형 디자인
- [ ] 브라우저 테스트

### 🛠️ 실행 순서

**1. HTML 템플릿 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\templates\base.html`
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{ summary }}">
    <title>{{ title }} | Spread Insight</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Malgun Gothic', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.8;
            color: #2C3E50;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }

        h1 {
            font-size: 2.2em;
            margin-bottom: 15px;
            font-weight: 700;
            line-height: 1.3;
        }

        .meta {
            font-size: 0.95em;
            opacity: 0.95;
            margin-top: 10px;
        }

        .meta span {
            margin: 0 10px;
        }

        .content-wrapper {
            padding: 30px;
        }

        .summary {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            padding: 25px;
            border-left: 5px solid #667eea;
            margin: 30px 0;
            border-radius: 8px;
            font-size: 1.15em;
            line-height: 1.8;
        }

        .summary strong {
            color: #667eea;
            font-size: 1.1em;
        }

        .chart {
            margin: 40px 0;
            text-align: center;
        }

        .chart img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .section {
            margin: 40px 0;
        }

        .section h2 {
            font-size: 1.6em;
            color: #2C3E50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }

        .section h2::before {
            content: '';
            display: inline-block;
            width: 6px;
            height: 25px;
            background: #667eea;
            margin-right: 10px;
            vertical-align: middle;
        }

        .content {
            font-size: 1.1em;
            line-height: 2;
            color: #34495e;
        }

        .timeline {
            background: #f8f9fa;
            padding: 25px;
            margin: 30px 0;
            border-left: 5px solid #28a745;
            border-radius: 8px;
        }

        .timeline h2 {
            color: #155724;
            border-bottom-color: #28a745;
        }

        .timeline h2::before {
            background: #28a745;
        }

        .terminology {
            background: #fff3cd;
            padding: 25px;
            margin: 30px 0;
            border-radius: 8px;
            border-left: 5px solid #ffc107;
        }

        .terminology h2 {
            color: #856404;
            border-bottom-color: #ffc107;
        }

        .terminology h2::before {
            background: #ffc107;
        }

        .term-item {
            margin-bottom: 15px;
            padding: 10px;
            background: white;
            border-radius: 5px;
        }

        .term-word {
            font-weight: 700;
            color: #856404;
            font-size: 1.1em;
        }

        .coupang-link {
            display: block;
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            color: white;
            text-align: center;
            padding: 20px;
            text-decoration: none;
            border-radius: 8px;
            font-size: 1.2em;
            font-weight: 700;
            margin: 40px 0;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        }

        .coupang-link:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
        }

        .coupang-link::before {
            content: '🛒 ';
            font-size: 1.3em;
        }

        footer {
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
            line-height: 1.6;
        }

        footer p {
            margin: 5px 0;
        }

        /* 반응형 디자인 */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }

            .container {
                border-radius: 10px;
            }

            header {
                padding: 25px 20px;
            }

            h1 {
                font-size: 1.6em;
            }

            .content-wrapper {
                padding: 20px;
            }

            .summary {
                font-size: 1.05em;
                padding: 20px;
            }

            .section h2 {
                font-size: 1.3em;
            }

            .content {
                font-size: 1.05em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 헤더 -->
        <header>
            <h1>{{ title }}</h1>
            <div class="meta">
                <span>📰 {{ source }}</span>
                <span>•</span>
                <span>📅 {{ date }}</span>
            </div>
        </header>

        <div class="content-wrapper">
            <!-- 요약 -->
            {% if summary %}
            <div class="summary">
                <strong>📌 핵심 요약</strong><br><br>
                {{ summary }}
            </div>
            {% endif %}

            <!-- 차트 -->
            {% if chart_path %}
            <div class="chart">
                <img src="{{ chart_path }}" alt="관련 차트">
            </div>
            {% endif %}

            <!-- 쉬운 설명 -->
            {% if easy_explanation %}
            <div class="section">
                <h2>쉽게 풀어보기</h2>
                <div class="content">
                    {{ easy_explanation|replace('\n', '<br>') }}
                </div>
            </div>
            {% endif %}

            <!-- 타임라인 -->
            {% if timeline %}
            <div class="timeline">
                <h2>📅 이슈 타임라인</h2>
                <div class="content">
                    {{ timeline|replace('\n', '<br>') }}
                </div>
            </div>
            {% endif %}

            <!-- 용어 해설 -->
            {% if terminology %}
            <div class="terminology">
                <h2>💡 용어 해설</h2>
                {% for term, explanation in terminology.items() %}
                <div class="term-item">
                    <span class="term-word">{{ term }}</span><br>
                    {{ explanation }}
                </div>
                {% endfor %}
            </div>
            {% endif %}

            <!-- 쿠팡 링크 -->
            {% if coupang_link %}
            <a href="{{ coupang_link }}" target="_blank" rel="noopener noreferrer" class="coupang-link">
                관련 추천 상품 보러가기
            </a>
            {% endif %}
        </div>

        <!-- 푸터 -->
        <footer>
            <p><strong>Spread Insight</strong> - 경제 뉴스를 쉽게 이해하기</p>
            <p>이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>
            <p>&copy; 2025 Spread Insight. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>
```

### ✅ 성공 기준
- [ ] 템플릿 파일 생성
- [ ] 모바일에서도 잘 보임 (반응형)
- [ ] 한글 폰트 정상 표시
- [ ] CSS 스타일 적용

---

## ✅ Step 4.2: HTML 생성기 구현
**목표:** 뉴스 데이터를 HTML 파일로 변환
**소요 시간:** 1.5시간

### 📝 체크리스트
- [ ] Jinja2 설치
- [ ] `publishers/html_generator.py` 작성
- [ ] 테스트 스크립트 작성
- [ ] HTML 파일 생성 및 브라우저 확인

### 🛠️ 실행 순서

**1. requirements.txt 업데이트**
```
# ... 기존 라이브러리들 ...
yfinance==0.2.36
pandas==2.2.0

# HTML 템플릿 엔진 추가
jinja2==3.1.3
```

설치:
```bash
pip install jinja2==3.1.3
```

**2. HTML 생성기 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\publishers\html_generator.py`
```python
from jinja2 import Template
from models.news_article import NewsArticle
from typing import Optional
import os
import re


class HTMLGenerator:
    """HTML 페이지 생성"""

    def __init__(
        self,
        template_path: str = './templates/base.html',
        output_dir: str = './data/html'
    ):
        self.template_path = template_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 템플릿 로드
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = Template(f.read())

    def _make_safe_filename(self, title: str) -> str:
        """파일명으로 사용 가능한 안전한 문자열 생성"""
        # 특수문자 제거
        safe_name = re.sub(r'[^\w\s-]', '', title)
        # 공백을 언더스코어로
        safe_name = re.sub(r'[-\s]+', '_', safe_name)
        # 최대 50자
        safe_name = safe_name[:50]
        return safe_name

    def generate(
        self,
        article: NewsArticle,
        chart_path: Optional[str] = None,
        timeline: Optional[str] = None,
        coupang_link: Optional[str] = None
    ) -> str:
        """HTML 파일 생성"""
        # 파일명 생성
        safe_title = self._make_safe_filename(article.title)
        timestamp = article.published_at.strftime('%Y%m%d')
        filename = f"{timestamp}_{safe_title}.html"
        filepath = os.path.join(self.output_dir, filename)

        # 차트 경로 처리 (상대 경로로)
        if chart_path:
            # data/charts/xxx.png → ../charts/xxx.png
            chart_path = os.path.relpath(chart_path, self.output_dir).replace('\\', '/')

        # HTML 렌더링
        html_content = self.template.render(
            title=article.title,
            source=article.source,
            date=article.published_at.strftime('%Y년 %m월 %d일'),
            summary=article.summary,
            easy_explanation=article.easy_explanation,
            timeline=timeline,
            terminology=article.terminology,
            chart_path=chart_path,
            coupang_link=coupang_link
        )

        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"  ✅ HTML 생성: {filename}")
        return filepath

    def generate_multiple(
        self,
        articles_data: list[dict]
    ) -> list[str]:
        """여러 기사 일괄 생성

        articles_data: [
            {
                'article': NewsArticle,
                'chart_path': str or None,
                'timeline': str or None,
                'coupang_link': str or None
            },
            ...
        ]
        """
        html_files = []

        for i, data in enumerate(articles_data, 1):
            print(f"[{i}/{len(articles_data)}] {data['article'].title[:40]}")

            filepath = self.generate(
                article=data['article'],
                chart_path=data.get('chart_path'),
                timeline=data.get('timeline'),
                coupang_link=data.get('coupang_link')
            )

            html_files.append(filepath)

        return html_files
```

**3. 테스트 스크립트 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_html.py`
```python
from utils.file_manager import FileManager
from publishers.html_generator import HTMLGenerator
import webbrowser
import os


if __name__ == '__main__':
    print("=" * 60)
    print("HTML 생성 테스트")
    print("=" * 60)

    # 초기화
    file_manager = FileManager()
    html_gen = HTMLGenerator()

    # 저장된 기사 로드
    saved_files = file_manager.list_saved_files()
    if not saved_files:
        print("❌ 저장된 기사가 없습니다.")
        exit(1)

    # top_news.json 또는 최신 파일
    target_file = 'top_news.json' if 'top_news.json' in saved_files else saved_files[0]
    articles = file_manager.load_articles(target_file)

    print(f"\n로드 파일: {target_file}")
    print(f"총 {len(articles)}개 기사\n")

    # 첫 번째 기사로 테스트
    article = articles[0]

    print("=" * 60)
    print("테스트 기사:")
    print(f"  제목: {article.title}")
    print(f"  출처: {article.source}")
    print(f"  날짜: {article.published_at}")
    print("=" * 60)

    # 더미 데이터로 HTML 생성
    html_path = html_gen.generate(
        article=article,
        chart_path='./data/charts/test_exchange_rate.png',  # 더미
        timeline="과거에는 환율이 낮았으나, 최근 미국 금리 인상으로 급등하고 있습니다.",
        coupang_link='https://www.coupang.com/np/search?q=환전'
    )

    print(f"\n✅ HTML 파일 생성 완료")
    print(f"경로: {html_path}")

    # 브라우저로 열기
    print(f"\n브라우저로 열기...")
    abs_path = os.path.abspath(html_path)
    webbrowser.open(f'file://{abs_path}')

    print(f"\n✅ 테스트 완료!")
```

**4. 실행**
```bash
python test_html.py
```

### ✅ 성공 기준
- [ ] HTML 파일 생성
- [ ] 브라우저에서 자동으로 열림
- [ ] 한글 정상 표시
- [ ] CSS 스타일 적용
- [ ] 반응형 동작 (브라우저 창 크기 조절 시)

### ⚠️ 예상 오류 및 해결

**오류 1:** `jinja2.exceptions.TemplateNotFound`
- **원인:** 템플릿 파일 경로 오류
- **해결:** `templates/base.html` 파일 존재 확인

**오류 2:** 한글이 깨짐
- **원인:** 인코딩 문제
- **해결:** 이미 코드에 `encoding='utf-8'` 포함

**오류 3:** 차트 이미지 안 보임
- **원인:** 상대 경로 오류
- **해결:** 코드의 `os.path.relpath()` 로직 확인

---

## ✅ Step 4.3: GitHub Pages 배포
**목표:** 생성된 HTML을 인터넷에 공개
**소요 시간:** 1.5시간

### 📝 체크리스트
- [ ] GitHub 저장소 생성
- [ ] Git 설정
- [ ] `publishers/github_deployer.py` 작성
- [ ] 배포 테스트

### 🛠️ 실행 순서

**1. GitHub 저장소 생성**
1. GitHub.com 접속 → 로그인
2. 우측 상단 `+` → `New repository`
3. Repository name: `spread-insight-pages`
4. Public 선택
5. `Create repository` 클릭

**2. GitHub Deployer 작성**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\publishers\github_deployer.py`
```python
import os
import subprocess
import shutil
from typing import List


class GitHubDeployer:
    """GitHub Pages 배포"""

    def __init__(self, repo_dir: str = './github_pages'):
        self.repo_dir = repo_dir

    def setup_repo(self, repo_url: str):
        """저장소 초기 설정 (최초 1회)"""
        if not os.path.exists(self.repo_dir):
            print(f"저장소 클론 중: {repo_url}")
            result = subprocess.run(
                ['git', 'clone', repo_url, self.repo_dir],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise Exception(f"클론 실패: {result.stderr}")

            print("✅ 저장소 클론 완료")
        else:
            print(f"저장소가 이미 존재합니다: {self.repo_dir}")
            # Pull 최신 버전
            result = subprocess.run(
                ['git', '-C', self.repo_dir, 'pull'],
                capture_output=True,
                text=True
            )
            print("✅ 저장소 업데이트 완료")

    def deploy(
        self,
        html_files: List[str],
        chart_files: List[str],
        commit_message: str = "Update news articles"
    ):
        """HTML 및 차트 파일 배포"""
        if not os.path.exists(self.repo_dir):
            raise Exception("저장소가 설정되지 않았습니다. setup_repo()를 먼저 실행하세요.")

        print("\n파일 복사 중...")

        # HTML 파일 복사
        for html_file in html_files:
            if os.path.exists(html_file):
                dest = os.path.join(self.repo_dir, os.path.basename(html_file))
                shutil.copy2(html_file, dest)
                print(f"  ✅ {os.path.basename(html_file)}")

        # 차트 디렉토리 생성
        charts_dir = os.path.join(self.repo_dir, 'charts')
        os.makedirs(charts_dir, exist_ok=True)

        # 차트 파일 복사
        for chart_file in chart_files:
            if os.path.exists(chart_file):
                dest = os.path.join(charts_dir, os.path.basename(chart_file))
                shutil.copy2(chart_file, dest)
                print(f"  ✅ charts/{os.path.basename(chart_file)}")

        # Git 커밋 및 푸시
        print(f"\nGit 커밋 중...")

        commands = [
            ['git', '-C', self.repo_dir, 'add', '.'],
            ['git', '-C', self.repo_dir, 'commit', '-m', commit_message],
            ['git', '-C', self.repo_dir, 'push']
        ]

        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                # commit 시 변경사항 없으면 에러지만 괜찮음
                if 'nothing to commit' in result.stdout:
                    print("  ⚠️  변경사항 없음")
                    return
                else:
                    raise Exception(f"Git 명령 실패: {result.stderr}")

        print("✅ GitHub Pages 배포 완료")

    def get_url(self, username: str, filename: str) -> str:
        """배포된 페이지 URL 반환"""
        return f"https://{username}.github.io/spread-insight-pages/{filename}"
```

**3. 배포 테스트 스크립트**
파일 경로: `g:\내 드라이브\08.Programming\spread_insight\test_deploy.py`
```python
from publishers.github_deployer import GitHubDeployer
import glob


if __name__ == '__main__':
    print("=" * 60)
    print("GitHub Pages 배포 테스트")
    print("=" * 60)

    deployer = GitHubDeployer()

    # === 1. 저장소 설정 (최초 1회) ===
    print("\n1단계: 저장소 설정")
    print("-" * 60)

    # 여기에 실제 GitHub 저장소 URL 입력
    REPO_URL = input("GitHub 저장소 URL 입력 (예: https://github.com/username/spread-insight-pages.git): ").strip()

    if not REPO_URL:
        print("❌ URL을 입력하지 않았습니다.")
        exit(1)

    try:
        deployer.setup_repo(REPO_URL)
    except Exception as e:
        print(f"❌ 저장소 설정 실패: {e}")
        exit(1)

    # === 2. 파일 수집 ===
    print("\n2단계: 파일 수집")
    print("-" * 60)

    html_files = glob.glob('./data/html/*.html')
    chart_files = glob.glob('./data/charts/*.png')

    print(f"  HTML 파일: {len(html_files)}개")
    print(f"  차트 파일: {len(chart_files)}개")

    if not html_files:
        print("❌ HTML 파일이 없습니다. 먼저 test_html.py를 실행하세요.")
        exit(1)

    # === 3. 배포 ===
    print("\n3단계: 배포")
    print("-" * 60)

    try:
        deployer.deploy(
            html_files=html_files,
            chart_files=chart_files,
            commit_message="Update: News articles"
        )
    except Exception as e:
        print(f"❌ 배포 실패: {e}")
        exit(1)

    # === 4. URL 출력 ===
    print("\n" + "=" * 60)
    print("✅ 배포 완료!")
    print("=" * 60)

    username = input("\nGitHub 사용자명 입력: ").strip()
    if username and html_files:
        first_file = html_files[0].split('\\')[-1].split('/')[-1]
        url = deployer.get_url(username, first_file)
        print(f"\n배포된 페이지: {url}")
        print(f"\n⚠️  GitHub Pages 활성화까지 2~3분 소요될 수 있습니다.")
```

**4. GitHub Pages 활성화**
1. GitHub 저장소 페이지 접속
2. Settings → Pages
3. Source: `Deploy from a branch`
4. Branch: `main` (또는 `master`)
5. Folder: `/ (root)`
6. Save

**5. 실행**
```bash
python test_deploy.py
```

### ✅ 성공 기준
- [ ] GitHub 저장소에 파일 푸시 완료
- [ ] GitHub Pages 활성화
- [ ] 배포된 URL 접속 가능 (2~3분 후)
- [ ] HTML 페이지 정상 표시
- [ ] 차트 이미지 정상 표시

### ⚠️ 예상 오류 및 해결

**오류 1:** `git: command not found`
- **원인:** Git 미설치
- **해결:** Git 설치 (https://git-scm.com/downloads)

**오류 2:** `Authentication failed`
- **원인:** Git 인증 안 됨
- **해결:**
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your@email.com"
  ```
  Personal Access Token 생성 및 사용

**오류 3:** GitHub Pages에서 404 오류
- **원인:** Pages 활성화 안 됨
- **해결:** Settings → Pages에서 Source 설정 확인

**오류 4:** 차트 이미지 안 보임
- **원인:** 상대 경로 오류
- **해결:** HTML의 차트 경로가 `../charts/xxx.png` 형식인지 확인

---

## 🎉 Phase 4 완료!

다음 단계: [Phase 5: 텔레그램 연동](PHASE5_TELEGRAM.md)
