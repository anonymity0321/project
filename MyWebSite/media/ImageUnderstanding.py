# coding: utf-8
import _thread as thread
import base64
import hashlib
import hmac
import json
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from urllib.parse import urlparse
from wsgiref.handlers import format_date_time
import websocket
import os
import pyautogui
import pytesseract
from PIL import Image, ImageFilter
import cv2
import numpy as np
import re

# 设置 Tesseract OCR 引擎的路径（Windows 需要设置，其他系统一般不需要）
pytesseract.pytesseract.tesseract_cmd = r'D:\SoftWare\OCR\tesseract.exe'

# 设置 TESSDATA_PREFIX 环境变量，这里需要替换为你的实际 tessdata 目录路径
os.environ['TESSDATA_PREFIX'] = r'D:\SoftWare\tessdata'
# 用于存储多次响应的字符串
response_text = ""

def capture_screen():
    # 精准截取目标区域（需根据实际场景调整坐标）
    region = (0, 100, 566, 747)  # left, top, width, height
    return pyautogui.screenshot(region=region)


def preprocess_image(image):
    # 缩放图像提高文字清晰度
    scaled_image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)
    # 降噪（高斯模糊）
    denoised_image = scaled_image.filter(ImageFilter.GaussianBlur(radius=1))
    # 转为灰度图
    gray_image = denoised_image.convert("L")
    # 转换为 OpenCV 格式
    img_cv = np.array(gray_image)
    # 自适应阈值二值化
    binary_image = cv2.adaptiveThreshold(img_cv, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # 转换回 PIL 格式
    binary_image = Image.fromarray(binary_image)
    return binary_image


def perform_ocr(image):
    # Tesseract 配置参数（语言、页面分割模式、引擎模式）
    config = r'--oem 3 --psm 11 -l chi_sim+eng'  # 尝试不同的 psm
    text = pytesseract.image_to_string(image, config=config)
    return text


def filter_text(text):
    # 定义正则表达式，匹配中英文和换行符
    pattern = re.compile(r'[\u4e00-\u9fa5a-zA-Z\n ]+')
    filtered_text = ''.join(pattern.findall(text))
    # 将连续的换行符替换为单个换行符
    filtered_text = re.sub(r'\n+', '\n', filtered_text)
    # 将多个连续空格替换为单个空格
    filtered_text = re.sub(r' +', ' ', filtered_text)
    return filtered_text


def detect_text_regions(image):
    img_cv = np.array(image)
    # 获取文字的位置信息
    data = pytesseract.image_to_data(img_cv, output_type=pytesseract.Output.DICT, config=r'--oem 3 --psm 11 -l chi_sim+eng')
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:  # 只处理置信度大于 60 的文字区域
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            # 在图像上绘制矩形框
            cv2.rectangle(img_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return img_cv


class Ws_Param(object):
    # 初始化
    def __init__(self, APIKey, APISecret, gpt_url):
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws, close_status_code, close_msg):
    global response_text
    print("### closed ###")
    print("完整响应内容:", response_text)


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(parameter)
    # 发送请求参数
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    global response_text
    data = json.loads(message)
    code = data['header']['code']
    choices = data["payload"]["choices"]
    status = choices["status"]
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    if 'text' in choices:
        for text in choices['text']:
            response_text += text['content']
    if status == 2:
        print("#### 关闭会话")
        ws.close()





def main(api_secret, api_key, gpt_url):
    wsParam = Ws_Param(api_key, api_secret, gpt_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == "__main__":
    screen_image = capture_screen()
    processed_image = preprocess_image(screen_image)
    result_text = perform_ocr(processed_image)
    filtered_result = filter_text(result_text)
    print("优化后识别结果:\n", filtered_result)

     # webSocket 请求的参数
    parameter = {
        "payload": {
            "message": {
                "text": [
                    {
                        "role": "system",
                        "content": "你是一个英语专家,我会给你一些选项，给我答案\n"
                    },
                    {
                        "role": "user",
                        "content": filtered_result+"这是一道英语题除了第一句话，其他都是选项，只需要给出尽可能全的答案选项即可"
                    }
                ]
            }
        },
        "parameter": {
            "chat": {
                "max_tokens": 4096,
                "domain": "generalv3.5",
                "top_k": 4,
                "temperature": 0.5
            }
        },
        "header": {
            "app_id": "38d7715a"
        }
    }

     # 检测并标记文字区域
    image_with_regions = detect_text_regions(processed_image)

    # 显示标记后的图像
    cv2.imshow('Text Regions', image_with_regions)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

   
     
    