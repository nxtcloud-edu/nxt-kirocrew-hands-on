# GitHub 처음 시작 · 자료 받기와 제출

![수업 레포와 내 포크, 로컬의 이동 관계](images/github-upstream-origin-local.png)


## 준비 순서 · 첫 Push 후 Crew 연결

1. Kiro IDE 설치·로그인 → Node.js·npm 확인 → Kiro CLI 인증 → Crew 설치·진단.
2. Git·GitHub CLI 설치 확인 → `gh auth login`으로 HTTPS·브라우저 인증 → `gh auth status`.
3. nxtcloud-edu 수업 레포를 내 계정에 Public Fork → 내 포크를 Clone → Kiro IDE에서 로컬 레포 열기.
4. `upstream`은 nxtcloud-edu 원본, `origin`은 내 포크인지 확인. 커밋 작성자 이름·이메일 설정.
5. `class/kookmin-2026-2/ai-platform-development/week02/submissions/start.md`를 IDE에서 만들고 저장.

```markdown
# 나의 첫 작업 기록
AI로 줄이고 싶은 일: (내 관심사)
이번 수업에서 확인할 것: (내 질문)
```

레포 루트에서 IDE 터미널 실행:
```sh
cd class/kookmin-2026-2/ai-platform-development/week02
git status
git add submissions/start.md
git commit -m "docs: 첫 작업 기록"
git push origin main
```

6. 내 GitHub 포크를 새로고침해 `start.md` 내용과 커밋 메시지를 확인. 첫 Push 성공을 확인한 뒤 다음 단계 진행.
7. Kiro Crew에서 **방금 Clone한 동일한 로컬 레포의 최상위 폴더**를 프로젝트로 열기. GitHub URL이나 submissions 폴더를 선택하는 것이 아님.
8. 첫 크루 생성 → 프로젝트 연결 확인 → 수업 자료 읽기와 첫 업무 지시.

`start.md`는 학생이 직접 작성하는 첫 기록입니다. 강사 원본에는 완성 파일을 배포하지 않습니다. 이후 AI 실습 결과와 컨텍스트 파일도 같은 submissions 아래에 누적합니다.


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

## 저장소 이름 · upstream / origin / local
- upstream: nxtcloud-edu의 수업 원본을 가리키도록 등록하는 remote 이름.
- origin: 자기 GitHub 포크를 Clone할 때 자동 등록되는 remote 이름.
- local: 내 컴퓨터의 저장소. remote 이름이 아닙니다.

Clone 후 저장소 안에서 `git remote -v`를 확인하고 upstream이 없을 때만 한 번 실행합니다. 아래는 모든 셸에서 복사할 수 있는 한 줄 명령입니다.
```sh
git remote add upstream https://github.com/nxtcloud-edu/nxt-kirocrew-hands-on.git
git remote -v
```
upstream이 이미 있으면 URL을 확인하며, 임의로 덮어쓰지 않습니다. origin은 자기 계정, upstream은 nxtcloud-edu 주소인지 확인합니다.
갱신은 **GitHub Sync fork: upstream 원본 → origin 포크**, 이후 **git pull --ff-only origin main: origin → local**입니다. 결과는 local에서 Commit한 뒤 origin에 Push합니다. upstream에 Push하지 않습니다. remote 이름은 관례이며 자동 권한·자동 동기화를 뜻하지 않습니다.


## 1. 계정과 Fork
GitHub에 로그인하고 [nxtcloud-edu 원본 레포](https://github.com/nxtcloud-edu/nxt-kirocrew-hands-on)를 엽니다. Fork → Owner에 내 계정 → Create fork. 이미 포크가 있다면 그것을 사용합니다. 주소의 소유자가 내 ID인지 확인합니다.

## 2. Kiro IDE에서 내 포크 Clone과 폴더 열기

1. GitHub의 **자기 포크**에서 **Code → HTTPS** 주소를 복사합니다. 저장소 이름만이 아니라 `https://github.com/내계정/nxt-kirocrew-hands-on.git` 전체 주소입니다.
2. Kiro IDE 시작 화면의 **Clone repository**를 누릅니다. 기존 창에서는 명령 팔레트(Windows `Ctrl+Shift+P`, Mac `Cmd+Shift+P`) → **Git: Clone**.
3. 자기 포크 URL을 붙여넣고 Clone합니다. `YOUR-GITHUB-ID` 같은 예시 문구는 실제 계정으로 바꿉니다. **Clone from GitHub**로 목록에서 찾을 수도 있으나 IDE GitHub 로그인 상태에 따라 인증이 필요할 수 있어 수업은 URL 방식으로 진행합니다.
4. 저장할 부모 폴더를 선택하고, Clone 완료 후 **Open**으로 엽니다. 이미 Clone했다면 다시 받지 않고 **File → Open Folder**(Mac은 **Open**으로 폴더 선택도 가능)로 기존 로컬 레포를 엽니다.
5. IDE 탐색기에 **SETUP.md와 class가 함께** 보이는지 확인합니다. `class/kookmin-2026-2/ai-platform-development/week02/README.md`를 열고, Markdown 미리보기(Windows `Ctrl+Shift+V`, Mac `Cmd+Shift+V`)를 확인합니다.
6. `data/`와 `submissions/` 위치까지 직접 찾은 뒤, IDE 새 터미널에서 `git remote -v`로 origin이 자기 포크인지 확인합니다. 설치·로그인만으로 준비 완료가 아닙니다.

![Kiro Clone 시작](images/ide-live/ide-clone-start.png)
![내 포크 주소 입력 예시](images/ide-live/ide-clone-url.png)
![IDE에서 week02 열기](images/ide-live/ide-week02-open.png)

주소 입력 캡처의 YOUR-GITHUB-ID는 예시입니다. 폴더 열기 캡처는 강사 로컬 레포이며 학생은 자기 포크를 사용합니다.

터미널로 이미 Clone한 경우에도 같은 결과입니다. 중복으로 Clone하지 않습니다.
```sh
git clone <내 포크의 HTTPS 주소>
cd nxt-kirocrew-hands-on
git remote -v
```
복사한 레포를 IDE에서 열고 다음 단계로 이동합니다.

## 3. 작성자 설정
복제한 레포 안에서 본인 정보로 바꿔 실행합니다. 로그인과는 별개인 커밋 작성자 정보입니다.
```bash
git config user.name "내 이름"
git config user.email "내 GitHub 이메일"
```
이메일은 GitHub Settings의 noreply 주소도 사용할 수 있습니다. 인증 요청은 IDE·Git 인증 도우미의 브라우저 안내를 따릅니다. 토큰·비밀번호를 파일에 넣지 않습니다. 인증이 막히면 강사와 확인합니다.

## 4. 어디에 저장하나요?
저장소 기준 `class/kookmin-2026-2/ai-platform-development/week02/submissions/`입니다.
- course-first.md / course-check.md: 최초·초기 검증 보고
- workspace/: 작업 계획과 개인 메모
- context/: 판단 기준과 작업 상태
- career-first.md / career-check.md: 선택 확장 결과
- execution-record.md: 실행 기록 양식을 복사해 작성
제공 data와 공유 양식은 보존합니다. 개인 포크이므로 별도 학생 이름 폴더는 필요 없습니다.

## 5. Commit·Push
파일 저장 → 로컬 이력 기록(Commit) → GitHub 업로드(Push) 순서입니다. 저장소 최상위 폴더에서 실행합니다.
```bash
git status
git add class/kookmin-2026-2/ai-platform-development/week02/submissions/
git diff --cached --stat
git commit -m "2주차 실습 결과 제출"
git push origin main
```
커밋 전에 제출 파일만 선택되었는지 확인합니다. 브랜치가 main이 아니거나 인증·push 오류가 나면 강사에게 보여주세요. 강제 push는 하지 않습니다.

## 6. 제출 확인
내 GitHub 레포를 새로고침하고 main의 submissions 파일 내용·최신 커밋을 확인합니다. 포크 URL과 제출 커밋 링크를 수업 안내 채널에 남깁니다. nxtcloud-edu 원본 레포에 Pull Request는 보내지 않습니다.

## 7. 다음 주 자료 받기
자기 작업 Commit·Push → 내 GitHub의 Sync fork → Update branch → IDE 터미널:
```bash
git pull --ff-only origin main
```
충돌이나 분기 오류가 나오면 멈추고 강사와 확인합니다. Discard commits·강제 덮어쓰기를 선택하지 않습니다.

## 수업 중 버전 기록
첫 작업과 새 공지 반영 후 각각 Commit·Push합니다. [작업 이어가기](05_작업_이어가기.md)의 순서를 따릅니다. career 결과는 선택 확장이며 필수 파일 목록은 [제출 폴더](submissions/README.md)를 기준으로 합니다.

## 공개 제출과 작성자 정보의 구분
nxtcloud-edu의 공개 원본을 Fork하면 포크도 Public입니다. 수업 기간에는 이 공개 포크에 결과를 누적해 강사가 조회할 수 있게 합니다. 별도 비공개 복제본을 제출처로 쓰지 않습니다.

- Public Clone·조회: Git 작성자 이름·이메일 설정 불필요.
- 로컬 Commit: 작성자 이름·이메일 필요. 기존 설정은 `git config user.name`, `git config user.email`로 확인.
- user.name: 커밋에 남는 표시 이름이며 GitHub 사용자명과 일치할 필요 없음.
- user.email: 계정과 커밋을 연결하려면 GitHub 등록 이메일 또는 GitHub noreply 이메일 사용.
- Push: 자신의 포크에 대한 GitHub 인증과 쓰기 권한 필요. Public이라고 누구나 수정 가능한 것은 아님.
- 학생 식별: 수업 채널에서 **학생 본인 + 포크 URL + 최종 커밋 링크**를 매칭. 실명·학번을 공개 레포 파일에 적을 필요 없음.

공식 근거: https://docs.github.com/en/pull-requests/reference/forks 및 https://docs.github.com/en/get-started/git-basics/setting-your-username-in-git
