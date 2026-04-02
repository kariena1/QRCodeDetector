from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from .utils import DecodeResult, coerce_url


@dataclass(frozen=True)
class QrDecodeError(Exception):
    message: str

    def __str__(self) -> str:  # pragma: no cover
        return self.message


def decode_qr_from_bgr(bgr: np.ndarray) -> DecodeResult:
    """
    bgr: OpenCV image (H, W, 3) in BGR format.
    """
    if bgr.size == 0:
        raise QrDecodeError("빈 이미지입니다.")

    detector = cv2.QRCodeDetector()

    def _try(img: np.ndarray) -> str:
        t, _, _ = detector.detectAndDecode(img)
        return (t or "").strip()

    text = _try(bgr)
    if not text:
        # Small/low-resolution QR often fails at native size.
        for scale in (2, 3, 4):
            up = cv2.resize(bgr, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            text = _try(up)
            if text:
                break

    if not text:
        raise QrDecodeError("QR 코드를 찾지 못했습니다.")

    url = coerce_url(text)
    if url:
        return DecodeResult(text=text, is_url=True, url=url)
    return DecodeResult(text=text, is_url=False, url=None)

