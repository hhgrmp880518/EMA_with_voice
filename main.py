from __future__ import unicode_literals
import os, shutil, csv
import threading, time
from EMA.generator import*
from Linebot.bot import app, video_reply, error_reply
import globals
from datetime import datetime as dtime



class hintcolors:
    Success = '\033[1;38;5;81m[Success] \033[0m'
    Clear = '\033[1;38;5;226m[Clear] \033[0m'
    Failed = '\033[1;38;5;196m[Failed] \033[0m'

# 確認 static 資料夾存在
if not os.path.exists('./Linebot/static'):
    os.mkdir('./Linebot/static')

# 確認 recording.csv 存在
if not os.path.exists('./recording.csv'):
    with open(file='./recording.csv', mode='w', encoding='UTF-8') as initialize:
        writer = csv.writer(initialize)
        writer.writerow(['時間', '資料', '狀態', '備註'])

if __name__ == '__main__':
    # 將 LINE Bot 的應用放入執行緒獨立運作
    line_bot = threading.Thread(target=app.run)
    line_bot.start()

    while True:
        if globals.require_list != {}:
            # 抓取使用者資料 (user_id)、題目輸入(text)
            user_id = list(globals.require_list.keys())[0]
            text = globals.require_list[user_id].text
            StepText = globals.require_list[user_id].StepsText
            print('\033[1;38;5;82m[START] \033[0muser_id:{}, text:{}'.format(user_id, text))
            try:
                # 製作 EMA 封面和動畫
                generator(user_id)

                # 移除 Tex 資料夾
                if os.path.exists('./media/Tex'):
                    shutil.rmtree('./media/Tex')

                # 移除 texts 資料夾
                if os.path.exists('./media/texts'):
                    shutil.rmtree('./media/texts')

                video_reply(user_id)

                print('{}user_id:{}, text:{}'.format(hintcolors.Success, user_id, text))
                # 清除已完成的要求
                pop_data = globals.require_list.pop(user_id)
                print('{}user_id:{}, text:{}'.format(hintcolors.Clear, user_id, text))
                pop_data.finish = True

            except:
                error_reply(user_id)

                print('{}user_id:{}, text:{}'.format(hintcolors.Failed, user_id, text))
                
                pop_data = globals.require_list.pop(user_id)
                print('{}user_id:{}, text:{}'.format(hintcolors.Clear, user_id, text))

            with open(file='./recording.csv', mode='a', encoding='UTF-8', newline='') as new_recording:
                writer = csv.writer(new_recording)
                writer.writerow([f'[{dtime.fromtimestamp(pop_data.post_time)}]', pop_data.text, pop_data.finish, ''])

        else:
            # 等待 1 秒
            time.sleep(1)