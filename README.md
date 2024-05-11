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
- Docker Descktop 설치 (WSL2 설치해야할 수도 있음.)

### 개발 빌드

1. 가상 환경 생성

   ```shell
   python -m venv .venv
   ```

2. 의존성 설치
   모듈 호환 에러 날 경우 개발 OS 차이 때문이니 poetry.toml 파일 참고해서 우선은 수동으로 설치해주세요.
   추후, window에도 호환되게 수정해두겠습니다.

   ```shell
   poetry install
   ```

3. PostgreSQL 이미지 다운로드

   - 윈도우 CMD를 관리자 모드로 실행하여 도커가 설치되었는지 확인
     ```
     docker -v
     ```
   - 도커에서 postgres 이미지를 다운받는다.
     ```
     docker pull postgres:latest
     ```
   - 도커 이미지를 사용하기 위해 컨터이너 생성
     ```
     docker run --name postgres -e POSTGRES_PASSWORD=1234 -e TZ=Asia/Seoul -p 5432:5432 -d postgres:latest
     ```
   - 설치했던 도커 데스크톱에서 container가 정상적으로 실행되는지 확인한다.

4. 이후 DBeaver에 접속해서 Docker에서 실행되는 PostgreSQL과 연결

   - 좌측 최상단 콘센트모양(+) 를 클릭
   - Connect to a databse 창이 뜨면 PostgreSQL 아이콘 클릭 후 `다음` 클릭
   - URL 칸에 `jdbc:postgresql://localhost:5432/postgres` 적혀있는지 확인 후
   - 각 칸에 DB정보를 기입한다.
     - Host -> localhost
     - Port -> 5432
     - Database -> postgres
     - Username -> postgres
     - Password -> postgres (혹은 기입X)
   - 이후 좌측 최하단 Test Connection 을 클릭해서 정상적으로 DB서버에 접속되었는지 확인한다.

5. VScode에서 Uvicorn 서버 실행
   ```
   uvicorn src.main:app --reload
   ```
   서버 실행 이후 DBeaver 에서 postgres 를 우클릭하여 검증/재연결 을 눌러서 정상 연결되고 있는지 확인한 후,
   public -> table -> user 을 클릭해서 user테이블이 정상적으로 생성되었는지 확인한다.

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
