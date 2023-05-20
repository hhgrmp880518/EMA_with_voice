from __future__ import unicode_literals
import execjs
import requests, json
import csv, time
import unicodedata
import globals
from EMA.explanatoryTools.tool import stringReplace
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from configparser import ConfigParser

from datetime import datetime as dtime

class media_data():
    def __init__(self, text: str, post_time: float, StepsText: list, finish: bool=False):
        self.text = text
        self.StepsText = StepsText
        self.post_time = post_time
        self.finish = finish

class hintcolors:
    Success = '\033[1;38;5;81m[Success] \033[0m'
    Clear = '\033[1;38;5;226m[Clear] \033[0m'
    Failed = '\033[1;38;5;196m[Failed] \033[0m'

# 導入 .js
def js_from_file(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result

# 將Flask框架導向目前運行程式的位置
app = Flask(__name__)

# 設定 Channel Access Token 與 Channel Secret
# 設定檔是 config.ini
line_bot_config = ConfigParser()
line_bot_config.read('./config.ini')
line_bot_api = LineBotApi(line_bot_config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(line_bot_config.get('line-bot', 'channel_secret'))
WebhookUrl = line_bot_config.get('line-bot', 'webhook_url')

# 建立 "/callback" 的路由被訪問的行為
@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature 頭部 (header) 資訊
    signature = request.headers['X-Line-Signature']
    
    # 取得 HTTP 請求的內容
    body = request.get_data(as_text=True)

    # 紀錄 HTTP 請求的內容
    app.logger.info("Request body: " + body)
    
    try:
        # 使用 handler 處理訊息
        handler.handle(body, signature)
    
    # 若驗證簽章失敗，則回應狀態碼 400
    except InvalidSignatureError:
        abort(400)

    # 回傳狀態碼 200，表示處理成功
    return 'OK'

# 當接收到文字訊息時，進行 quick_reply() 函式
@handler.add(MessageEvent, message=TextMessage)
def quick_reply(event):

    # 如果使用者不是連線測試，則將使用者的訊息記錄在 require_list 中
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.source.user_id in list(globals.require_list.keys()):
            # 回覆提醒使用者不要連續要求
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='前一部影片還沒生成完畢\n稍後再傳新的問題')
            )
        else:
            try:
                mathsteps = execjs.compile(js_from_file('./EMA/mathsteps/mathsteps.js'))
                text = unicodedata.normalize('NFKC', event.message.text)
                StepsText = mathsteps.call('steps', text)
                text = stringReplace(text)+' = ?'
                globals.require_list[event.source.user_id] = media_data(text, time.time(), StepsText)
                
                # 回覆使用者正在產生影片
                if len(list(globals.require_list.keys())) < 3:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='影片產生中，請等一下')
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='目前等待生成的影片繁多，請等一下')
                    )
            except:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='輸入的資料暫時不支援生成')
                )

                with open(file='../recording.csv', mode='a', encoding='UTF-8', newline='') as new_recording:
                    writer = csv.writer(new_recording)
                    writer.writerow([f'[{dtime.now()}]', text, False, 'MathStepError'])

def error_reply(user_id):
    headers = {'Authorization':'Bearer {}'.format(line_bot_config.get('line-bot', 'channel_access_token')),
                        'Content-Type':'application/json'}
    body = {'to':user_id,
            'messages':[{"type": "text", "text": "😢對不起，\n　我們遇到了預期外的錯誤\n\n⚠️暫時不要傳送相同題目⚠️\n\n如果您願意回報異常情形給開發團隊，請填寫以下表單：\n🔗https://forms.gle/LsX35K63vBwTyHQC8"}]}
    
    # 傳送錯誤資訊
    requests.request('POST', 'https://api.line.me/v2/bot/message/push',
                    headers=headers,
                    data=json.dumps(body).encode('utf-8'))
    
def video_reply(user_id):
    # 傳送設定
    headers = {'Authorization':'Bearer {}'.format(line_bot_config.get('line-bot', 'channel_access_token')),
            'Content-Type':'application/json'}
    body = {'to':user_id,
            'messages':[{"type": "video", "originalContentUrl": "{}/static/{}.mp4".format(WebhookUrl, user_id), "previewImageUrl": "{}/static/{}.png".format(WebhookUrl, user_id)}]}
    
    # 傳送 EMA 檔案
    requests.request('POST', 'https://api.line.me/v2/bot/message/push',
                    headers=headers,
                    data=json.dumps(body).encode('utf-8'))