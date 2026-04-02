from __future__ import annotations

import sys
import webbrowser

import numpy as np
from mss import mss
from PySide6 import QtCore, QtGui, QtWidgets

from .capture_overlay import CaptureOverlay, CaptureRect
from .decode import QrDecodeError, decode_qr_from_bgr


def _grab_region(rect: CaptureRect) -> np.ndarray:
    with mss() as sct:
        monitor = {"left": rect.x, "top": rect.y, "width": rect.w, "height": rect.h}
        shot = sct.grab(monitor)  # BGRA
        img = np.asarray(shot, dtype=np.uint8)
        if img.ndim != 3 or img.shape[2] < 3:
            return img
        bgr = img[:, :, :3]
        return bgr


def _copy_image_to_clipboard(bgr: np.ndarray) -> None:
    h, w = bgr.shape[:2]
    if h <= 0 or w <= 0:
        return
    rgb = bgr[:, :, ::-1].copy()
    qimg = QtGui.QImage(rgb.data, w, h, rgb.strides[0], QtGui.QImage.Format.Format_RGB888)
    QtWidgets.QApplication.clipboard().setImage(qimg)


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QR Viewer")
        self.setMinimumWidth(420)

        self._overlay = CaptureOverlay()
        self._overlay.captured.connect(self._on_captured)
        self._overlay.cancelled.connect(self._on_cancelled)

        self._btn = QtWidgets.QPushButton("Capture")
        self._btn.clicked.connect(self._start_capture)

        self._status = QtWidgets.QLabel("버튼을 누르고 드래그해서 QR 영역을 선택해요.")
        self._status.setWordWrap(True)

        self._auto_open = QtWidgets.QCheckBox("URL이면 자동으로 브라우저 열기")
        self._auto_open.setChecked(True)

        self._copy_image = QtWidgets.QCheckBox("캡처 이미지를 클립보드에 저장")
        self._copy_image.setChecked(True)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self._status)
        layout.addSpacing(8)
        layout.addWidget(self._btn)
        layout.addWidget(self._auto_open)
        layout.addWidget(self._copy_image)
        layout.addStretch(1)

    @QtCore.Slot()
    def _start_capture(self) -> None:
        self._status.setText("캡처 모드: 드래그로 영역 선택 (ESC 취소)")
        self._overlay.start_fullscreen()

    @QtCore.Slot()
    def _on_cancelled(self) -> None:
        self._status.setText("취소됨. 다시 시도해요.")

    @QtCore.Slot(object)
    def _on_captured(self, rect: CaptureRect) -> None:
        try:
            bgr = _grab_region(rect)
            if self._copy_image.isChecked():
                _copy_image_to_clipboard(bgr)

            result = decode_qr_from_bgr(bgr)
            if result.is_url and result.url:
                QtWidgets.QApplication.clipboard().setText(result.url)
                self._status.setText(f"URL 감지: {result.url}\n(클립보드에 복사됨)")
                if self._auto_open.isChecked():
                    webbrowser.open(result.url)
            else:
                QtWidgets.QApplication.clipboard().setText(result.text)
                self._status.setText(f"텍스트 감지: {result.text}\n(클립보드에 복사됨)")
        except QrDecodeError as e:
            self._status.setText(str(e))
        except Exception as e:  # noqa: BLE001
            self._status.setText(f"오류: {e}")


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    return app.exec()

