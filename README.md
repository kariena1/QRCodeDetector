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
- 실행이 끝나면 Artifacts에서 `QRViewer-windows.zip` 다운로드
- 압축 해제 후 `QRViewer.exe` 실행

