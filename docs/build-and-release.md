# Build & Release

## Windows 빌드/배포 (GitHub Actions, 단일 EXE)

워크플로우: `.github/workflows/windows-exe.yml`

### 1) 단일 exe 빌드
- PyInstaller `--onefile`로 `dist/QRViewer.exe`를 생성합니다.
- GitHub Actions Artifacts에서 `QRViewer-windows-exe`를 다운로드할 수 있습니다.

### 2) GitHub Release 자동 첨부
- `v*` 태그 push 시(예: `v1.0.0`) 워크플로우가 실행됩니다.
- 빌드 완료 후 Release 자산으로 `QRViewer.exe`가 자동 업로드됩니다.

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 3) 참고사항
- onefile 특성상 초기 실행이 조금 느릴 수 있고 파일 크기가 커질 수 있습니다.
- 첫 실행 시 SmartScreen 경고가 뜰 수 있으며, 코드 서명 인증서 적용 시 완화됩니다.

## macOS 빌드/배포 (PyInstaller 기준)

### 1) 로컬 빌드 (가장 쉬움)

```bash
cd "/Users/kariena/Desktop/qr-viewer"
source .venv/bin/activate
pip install pyinstaller
pyinstaller --noconfirm --windowed --name "QRViewer" run.py
```

- 결과물: `dist/QRViewer.app`

### 2) 서명 (권장)
다른 맥에서도 경고를 줄이려면 **Developer ID Application** 인증서로 서명하는 게 좋습니다.

```bash
codesign --force --deep --options runtime --sign "Developer ID Application: <YOUR NAME> (<TEAMID>)" "dist/QRViewer.app"
codesign -vvv --deep --strict "dist/QRViewer.app"
spctl -a -vv "dist/QRViewer.app"
```

### 3) 공증(Notarization) + 스테이플 (강력 권장)

```bash
ditto -c -k --keepParent "dist/QRViewer.app" "QRViewer.zip"

xcrun notarytool submit "QRViewer.zip" \
  --apple-id "<APPLE_ID_EMAIL>" \
  --team-id "<TEAMID>" \
  --password "<APP_SPECIFIC_PASSWORD>" \
  --wait

xcrun stapler staple "dist/QRViewer.app"
spctl -a -vv "dist/QRViewer.app"
```

### 4) 배포 형태
- 가장 간단: `dist/QRViewer.app`를 zip으로 압축해 배포
- 더 깔끔: DMG 생성(선택)

### 5) 사용자 권한 안내 (필수)
화면 캡처가 필요하므로, 처음 실행 시 사용자가 다음을 허용해야 할 수 있습니다.

- 시스템 설정 → 개인정보 보호 및 보안 → 화면 기록(Screen Recording)

