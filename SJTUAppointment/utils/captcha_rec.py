from io import BytesIO
from PIL import Image
import pytesseract
import requests

# 识别图形验证码
def captcha_rec(captcha):
    imgByteArr = captcha.screenshot_as_png
    imgByteArr2 = BytesIO(imgByteArr)
    captcha_img = Image.open(imgByteArr2)
    captcha_img = captcha_img.resize((100, 40))
    captcha_img = captcha_img.convert('L')
    captcha = pytesseract.image_to_string(captcha_img, lang='eng')
    captcha = captcha.strip() # Remove trailing whitespaces
    return captcha