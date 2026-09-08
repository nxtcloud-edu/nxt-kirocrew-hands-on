# 01 · GitHub 준비와 첫 Push

## 1. 설치·인증

[SETUP.md](../../../../SETUP.md): Kiro IDE 로그인 → Node·npm 확인 → CLI 인증 → Crew 설치.
IDE 터미널에서 Git·GitHub CLI 확인. 없으면 [Git](https://git-scm.com/downloads)·[gh](https://cli.github.com/) 설치.

```sh
git --version
gh --version
gh auth status
```

인증이 없으면 `gh auth login`: **GitHub.com → HTTPS → Git 인증 Y → 브라우저 로그인**.
기존 gh 인증만 있고 Git 연결이 안 되면 `gh auth setup-git`.

## 2. Fork → Clone → Open

1. [nxtcloud-edu 원본](https://github.com/nxtcloud-edu/nxt-kirocrew-hands-on) → **Fork** → 내 계정. Public 유지.
2. 내 포크의 **Code → HTTPS** 주소 복사.
3. Kiro IDE **Clone repository** → 내 포크 URL → 저장 위치 → **Open**.
4. 이미 Clone했다면 **Open Folder**로 열기. `SETUP.md`와 `class/`가 함께 보이는 최상위 폴더 선택.
5. `week02/README.md`, `data/`, `submissions/` 위치 확인.

Markdown 미리보기: Windows `Ctrl+Shift+V` / Mac `Cmd+Shift+V`.

## 3. 원격 저장소·작성자 확인

| 이름 | 위치 | 용도 |
|---|---|---|
| upstream | nxtcloud-edu 원본 | 자료 받기 |
| origin | 자기 GitHub 포크 | 결과 Push |
| local | 내 컴퓨터 | 작업·Commit |

```sh
git remote -v
git config user.name
git config user.email
```

upstream이 없을 때만:
```sh
git remote add upstream https://github.com/nxtcloud-edu/nxt-kirocrew-hands-on.git
```

작성자 설정이 없으면 본인 정보로 설정. 인증과는 별개이며 이메일은 GitHub noreply 주소도 가능.
```sh
git config user.name "내 이름"
git config user.email "내 GitHub 이메일"
```

## 4. 첫 파일 수정 → Commit → Push

IDE에서 `week02/submissions/start.md`를 열어 **내가 해야 하는 일·시간이 오래 걸리거나 귀찮은 부분·AI가 해주면 좋을 결과** 작성.
저장소 최상위 폴더의 터미널에서:

```sh
cd class/kookmin-2026-2/ai-platform-development/week02
git status
git add submissions/start.md
git diff --cached
git commit -m "docs: 첫 작업 기록"
git push origin main
```

**확인:** 자기 GitHub에 수정 내용과 커밋이 보이면 성공.
이제 Crew에서 **같은 로컬 저장소 최상위 폴더**를 프로젝트로 연결.

- 결과는 `submissions/`에만 저장. 토큰·인증 코드·학번은 공개 파일에 넣지 않기.
- 오류·충돌 시 강사와 확인. 강제 Push·Discard commits 금지.
- 새 자료 받기와 이후 제출은 [05 작업 이어가기](05_작업_이어가기.md).
