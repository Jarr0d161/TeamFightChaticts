import pytesseract
from PIL import ImageGrab
import cv2
import numpy as np

def capture_screenshot(box: Tuple[int, int, int, int], crop: Tuple[int, int, int, int]=None):
    return ImageGrab.grab(bbox=box).crop(crop) if crop else ImageGrab.grab(bbox=box)

def scale_screenshot(screenshot, factor):
    (width, height) = (screenshot.width * factor, screenshot.height * factor)
    return screenshot.resize((width, height))

def get_level_text() -> str:
    screenshot = capture_screenshot((400, 880, 450, 910), (5, 10, 40, 25))
    screenshot = scale_screenshot(screenshot, 4)

    grayscale = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    thresholding = cv2.threshold(grayscale, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    tess_dir = 'C:\\Program Files\\Tesseract-OCR\\tessdata'
    tessdata_dir_config = '--psm 7 -c tessedit_char_whitelist=0123456789/ --tessdata-dir "{tess_dir}"'
    text = pytesseract.image_to_string(thresholding, config=tessdata_dir_config).strip()

    # TODO: add parser logic here and change interface to return a proper data type ...

    return text

def get_gold_text() -> str:
    screenshot = ImageGrab.grab(bbox=(870, 880, 905, 910))
    scale = 4
    (width, height) = (screenshot.width * scale, screenshot.height * scale)
    screenshot = screenshot.resize((width, height))
    image = np.array(screenshot)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholding = cv2.threshold(grayscale, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    tess_dir = 'C:\\Program Files\\Tesseract-OCR\\tessdata'
    tessdata_dir_config = '--psm 7 -c tessedit_char_whitelist=0123456789/ --tessdata-dir "{tess_dir}"'
    text = pytesseract.image_to_string(thresholding, config=tessdata_dir_config).strip()

    # TODO: add parser logic here and change interface to return a proper data type ...

    return text

def get_items():
    screenshot = ImageGrab.grab().crop((500, 200, 1375, 725))
    image = np.array(screenshot)
    grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    width = int(grayscale.shape[1])
    height = int(grayscale.shape[0])
    dim = (width, height)
    resized = cv2.resize(grayscale, dim, interpolation = cv2.INTER_AREA)
    thresh = adthresholding(resized)
    cv2.imwrite('../output/res.png', thresh)

    matches_w = findMatches(thresh, '../images/white.png')
    matches_b = findMatches(thresh, '../images/blue.png')
    return matches_w + matches_w

def adthresholding(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 61, 11)

def findMatches(img, tmp, threshold=0.5) -> list:
    template = cv2.imread(tmp, 0)
    w, h = template.shape[::-1]
    template = adthresholding(template)
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where(res >= threshold)
    return list(zip(*loc[::-1]))
