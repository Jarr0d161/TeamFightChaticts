import os
from typing import Tuple, List
from dataclasses import dataclass, field
from PIL import ImageGrab, Image

import cv2
import numpy as np
import pytesseract


@dataclass
class TFTTesseractScreenCapture:
    tesseract_rootdir: str
    item_icon_files: List[str] = field(default_factory=
        lambda:['./images/white.png', './images/blue.png'])

    def __post_init__(self):
        if os.path.exists(self.tesseract_rootdir):
            tesseract_exe = os.path.join(self.tesseract_rootdir, 'tesseract.exe')
            pytesseract.pytesseract.tesseract_cmd = tesseract_exe
        else:
            raise ValueError('Der Pfad für Tesseract ist nicht korrekt!')

    def capture_level(self) -> Tuple[int, int]:
        screenshot = self._capture_screenshot(box=(400, 880, 450, 910), crop=(5, 10, 40, 25))
        screenshot = self._scale_screenshot(screenshot, 4)
        ocr_text = self._scan_numeric_text_ocr(np.array(screenshot))

        if '/' not in ocr_text:
            return None
        parts = ocr_text.split('/')

        act_xp, total_xp = parts[0].strip(), parts[1].strip()
        if not act_xp.isdecimal() or total_xp.isdecimal():
            return None
        return int(act_xp), int(total_xp)

    def capture_gold(self) -> int:
        screenshot = TFTTesseractScreenCapture._capture_screenshot(box=(870, 880, 905, 910))
        screenshot = TFTTesseractScreenCapture._scale_screenshot(screenshot, 4)
        ocr_text = self._scan_numeric_text_ocr(np.array(screenshot))
        return int(ocr_text) if ocr_text.isdecimal() else None

    def capture_item_locations(self, crop: Tuple[int, int, int, int]) -> List[Tuple[int, int]]:
        screenshot = self._capture_screenshot(crop=crop)
        grayscale: np.ndarray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        dim = (int(grayscale.shape[0]), int(grayscale.shape[1]))
        resized = cv2.resize(grayscale, dim, interpolation = cv2.INTER_AREA)
        thresh = TFTTesseractScreenCapture._adaptive_threshold(resized)

        return [(match[0], match[1]) for template_file in self.item_icon_files
                for match in TFTTesseractScreenCapture._find_image_matches(thresh, template_file)]

    @staticmethod
    def _capture_screenshot(box: Tuple[int, int, int, int]=None,
                            crop: Tuple[int, int, int, int]=None) -> Image.Image:
        return ImageGrab.grab(bbox=box).crop(crop) if crop else ImageGrab.grab(bbox=box)

    @staticmethod
    def _scale_screenshot(screenshot: Image.Image, factor: float):
        (width, height) = (screenshot.width * factor, screenshot.height * factor)
        return screenshot.resize((width, height))

    def _scan_numeric_text_ocr(self, image: np.ndarray) -> str:
        tess_settings = "--psm 7 -c tessedit_char_whitelist=0123456789/"
        tess_datadir = os.path.join(self.tesseract_rootdir, "tessdata")
        tess_params = f'{tess_settings} --tessdata-dir "{tess_datadir}"'
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edge_filtered_image = cv2.threshold(
            grayscale, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        return pytesseract.image_to_string(
            edge_filtered_image, config=tess_params).strip()

    @staticmethod
    def _adaptive_threshold(image: np.ndarray):
        return cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 61, 11)

    @staticmethod
    def _find_image_matches(image, template_filepath: str, threshold=0.5) -> list:
        template: np.ndarray = cv2.imread(template_filepath, 0)
        template = TFTTesseractScreenCapture._adaptive_threshold(template)
        res = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        return list(zip(*loc[::-1]))
