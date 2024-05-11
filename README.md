<p align="center">
  <a href="https://www.google.com">
    <img alt="Semtle Logo" src="https://github.com/Lab-Semtle/Semtle-Web-Server/blob/master/asset/semtle_logo2.jpg?raw=true" width="60" style="border-radius: 50%;" />
  </a>
</p>
<h1 align="center">
    Semtle-Web-Server
</h1>

🔥 한국해양대학교 인공지능공학부 컴퓨터공학전공 학회 아치셈틀 웹페이지 구축 프로젝트 🔥

## 개발 환경

### 사전 준비

- `python` 버전 관리 목적 `pyenv` 설치
- `python` 패키지 관리 목적 `poetry` 설치

### 개발 빌드

1. 가상 환경 생성

   ```shell
   python -m venv .venv
   ```

2. 의존성 설치

   ```shell
   poetry install
   ```

3. 개발
   - IDE `vscode`로 개발

### PostgreSQL 설정

### 프로젝트 아키텍처 구조

```
Semtle-Web-Server/
│
├── asset                  # 프로젝트에 사용되는 정적 자원들(이미지, CSS 파일 등) 모음
├── src/                   # 소스 코드 폴더, 여기에 프로젝트의 모든 파이썬 코드가 들어감
│   ├── api/               # API 관련 코드를 모아둔 폴더
│   │   ├── __init__.py    # API 모듈을 초기화하는 스크립트, api 폴더를 파이썬 패키지로 만듬
│   │   ├── v1/            # API의 첫 번째 버전을 정의한 폴더
│   │   │   ├── __init__.py
│   │   │   ├── post/      # 'post' 관련 기능들을 처리하는 코드가 들어있는 폴더
│   │   │   │   ├── __init__.py
│   │   │   │   ├── post_control.py   # 엔드포인트 로직 작성, HTTP 요청 처리
│   │   │   │   ├── post_dao.py       # 데이터베이스 접근하는 로직 구현
│   │   │   │   ├── post_dto.py       # 데이터 전송 객체(데이터의 구조를 정의)
│   │   │   │   └── post_service.py   # 비즈니스 로직 처리
│   │   ...
│   │
│   ├── core/              # 애플리케이션 핵심 기능 모음
│   │   ├── __init__.py
│   │   ├── config.py      # 애플리케이션의 설정을 관리
│   │   ├── security.py    # 보안 관련 기능 구현
│   │   ├── error.py       # 에러 핸들링 관련 코드 구현
│   │   ├── event.py       # 애플리케이션에서 발생하는 이벤트 핸들링
│   │   ├── status.py      # HTTP 상태 코드 추가 정의(확장)
│   │   └── cors.py        # 요청 필터링 미들웨어 (웹 요청 사이의 자원 공유를 위한 설정)
│   │
│   ├── dependencies/      # API 엔드포인트의 의존성(종속성) 관리를 위한 파일 모음 (API 요청 전 검사)
│   │   ├── __init__.py.
│   │   └── authentication.py # 엔드포인트에서 필요한 모든 사용자 인증 관련 종속성 관리 코드
│   │
│   ├── var/               # 애플리케이션 모델, 데이터베이스 세션 관리 코드 모음
│   │   ├── __init__.py
│   │   ├── dto.py         # 유지보수성을 위한 BaseDTO 설정
│   │   ├── models.py      # 애플리케이션에서 사용되는 데이터베이스 모델 정의
│   │   └── session.py     # 데이터베이스 연결 및 세션 관리를 위한 코드
│   │
│   │
│   ├── utils/             # 유틸리티 함수 모음
│   │   ├── __init__.py
│   │
│   ├── __init__.py        # 애플리케이션을 초기화하는 스크립트, 동일한 python 패키지로 만듬
│   └── main.py            # FastAPI 애플리케이션의 진입점
│
├── tests/             # 테스트 코드, 애플리케이션 기능 검증
│   │   ...
│
├── .gitignore          # Git 버전 관리에서 제외할 파일 목록
├── Dockerfile          # Docker를 사용하여 애플리케이션을 컨테이너화하는 설정
├── docker-compose.yml  # 여러 컨테이너를 함께 관리하고 실행하기 위한 설정
├── poetry.lock         # 프로젝트 의존성 관리, 실제로 설치된 패키지 버전 잠금(고정) 설정
├── pyproject.toml      # 설치한 패키치 목록, 호환 가능한 버전 정보 명시
└── README.md
```
