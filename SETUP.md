# 시작 준비 · 공식 앱 다운로드

## 1. Kiro IDE
[공식 다운로드](https://kiro.dev/downloads/)에서 내 OS에 맞는 IDE를 설치하고 수업 계정으로 로그인합니다.

## Git·GitHub CLI 설치와 인증
Kiro IDE 로그인 후 새 터미널에서 확인합니다. Git과 GitHub CLI(gh)는 별도 도구입니다.
```sh
git --version
gh --version
```
없으면 [Git 공식 다운로드](https://git-scm.com/downloads)와 [GitHub CLI 공식 설치 안내](https://cli.github.com/)에서 운영체제별 절차로 설치합니다. 설치 후 IDE 새 터미널에서 재확인합니다.

먼저 `gh auth status`로 기존 인증을 확인합니다. 올바른 자기 계정으로 준비되어 있으면 반복 로그인하지 않습니다. 처음이면:
```sh
gh auth login
```
**GitHub.com → HTTPS → Git 인증 질문에 Y → Login with a web browser** 순서로 진행합니다. 표시된 일회용 코드를 본인이 입력하고 승인합니다.
```sh
gh auth status
```
기존 gh 인증은 있지만 Git과 연결이 안 된 경우 `gh auth setup-git`을 실행합니다. 여러 계정을 쓰고 있다면 사용할 계정을 먼저 강사와 확인합니다.

- Settings에서 Personal Access Token을 직접 발급하는 과정은 기본 실습에 없습니다.
- gh 인증과 `git config user.name / user.email` 작성자 설정은 별개입니다.
- Public 포크는 강사에게 별도 쓰기 권한을 받을 필요가 없습니다. 자기 포크에 Push합니다.
- 이 인증 확인은 실제 Push 성공을 대신하지 않습니다. 제출 때 Push와 온라인 파일 확인까지 진행합니다.
- 인증 코드·토큰은 캡처나 제출 파일에 넣지 않습니다.

공식 근거: [GitHub 인증 안내](https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git), [gh auth login](https://cli.github.com/manual/gh_auth_login).

## 2. IDE 터미널 · Node.js·npm 점검
IDE 로그인 후 Terminal 메뉴에서 새 터미널을 엽니다.
```bash
node --version
npm --version
```
없으면 https://nodejs.org/ 에서 LTS를 설치하고 새 터미널에서 재확인합니다. 프런트엔드 개발·빌드를 위한 준비이며 Crew 앱 자체의 일괄 필수 조건을 뜻하지 않습니다.

## 3. Kiro CLI 설치·인증
https://kiro.dev/downloads/ 의 CLI 항목에서 내 OS의 공식 절차를 따릅니다.
```bash
kiro-cli --version
kiro-cli login
kiro-cli whoami
```
로그인은 직접 진행하며 이미 수업 계정으로 인증되어 있으면 생략합니다. IDE 로그인과 CLI 인증을 따로 확인합니다.

## 4. Kiro Crew
같은 페이지에서 **Download Kiro Crew**를 선택합니다. 공식 GitHub 다운로드 안내로 이동할 수 있습니다.
- macOS·Windows: 내 OS의 **Stable** 데스크톱 설치 파일을 내려받아 설치·실행합니다.
- Linux: 공식 README의 배포판별 설치 안내를 강사와 확인합니다. 공식 문서는 Linux에 CLI 설치를 우선 안내하므로 앱 설치만으로 일괄 진행하지 않습니다.
- 설치 파일이 없거나 오류가 나면 OS·오류 문구를 강사에게 보여줍니다. 임의의 외부 설치 파일이나 우회 명령을 사용하지 않습니다.

## 5. 첫 실행·계정 확인
앱의 CLI 설치·로그인 안내가 나타나면 안내에 따라 진행합니다. 브라우저 인증은 직접 완료합니다. 이미 로그인된 경우 수업 계정을 확인합니다.
일반적인 앱 실행은 내장 Gateway를 시작하므로 터미널에서 `kirocrew gateway`나 `kirocrew setup`을 별도로 실행하는 것을 기본 절차로 삼지 않습니다. Slack·AWS 연동은 이번 실습에 필요하지 않습니다.

## 6. IDE 터미널 · Crew 점검
```bash
kirocrew --version
kirocrew doctor
```
앱 설치 후 새 터미널에서 확인합니다. 명령이 없으면 앱 버전·연결 상태와 CLI PATH를 강사와 확인합니다. 앱 설치와 CLI 명령 노출은 별개일 수 있으므로 무조건 재설치하지 않습니다. Slack 미설정과 실제 인증·연결 실패를 구분합니다. 수업 승인 모드는 Normal입니다.

## 7. 수업 자료 연결
개인 GitHub 계정으로 수업 레포를 Fork하고 자기 포크를 clone합니다. IDE와 Crew 세션 프로젝트에 SETUP.md와 class가 있는 저장소 최상위 폴더를 연결합니다. Normal 승인 모드로 시작합니다.
Git 설치 전 ZIP으로 시작했다면 제출 전에 자기 포크를 clone하고 결과를 옮깁니다.

국민대 2주차 확인 요청:
```text
class/kookmin-2026-2/ai-platform-development/week02/data/course/notices.md를 읽고
제목과 공지 ID 목록만 알려줘. 파일은 수정하지 마.
```
앱 화면·계정·연결 경로·읽은 원문과 응답까지 확인하면 실습 준비 완료입니다.

## 문제 해결용 참고
[이전 CLI 설치 절차](SETUP_CLI_FALLBACK.md)는 강사와 원인을 확인한 뒤 필요한 부분만 사용합니다. AI에게 설치 전체를 맡기는 기본 지시는 사용하지 않습니다.

확인 기준: 2026-09-08 공식 다운로드 및 공식 README.
- https://kiro.dev/downloads/
- https://github.com/kirodotdev/KiroCrew#quick-start

## 국민대 W02 · 설치 다음 순서
설치·인증 완료 후 Public Fork와 Clone을 진행합니다. week02/submissions/start.md를 IDE에서 작성하고 첫 Commit·Push 및 GitHub 웹 확인을 마친 뒤, Crew에 동일한 로컬 레포 최상위 폴더를 연결합니다. 자세한 순서는 [W02 실습 안내](class/kookmin-2026-2/ai-platform-development/week02/03_실습_안내.md)를 따릅니다.
