# 시작 준비 — Kiro Crew 설치와 대시보드 실행

이 폴더를 Kiro IDE로 연 직후, 실습을 시작할 수 있는 상태(대시보드 접속)까지 준비하는 문서입니다. Kiro IDE 설치와 로그인은 별도 안내를 따릅니다.

## 1. 에이전트에게 설치를 맡기기

Kiro IDE 채팅에 아래를 붙여넣습니다.

```text
이 폴더의 SETUP.md 를 읽고 "2. Kiro Crew 설치" 절차를 진행해 줘.
kirocrew setup 은 실행하지 마 — 그건 내가 직접 할 거야.
설치가 끝나면 새 셸 기준으로 kirocrew --version 결과를 보여 줘.
```

에이전트가 명령 실행 전에 승인을 요청하면 내용을 확인하고 승인합니다. 에이전트 진행이 매끄럽지 않으면 아래 절차를 직접 실행해도 됩니다.

## 1.5. kiro-cli가 없다면 먼저 설치

`kiro-cli whoami`가 `command not found`로 실패하면 kiro-cli부터 설치합니다.

### macOS

```bash
curl -fsSL https://cli.kiro.dev/install | bash
```

### Windows PowerShell

```powershell
irm 'https://cli.kiro.dev/install.ps1' | iex
```

설치 후 새 터미널에서 `kiro-cli login`으로 로그인하고 `kiro-cli whoami`로 계정을 확인합니다. 로그인은 브라우저 인증이 필요하므로 사람이 직접 합니다.

## 2. Kiro Crew 설치

### macOS

```bash
curl -fsSL https://download.crew.kiro.dev/cli.sh | sh
exec zsh
command -v kirocrew
kirocrew --version
```

`command -v`가 비어 있으면 다음을 실행한 뒤 새 셸에서 다시 확인합니다.

```bash
export PATH="$HOME/.local/bin:$PATH"
exec zsh
kirocrew --version
```

### Windows PowerShell

```powershell
cd $HOME
git clone https://github.com/kirodotdev/KiroCrew.git kirocrew-app
cd kirocrew-app
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\Activate.ps1
kirocrew --version
```

새 터미널을 열 때마다 가상환경을 다시 활성화합니다: `cd "$HOME\kirocrew-app"; .\.venv\Scripts\Activate.ps1`

## 3. 초기 설정 — 여기부터는 직접 합니다

설치가 끝나면 이 실습 폴더에서 실행합니다. 대화형 질문에 답해야 하므로 사람이 직접 진행합니다.

```bash
kirocrew setup
```

| 질문 | 권장 응답 |
|---|---|
| `Workspace path [...]` | `Enter` (기본 별도 경로 사용) |
| `Configure Slack tokens? [Y/n]` | `n` |
| `Slash command name [kirocrew]` | `Enter` |
| `Timezone [...]` | `Enter` (한국은 필요 시 `Asia/Seoul`) |
| `Install KiroCrew desktop app ... [Y/n]` | `n` |
| `Launch KiroCrew on AWS now? [y/N]` | `Enter` |

```bash
kirocrew doctor
```

`doctor`에서 다음은 이 과정의 문제로 보지 않습니다 — Slack 미설정, `project dir: not set`, `whisper: not found`, Gateway 실행 전의 `Gateway not running`.

## 4. Gateway 실행과 접속

터미널 하나를 Gateway 전용으로 씁니다. 실습 중에는 끄지 않습니다.

```bash
kirocrew gateway
```

브라우저에서 `http://localhost:5476`을 엽니다.

### 처음 접속 시 — Import Setup 안내

첫 접속에서 `Import Setup` 화면(Bring your crew with you)이 뜰 수 있습니다. 이 컴퓨터에서 다른 AI 도구(Codex, Claude Code 등)를 쓰고 있었다면 그 설정을 가져올지 묻는 것입니다.

**이 과정에서는 `Skip all`을 누릅니다.** 개인 설정을 가져오면 실습 화면이 안내와 달라질 수 있습니다. 화면이 뜨지 않으면 그대로 진행합니다.

## 5. 준비 완료 확인

```text
□ 대시보드가 열린다 (http://localhost:5476)
□ 이 폴더에서 git status 를 치면 브랜치 main 이 보인다
```

여기까지 됐으면 교재의 Lab 0(세션 준비)으로 이동합니다.
