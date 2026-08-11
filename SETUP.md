# 시작 준비 — Kiro Crew 설치와 대시보드 실행

이 폴더를 Kiro IDE로 연 직후, 실습을 시작할 수 있는 상태(대시보드 접속)까지 준비하는 문서입니다. Kiro IDE 설치와 로그인은 별도 안내를 따릅니다.

## 0. 사전 요구 점검과 설치 — 에이전트가 수행할 수 있는 절차

이 절은 에이전트가 읽고 그대로 수행할 수 있도록 쓰여 있습니다. Kiro IDE 채팅에 "이 폴더의 SETUP.md에서 0번 절차를 수행해 줘"라고 맡기면 됩니다.

**에이전트가 지켜야 할 경계:**

- 점검과 설치, 버전 확인까지만 수행한다. **로그인(`kiro-cli login`)과 초기 설정(`kirocrew setup`)은 실행하지 않는다** — 브라우저 인증과 대화형 질문은 사람이 직접 한다.
- 이미 설치된 도구는 재설치하지 않고 버전만 보고한다.
- 설치 직후 같은 셸에서 명령이 인식되지 않으면 아래 "PATH 갱신"을 수행한 뒤 다시 확인한다.
- 모든 항목이 끝나면 아래 "완료 보고 형식"으로 보고한다.

### 점검 대상 (순서대로)

**Git**

- 확인: `git --version`
- 없으면 — macOS: `brew install git` (brew가 없으면 아래 Homebrew 먼저) · Windows: `winget install --id Git.Git -e`

**Homebrew (macOS만)**

- 확인: `brew --version`
- 없으면: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- 설치가 관리자 암호를 요구해 진행할 수 없으면 중단하고, 사람에게 직접 설치를 안내한다.

**Python 3.12**

- 확인: `python3 --version` (macOS) · `py -3.12 --version` (Windows) — 3.12 이어야 한다
- 없으면 — macOS: `brew install python@3.12` · Windows: `winget install --id Python.Python.3.12 -e`
- Windows는 Microsoft Store alias가 아니라 실제 CPython이어야 한다.

**uv**

- 확인: `uvx --version`
- 없으면 — macOS: `brew install uv` · Windows: `winget install --id astral-sh.uv -e`

**kiro-cli**

- 확인: `kiro-cli --version`
- 없으면 — macOS: `curl -fsSL https://cli.kiro.dev/install | bash` · Windows: `irm 'https://cli.kiro.dev/install.ps1' | iex` (공식 다운로드 페이지 kiro.dev/downloads 의 CLI 카드와 동일한 명령입니다)
- 설치까지만. 로그인 상태(`kiro-cli whoami`)는 확인해서 보고만 하고, 로그인되어 있지 않으면 "사람이 `kiro-cli login`을 직접 실행해야 함"이라고 보고한다.

### PATH 갱신 — 설치 직후 같은 셸에서 바로 확인하기

설치 직후에는 현재 셸의 PATH에 새 명령이 아직 없을 수 있다. 새 터미널을 열지 않고 이어서 확인하려면:

macOS:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Windows PowerShell:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable('Path','User') + ';' + [Environment]::GetEnvironmentVariable('Path','Machine')
```

### 완료 보고 형식

```text
git: 2.x.x
brew: 4.x.x (macOS)
python3: 3.12.x
uvx: 0.x.x
kiro-cli: x.x.x / 로그인: <계정> 또는 "로그인 필요 — 사람이 kiro-cli login 실행"
```

## 1. 에이전트에게 설치를 맡기기

Kiro IDE 채팅에 아래를 붙여넣습니다.

```text
이 폴더의 SETUP.md 를 읽고 "0. 사전 요구 점검과 설치"와
"2. Kiro Crew 설치"를 순서대로 진행해 줘.
kiro-cli login 과 kirocrew setup 은 실행하지 마 — 그건 내가 직접 할 거야.
끝나면 0번의 완료 보고 형식과 kirocrew --version 결과를 보여 줘.
```

에이전트가 명령 실행 전에 승인을 요청하면 내용을 확인하고 승인합니다. 에이전트 진행이 매끄럽지 않으면 아래 절차를 직접 실행해도 됩니다.

## 2. Kiro Crew 설치

> **주의**: 공식 다운로드 페이지(kiro.dev/downloads)의 `Download Crew` 버튼은 **데스크톱 앱**입니다. 이 과정은 데스크톱 앱이 아니라 **CLI 설치**(아래 명령)와 브라우저 대시보드를 사용합니다 — 그 버튼은 누르지 않습니다.

### macOS

```bash
curl -fsSL https://download.crew.kiro.dev/cli.sh | sh
export PATH="$HOME/.local/bin:$PATH"
command -v kirocrew
kirocrew --version
```

설치 직후 같은 셸에는 새 경로가 없을 수 있으므로 두 번째 줄처럼 PATH를 갱신한 뒤 확인합니다 — 새 터미널을 열지 않아도 바로 검증됩니다. `command -v`가 `$HOME/.local/bin/kirocrew`를 출력하고 버전이 나오면 완료입니다. (사람이 터미널에서 직접 진행한다면 새 터미널을 여는 것으로도 충분합니다.)

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
