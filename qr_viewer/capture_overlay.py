from __future__ import annotations

from dataclasses import dataclass

from PySide6 import QtCore, QtGui, QtWidgets


@dataclass(frozen=True)
class CaptureRect:
    x: int
    y: int
    w: int
    h: int


class CaptureOverlay(QtWidgets.QWidget):
    captured = QtCore.Signal(CaptureRect)
    cancelled = QtCore.Signal()

    def __init__(self) -> None:
        super().__init__(None)
        self.setWindowTitle("CaptureOverlay")
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.Tool
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setCursor(QtCore.Qt.CursorShape.CrossCursor)

        self._dragging = False
        self._start = QtCore.QPoint()
        self._end = QtCore.QPoint()

        self._dim_color = QtGui.QColor(0, 0, 0, 120)
        self._border_color = QtGui.QColor(255, 255, 255, 220)
        self._fill_color = QtGui.QColor(80, 160, 255, 60)

        self._help = QtWidgets.QLabel("드래그로 영역 선택 • ESC 취소", self)
        self._help.setStyleSheet(
            "QLabel { color: white; background: rgba(0,0,0,160); padding: 8px 10px; border-radius: 8px; }"
        )
        self._help.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    def start_fullscreen(self) -> None:
        screen = QtGui.QGuiApplication.primaryScreen()
        if screen is None:
            raise RuntimeError("No primary screen")
        geom = screen.virtualGeometry()
        self.setGeometry(geom)
        self.show()
        self.raise_()
        self.activateWindow()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self._dragging = False
            self.hide()
            self.cancelled.emit()
            return
        super().keyPressEvent(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() != QtCore.Qt.MouseButton.LeftButton:
            return
        self._dragging = True
        self._start = event.position().toPoint()
        self._end = self._start
        self.update()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if not self._dragging:
            return
        self._end = event.position().toPoint()
        self.update()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if not self._dragging or event.button() != QtCore.Qt.MouseButton.LeftButton:
            return
        self._dragging = False
        self._end = event.position().toPoint()
        rect = QtCore.QRect(self._start, self._end).normalized()
        self.hide()
        if rect.width() < 8 or rect.height() < 8:
            self.cancelled.emit()
            return
        self.captured.emit(CaptureRect(rect.x(), rect.y(), rect.width(), rect.height()))

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self._help.move(16, 16)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        painter.fillRect(self.rect(), self._dim_color)

        if self._dragging:
            rect = QtCore.QRect(self._start, self._end).normalized()
            painter.fillRect(rect, self._fill_color)
            pen = QtGui.QPen(self._border_color)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawRect(rect)

