# QR Viewer (MVP)
화면에서 드래그로 영역을 선택해 QR을 디코딩하고, URL이면 기본 브라우저로 엽니다.

## 실행
가상환경을 권장합니다.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## 사용 방법
- 앱 창에서 `Capture` 클릭
- 전체 화면 오버레이에서 드래그로 QR 영역 선택
- URL이면 브라우저가 열리고, 결과는 클립보드에도 복사됩니다.

## macOS 권한
처음 실행 시 동작이 막히면 **시스템 설정 → 개인정보 보호 및 보안 → 화면 기록(Screen Recording)** 권한을 허용해주세요.

## Windows EXE 빌드(맥에서도 가능)
macOS에서는 Windows용 `.exe`를 직접 빌드할 수 없어서, GitHub Actions로 Windows에서 자동 빌드합니다.

- `.github/workflows/windows-exe.yml` 을 포함한 상태로 GitHub에 push
- GitHub → Actions → **Build Windows EXE** 실행(또는 push로 자동 실행)
- 실행이 끝나면 Artifacts에서 `QRViewer-windows-exe`의 `QRViewer.exe` 다운로드

## GitHub Release 배포(단일 exe)
- 릴리즈 태그를 생성해 push하면(`v1.0.0` 같은 형식) Windows 빌드 후 Release에 `QRViewer.exe`가 자동 첨부됩니다.
- 예시:

```bash
git tag v1.0.0
git push origin v1.0.0
```

- GitHub → Releases에서 해당 버전의 `QRViewer.exe`를 바로 배포하면 됩니다.

## 맥북으로 알라딘 전자책보다가 빡쳐서만듬.. 주소도 같이 넣어주면 안되나요.?
## 전자책에서 큐알링크 클릭하면 강의보러 가는기능 있으면 좋겠는데......
