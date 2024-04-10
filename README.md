<p align="center">
  <a href="https://www.google.com">
    <img alt="Semtle Logo" src="https://github.com/Lab-Semtle/Semtle-Web-Server/blob/master/asset/semtle_logo2.jpg?raw=true" width="60" style="border-radius: 50%;" />
  </a>
</p>
<h1 align="center">
    Semtle-Web-Server
</h1>

🔥 한국해양대학교 인공지능공학부 컴퓨터공학전공 학회 아치셈틀 웹페이지 구축 프로젝트 🔥

## 🧐 프로젝트 아키텍처

해당 프로젝트의 디렉터리 구조는 다음과 같습니다.

    .
    ├── asset
    ├── data
    ├── docs
    ├── src
    ⎪   ├─ api
    ⎪   ├─ context
    ⎪   ├─ extentions
    ⎪   └─ variables
    ├── .gitignore
    ├── pyproject.toml
    └── README.md

1.  **`/data`**: 애플리케이션에서 사용할 데이터 파일들이 저장되는 디렉토리입니다. 구성 파일, JSON 파일, 초기 데이터 세트 등을 포함될 수 있습니다.

2.  **`/docs`**: 협업 및 유지보수를 위한 추가 설명(마크다운)들을 기록하고 보관하는 디렉토리입니다.

3.  **`/src`**: 소스 코드의 메인 디렉토리입니다. 이곳에 애플리케이션의 주요 로직이 포함됩니다.

- **`/src/api`**: 각종 API 엔드포인트를 정의합니다. 컨트롤러(Controller), 서비스(Service), 데이터 접근 객체(DAO), 데이터 전송 객체(DTO) 로 구성되어 있습니다.

  - **`../_ctl.py`**: 컨트롤러 파일로, HTTP 요청을 처리하고 응답합니다.
  - **`../_dao.py`**: 데이터 접근 객체로, 데이터베이스와의 직접적인 상호작용을 담당합니다.
  - **`../_dto.py`**: 데이터 전송 객체로, 클라이언트와 서버 간의 데이터 교환 포맷을 정의합니다.
  - **`../_svc.py`**: 서비스 로직을 구현, 비즈니스 로직을 처리합니다.

4.  **`src/context`**: 애플리케이션 컨텍스트 및 설정을 관리합니다.

5.  **`src/extensions`**: 애플리케이션의 확장성을 고려한 구조로, 미들웨어, CORS, 이벤트 핸들러 등을 쉽게 추가할 수 있는 확장 포인트를 포함합니다.

6.  **`src/variables`**: 애플리케이션의 변수, 모델 정의, 세션 관리 등을 포함합니다.

7.  **`.gitignore`**: Git 버전 관리에서 제외할 파일 목록을 정의합니다.

8.  **`.pyproject.toml`**: 프로젝트의 의존성 관리와 패키지 설정을 포함합니다. Poetry를 사용하여 의존성을 관리하고, 프로젝트 설정을 정의합니다.
