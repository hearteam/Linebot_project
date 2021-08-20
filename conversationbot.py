# 載入需要的模組
from __future__ import unicode_literals
import os
import random
import string
import json
import pymysql
from flask import Flask, request, abort,render_template, redirect, flash, url_for
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import configparser
from linebot.models import MessageEvent,ImageMessage ,TextMessage, TextSendMessage,ImageSendMessage,TemplateSendMessage,ButtonsTemplate,PostbackTemplateAction,FlexSendMessage,CarouselTemplate,PostbackEvent,PostbackTemplateAction,URITemplateAction,MessageTemplateAction
# from flask_mysqldb import MySQL
import jieba
import inverted_index
import tool,test
# from yolo import predict2 as predict
import pyimgur
import pandas as pd




app = Flask(__name__)
CONFIG = json.load(open("config.json", "r"))

# LINE 聊天機器人的基本資料

LINE_SECRET = CONFIG["linebot"]["line_secret"]
LINE_TOKEN = CONFIG["linebot"]["line_token"]
line_bot_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

#mysql連線
# app.secret_key = "super secret key"
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = "root"
# app.config['MYSQL_PASSWORD'] = "mysql"
# app.config['MYSQL_DB'] = 'ques_data'
# mysql = MySQL(app)
conn = pymysql.connect(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8')

#imgur連線
CLIENT_ID = CONFIG["imgur"]["client_id"]

#liff連線
liffid = CONFIG["liff"]["liff_id"]

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#LIFT靜態頁面
@app.route('/page')
def page():
    return render_template('book.html')


# #接收表單
# @app.route('/', methods=['GET', 'POST'])
# def register():
#
#
#     if request.method == 'GET':
#         return render_template('Question.html')
#
#     elif request.method == 'POST':
#         try:
#             # username = user_id
#             username = request.form['username']
#             email = request.form['email']
#             gender = request.form['gender']
#             age = request.form['age']
#             height = request.form['height']
#             weight = request.form['weight']
#             disliked = request.form['disliked']
#             health = request.form['health']
#             fried = request.form['fried']
#             vegetable = request.form['vegetable']
#             activity = request.form['activity']
#             cur = mysql.connection.cursor()
#             sqlcommit = f"""INSERT INTO USER VALUES(
#             '{username}','{email}',{gender},{age},{height},{weight},'{disliked}',{health},{fried},{vegetable},{activity})"""
#             cur.execute(sqlcommit)
#             mysql.connection.commit()
#             flash('Item Created.')
#             return '輸入完成請關掉此頁'
#
#         except:
#             flash('Invalid input.')
#             return '填寫失敗，可能原因(1)你已經填過(2)資料輸入格式有勿再試一次'

#設計回應程式文字
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if isinstance(event.message, TextMessage):
        msg = event.message.text
        user_id =event.source.user_id
        # if msg == "張銘勛":
        #     txt = '帥哥'
        #     fig_url = 'https://s.rfi.fr/media/display/7885189c-10a1-11ea-bb1a-005056a99247/w:980/p:16x9/panda_0.webp'
        #     url2 = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'
        #     cur = mysql.connection.cursor()
        #
        #     mydata = ''
        #     cur.execute('SELECT * FROM my_db.customer')
        #     result = cur.fetchall()
        #     for r in result:
        #         mydata += str(r)
        #
        #
        #
        #
        #
        #     reply = [TextSendMessage(text=txt),
        #              ImageSendMessage(original_content_url=url2,preview_image_url=url2),
        #              TextSendMessage(text=mydata)
        #              ]
        #
        #     line_bot_api.reply_message(
        #         event.reply_token,reply)
        #建立資料表
        if msg[0:3] == '###':

            sentence = '###085/778/男/17歲以下/616/999/124/是/是/是/輕度活動'
            source = sentence.split('/')
            username = source[0].split('###')[1]
            user_id = user_id
            email = source[1]
            gender = source[2]
            age = source[3]
            height = source[4]
            weight = source[5]
            disliked = source[6]
            health = source[7]
            fried = source[8]
            vegetable = source[9]
            activity = source[10]

            mycursor = conn.cursor()
            mycursor.execute(f'SELECT * FROM membership where user_id = {user_id}')
            result = cursor.fetchall()
            if len(result) == 0:
                mycursor = conn.cursor()
                increase = f"""INSERT INTO MEMBER VALUES(
                         '{username}','{user_id}','{email}','{gender}','{age}','{height}','{weight}','{disliked}','{health}','{fried}','{vegetable}','{activity}')"""
                mycursor.execute(increase)
                conn.commit()

            else:
                mycursor = conn.cursor()
                delete = f"""delete from membership where user_id = {user_id}
                m
                """
                mycursor.execute(delete)
                conn.commit()
                mycursor = conn.cursor()
                increase = f"""INSERT INTO MEMBER VALUES(
                                         '{username}','{user_id}','{email}','{gender}','{age}','{height}','{weight}','{disliked}','{health}','{fried}','{vegetable}','{activity}')"""
                mycursor.execute(increase)
                conn.commit()


        elif msg[0:3] == '我覺得':
            sentence = msg.split('我覺得')[1]
            recommend = inverted_index.main(sentence)
            txt = f'您欠缺{recommend}'
            reply = [TextSendMessage(text=txt)]
            result1 = recommend.split('以及')[0]
            result2 = recommend.split('以及')[1]
            find = []
            #找尋營養素
            mycursor = conn.cursor()
            sql = f'''selet * from nutrient_tofood where nutrient = {result1}'''
            mycursor.execute(sql)
            result = mycursor.fetchone()
            find.append(list(result))

            mycursor = conn.cursor()
            sql = f'''selet * from nutrient_tofood where nutrient = {result2}'''
            mycursor.execute(sql)
            result = mycursor.fetchone()
            find.append(list(result))
            active = True
            finalfind = []
            while active:
                left=list(random.choice(find))
                finalfind.append(left)
                recipelist = tool.leftoverRecipe(left)
                recipes = tool.recipetempelete(recipelist)
                if tool.recipe_temp(recipes) == 'error':
                    pass
                else:
                    active = False
            left = list(finalfind[-1])
            recipelist = tool.leftoverRecipe(left)
            recipes = tool.recipetempelete(recipelist)
            flex_message =FlexSendMessage(alt_text='stock_name',  # alt_text
                contents=tool.recipe_temp(recipes))

            reply.append(flex_message)









            line_bot_api.reply_message(
                event.reply_token, reply)

        elif msg[0:3] == '歡迎使':
            flex_message = FlexSendMessage(
                alt_text='stock_name',
                contents={
                              "type": "bubble",
                              "hero": {
                                "type": "image",
                                "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTn3-Z0Df6pifp7UT3vrgn6oUdxaDnkSby-0Q&usqp=CAU",
                                "size": "full",
                                "aspectRatio": "20:13",
                                "aspectMode": "cover",
                                "backgroundColor": "#BD0000"
                              },
                              "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "text",
                                    "weight": "bold",
                                    "size": "xl",
                                    "text": "請選擇你追求的喜好"
                                  }
                                ]
                              },
                              "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "contents": [
                                  {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                      "type": "postback",
                                      "label": "增肌",
                                      "data": "goal=增肌&id=1001",
                                      "displayText": "推薦您增肌的食譜"
                                    },
                                    "position": "relative",
                                    "color": "#FFA1A1"
                                  },
                                  {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                      "type": "postback",
                                      "label": "美白",
                                      "data": "goal=美白&id=1002",
                                      "displayText": "推薦您美白的食譜"
                                    },
                                    "color": "#FFA1A1"
                                  },
                                  {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                      "type": "postback",
                                      "label": "護眼",
                                      "data": "goal=護眼&id=1003",
                                      "displayText": "推薦您護眼的食譜"
                                    },
                                    "color": "#FFA1A1"
                                  },
                                  {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                      "type": "postback",
                                      "label": "提神醒腦",
                                      "data": "goal=提神醒腦&id=1004",
                                      "displayText": "推薦您提神醒腦的食譜"
                                    },
                                    "color": "#FFA1A1"
                                  },
                                  {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                      "type": "postback",
                                      "label": "消除疲勞",
                                      "data": "goal=消除疲勞&1005",
                                      "displayText": "推薦您消除疲勞的食譜"
                                    },
                                    "color": "#FFA1A1"
                                  }
                                ],
                                "flex": 0,
                                "background": {
                                  "type": "linearGradient",
                                  "angle": "0deg",
                                  "startColor": "#ffffff",
                                  "endColor": "#ffffff"
                                }
                              },
                              "styles": {
                                "hero": {
                                  "backgroundColor": "#A36A00"
                                },
                                "body": {
                                  "separator": False,
                                  "backgroundColor": "#BFFFFF"
                                },
                                "footer": {
                                  "separator": True,
                                  "backgroundColor": "#FFA1A1"
                                }
                              }
                            }  # 貼進來
            )
            line_bot_api.reply_message(event.reply_token, flex_message)


        elif msg[0:3] == '我剩下':

            left = msg.split('我剩下')[1].split(' ')
            recipelist = tool.leftoverRecipe(left)
            # recipelist = test.left()  #測試用
            recipes = tool.recipetempelete(recipelist)
            if tool.recipe_temp(recipes) == 'error':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='查無符合結果'))
            else:
                flex_message = FlexSendMessage(
                    alt_text='stock_name',  # alt_text
                    contents=tool.recipe_temp(recipes))
                line_bot_api.reply_message(event.reply_token, flex_message)


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data[0:4] == "goal":
        searchUserId = event.postback.data[-4:]
        tool.get_the_most_similar_receipes(searchUserId,5)
        ###id 對應的食譜
        recipes = tool.recipetempelete(recipelist)
        if tool.recipe_temp(recipes) == 'error':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='查無符合結果'))
        else:
            flex_message = FlexSendMessage(
                alt_text='stock_name',  # alt_text
                contents=tool.recipe_temp(recipes))
            line_bot_api.reply_message(event.reply_token, flex_message)



        # line_bot_api.reply_message(
        #     event.reply_token, TextSendMessage(text=command))










#設計程式圖片
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    # image_name = ''.join(random.choice(string.ascii_letters+string.digits) for x in range(1))
    # image_name = image_name.upper()+'.png'
    image_name = 'yolo1'+'.png'
    path = './img/' + image_name
    with open(path, 'wb') as fd:   #寫入圖片
        for chunk in message_content.iter_content():
            fd.write(chunk)
    os.system("python ./turnback.py")

    filename = './imageoutput/'+image_name

    title = "Uploaded with PyImgur"
    im = pyimgur.Imgur(CLIENT_ID)

    uploaded_image = im.upload_image(filename, title=title)
    link = uploaded_image.link
    print(link)


    line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=link,preview_image_url=link))







if __name__ == "__main__":
    app.run(debug = True)