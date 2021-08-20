# coding: utf-8
import test
import urllib.parse
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import paired_distances,cosine_similarity
import pymysql
import pymongo


#得到相關資訊



def recipetempelete(left):
    if len(left) >= 6:
        myfinallist = []


        for content in left[0:6]:
            singlelist = []
            name = content[0]
            imgurl = content[1]
            ingredient = content[2]
            singlelist.append(imgurl)   #得到網址
            singlelist.append(name)     #得到名稱
            singlelist.append(ingredient) #得到食材
            urlname = urllib.parse.quote(name)
            #做youtube搜尋

            ytname = f'https://www.youtube.com/results?search_query={urlname}'
            singlelist.append(ytname)    #得到影片網址
            #新增食譜連結
            if imgurl[0:11] == r'https://img':

                url = f"https://cook1cook.com/search?keyword={urlname}&theme=recipe"
                singlelist.append(url)#得到食譜
            elif imgurl[0:11] == r'https://tok':

                url = f'https://icook.tw/search/{urlname}'
                singlelist.append(url) #得到食譜
            #營養素搜尋
            nutrientsentence = ''
            for nutrient, weight in content[5].items():
                nutrientsentence += (f'{nutrient}含有: {weight}\n')

            singlelist.append(nutrientsentence) #得到營養素

            myfinallist.append(singlelist) #回傳最終結果回去
        return myfinallist
    elif left ==[]:
        return '{查無符合資料}'

    else:
        myfinallist = []

        for content in left[0:len(left)]:
            singlelist = []
            name = content[0]
            imgurl = content[1]
            ingredient = content[2]
            singlelist.append(imgurl)  # 得到圖片網址
            singlelist.append(name)  # 得到名稱
            singlelist.append(ingredient)  # 得到食材

            # 做youtube搜尋
            ytname = f'https://www.youtube.com/results?search_query={name}'
            singlelist.append(ytname)  # 得到影片網址
            # 新增食譜連結
            if imgurl[0:11] == r'https://img':

                url = f"https://cook1cook.com/search?keyword={name}&theme=recipe"
                singlelist.append(url)  # 得到食譜
            elif imgurl[0:11] == r'https://tok':

                url = f'https://icook.tw/search/{name}'
                singlelist.append(url)  # 得到食譜
            # 營養素搜尋
            nutrientsentence = ''
            for nutrient, weight in content[5].items():
                nutrientsentence += (f'營養素名:{nutrient},重量:{weight}\n')

            singlelist.append(nutrientsentence)  # 得到營養素

            myfinallist.append(singlelist)  # 回傳最終結果回去
        return myfinallist

# print(len(left))
# print(recipetempelete(left))

########################################################################

#回傳範本
# def input_column(recipes):
#     if recipes == '{查無符合資料}':
#         # text_message = TextSendMessage(text='查無符合資料')
#         # line_bot_api.reply_message(event.reply_token, text_message)
#         return "error"
#
#     else:
#         columnlist=[]
#         for recipe in recipes:
#
#             column = CarouselColumn(
#                     thumbnail_image_url=f'{recipe[0]}',
#                     title=f'{recipe[1]}',
#                     text=f'{recipe[2]}',
#                     actions=[
#                         URITemplateAction(
#                             label=f'{recipe[1]}作法影片',
#                             uri=f'{recipe[3]}'),
#                         URITemplateAction(
#                             label=f'{recipe[1]}食譜查詢',
#                             uri= f'{recipe[4]}'),
#                         MessageTemplateAction(
#                             label=f'{recipe[1]}營養素',
#                             text=f'{recipe[5]}')
#                     ]
#             )
#             columnlist.append(column)
#         # Carousel_template = TemplateSendMessage(
#             # alt_text='Carousel template',
#             # template=CarouselTemplate(
#                 # columns=columnlist))
#         # line_bot_api.reply_message(event.reply_token,Carousel_template)
#             print(columnlist)


# def leftoverRecipe(leftover):
#     # SQL settings
#     db_settings = {
#     'host': '127.0.0.1',
#     'port': 3306,
#     'user': 'test',
#     'password': 'test',
#     'db': 'my_db'
#     }
#     # 連接到 MySQL
#     conn = pymysql.connect(**db_settings)
#     # 讀取 view_recipe_energe
#     get_energe = """SELECT id, Calorie_correction, Moisture, 
#                            Crude_protein, Crude_fat, Saturated_fat, Total_carbohydrates
#                            FROM view_recipe_energe;"""
#     energe = pd.read_sql(get_energe, conn)
#     energe.columns = ['id', '修正熱量', '水分', '粗蛋白',
#                       '粗脂肪', '飽和脂肪', '總碳水化合物']
#     # 從 view_recipe_energe 取出 recipe 的 id
#     cache_id = energe.iloc[:, 0].to_list()
#     # 讀取 recipe_to_sql
#     get_recipe = f"SELECT * FROM recipe_to_sql;"
#     recipes = pd.read_sql(get_recipe, conn)
#     # 連接到 MongoDB
#     mongo_info = "mongodb+srv://lukelee:cfb101@cluster0.lfpkd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
#     client = pymongo.MongoClient(mongo_info)
#     # MongoDB database
#     db = client.food
#     # MongoDB collection
#     monrecipe = db.recipe
#     outputs = list()
#     for i in cache_id:
#         recipe = recipes.loc[recipes["id"] == i]
#         mates = recipe["material"].to_list()
#         # 若包含該食譜所有食材
#         if all(m in leftover for m in mates):
#             # get recipe info from MongoDB
#             mongoData = monrecipe.find_one({'id': str(i)},
#                                         {'id': 0, '_id': 0, '料理時間': 0, '簡介': 0, '作者': 0})
#             output = [v for k,v in mongoData.items()]
#             # get recipe_energe info from view_recipe_energe
#             recipe_energe = energe.loc[energe["id"] == i].drop(["id"], axis=1).to_dict("records")[0]
#             output.append(recipe_energe)
#             outputs.append(output)
#     return outputs

def recipe_temp(recipes):
    if recipes == '{查無符合資料}':
        return "error"
    else:
        temlist = []
        for recipe in recipes:

            a = {
              "type": "bubble",
              "size": "micro",
              "hero": {
                "type": "image",
                "url": f"{recipe[0]}",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "320:213"
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{recipe[1]}"
                  },
                  {
                    "type": "text",
                    "text": f"{recipe[2]}",
                    "weight": "bold",
                    "size": "sm",
                    "wrap": True
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": []
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "uri",
                          "label": '作法影片',
                          "uri": f'{recipe[3]}'
                        },
                        "style": "primary",
                        "color": "#FF8282"
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "uri",
                          "label": '食譜查詢',
                          "uri": f'{recipe[4]}'
                        },
                        "style": "primary",
                        "color": "#FF8C8C"
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": '營養素',
                          "text": f'{recipe[5]}'
                        },
                        "style": "primary",
                        "color": "#FF9696"
                      }
                    ]
                  }
                ],
                "spacing": "sm",
                "paddingAll": "13px"
              }
            }

            temlist.append(a)
        content = {"type": "carousel", "contents":temlist}
        return content


# recipelist = test.left()
# recipes = recipetempelete(recipelist)
# a = recipe_temp(recipes)

# print(a)


# b= f'str({"type": "carousel", "contents":[{}]})'
# print(type(b))

def get_the_most_similar_receipes(searchUserId, num):
    receipes = pd.read_csv('./recipe_group.csv')
    like = pd.read_csv('./userid_like.csv')
    df = pd.merge(like, receipes, on='id')
    # 建立receipe的特徵矩陣
    oneHot = pd.get_dummies(receipes["Cluster_category"].astype(str))  # One-Hot Encoding
    receipe_arr = pd.concat([receipes, oneHot], axis=1)
    receipe_arr.drop("Cluster_category", axis=1, inplace=True)
    receipe_arr.set_index("id", inplace=True)
    # 建立user的特徵矩陣
    oneHot = pd.get_dummies(df["Cluster_category"].astype(str))  # One-Hot Encoding
    user_arr = pd.concat([df, oneHot], axis=1)
    user_arr.drop(["id", "like", "Cluster_category"], axis=1, inplace=True)
    user_arr = user_arr.groupby('userid').mean()
    similar_matrix = cosine_similarity(user_arr.values, receipe_arr.values)
    similar_matrix = pd.DataFrame(similar_matrix, index=user_arr.index, columns=receipe_arr.index)
    vec = similar_matrix.loc[searchUserId].values
    sorted_index = np.argsort(-vec)[:num]   #找距離最短
    return list(similar_matrix.columns[sorted_index])


# def leftoverRecipe(leftover, member_id):
#     # SQL settings
#     db_settings = {
#     'host': '127.0.0.1',
#     'port': 3306,
#     'user': 'test',
#     'password': 'test',
#     'db': 'my_db'
#     }
#     # 連接到 MySQL
#     conn = pymysql.connect(**db_settings)
#     # 讀取 view_recipe_energe
#     get_energe = "SELECT * FROM view_recipe_energe;"
#     energe = pd.read_sql(get_energe, conn)
#     energe.columns = ['id', '修正熱量', '水分', '粗蛋白',
#                       '粗脂肪', '飽和脂肪', '總碳水化合物',
#                       '膳食纖維', '糖質總量', '葡萄糖',
#                       '果糖', '半乳糖', '麥芽糖',
#                       '蔗糖', '乳糖', '鈉',
#                       '鉀', '鈣', '鎂',
#                       '鐵', '鋅','磷',
#                       '銅', '錳', '維生素B1',
#                       '維生素B2', '維生素B6', '維生素B12',
#                       '維生素C', '葉酸', '維生素A',
#                       '維生素D', '維生素E']
#     get_membership = "SELECT * FROM membership;"
#     membership = pd.read_sql(get_membership, conn)
#     dislike = membership.loc[membership["user_id"] == i, "disliked"].to_list()[0]
    
#     # 從 view_recipe_energe 取出 recipe 的 id
#     cache_id = energe.iloc[:, 0].to_list()
#     # 讀取 recipe_to_sql
#     get_recipe = "SELECT * FROM recipe_to_sql_2;"
#     recipes = pd.read_sql(get_recipe, conn)
#     # 連接到 MongoDB
#     mongo_info = "mongodb+srv://lukelee:cfb101@cluster0.lfpkd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
#     client = pymongo.MongoClient(mongo_info)
#     # MongoDB database
#     db = client.food
#     # MongoDB collection
#     monrecipe = db.recipe
#     outputs = list()
#     for i in cache_id:
#         recipe = recipes.loc[recipes["id"] == i]
#         mates = recipe["material_zh"].to_list()
#         # 若包含該食譜所有食材
#         if all(m in leftover for m in mates) and dislike not in mates:
#             # get recipe info from MongoDB
#             mongoData = monrecipe.find_one({'id': str(i)},
#                                         {'id': 0, '_id': 0, '料理時間': 0, '簡介': 0, '作者': 0})
#             output = [v for k,v in mongoData.items()]
#             # get recipe_energe info from view_recipe_energe
#             recipe_energe = energe.loc[energe["id"] == i].drop(["id"], axis=1).to_dict("records")[0]
#             output.append(recipe_energe)
#             outputs.append(output)
#     return outputs




def leftoverRecipe(leftover, member_id):
    # SQL settings
    db_settings = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'test',
    'password': 'test',
    'db': 'my_db'
    }
    # 連接到 MySQL
    conn = pymysql.connect(**db_settings)
    # 讀取 view_recipe_energe
    get_energe = "SELECT id, Calorie_correction, Moisture,Crude_protein, Crude_fat, Saturated_fat, Total_carbohydrates                     FROM view_recipe_energe;"
    energe = pd.read_sql(get_energe, conn)
    energe.columns = ['id', '修正熱量', '水分', '粗蛋白',
                      '粗脂肪', '飽和脂肪', '總碳水化合物']
    get_membership = "SELECT * FROM membership;"
    membership = pd.read_sql(get_membership, conn)
    dislike = membership.loc[membership["user_id"] == member_id, "disliked"].to_list()[0]
    
    # 從 view_recipe_energe 取出 recipe 的 id
    cache_id = energe.iloc[:, 0].to_list()
    # 讀取 recipe_to_sql
    get_recipe = "SELECT * FROM recipe_to_sql_2;"
    recipes = pd.read_sql(get_recipe, conn)
    # 連接到 MongoDB
    mongo_info = "mongodb+srv://lukelee:cfb101@cluster0.lfpkd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_info)
    # MongoDB database
    db = client.food
    # MongoDB collection
    monrecipe = db.recipe
    outputs = list()
    for i in cache_id:
        recipe = recipes.loc[recipes["id"] ==i]
        mates = recipe["material_zh"].to_list()
        # 若包含該食譜所有食材
        if all(m in leftover for m in mates) and dislike not in mates:
            # get recipe info from MongoDB
            mongoData = monrecipe.find_one({'id': str(i)},
                                        {'id': 0, '_id': 0, '料理時間': 0, '簡介': 0, '作者': 0})
            output = [v for k,v in mongoData.items()]
            # get recipe_energe info from view_recipe_energe
            recipe_energe = energe.loc[energe["id"] == i].drop(["id"], axis=1).to_dict("records")[0]
            output.append(recipe_energe)
            outputs.append(output)
    return outputs

def leftoverid(id_list, member_id):
    # SQL settings
    db_settings = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'test',
    'password': 'test',
    'db': 'my_db'
    }
    # 連接到 MySQL
    conn = pymysql.connect(**db_settings)
    # 讀取 view_recipe_energe
    get_energe = "SELECT id, Calorie_correction, Moisture,Crude_protein, Crude_fat, Saturated_fat, Total_carbohydrates                     FROM view_recipe_energe;"
    energe = pd.read_sql(get_energe, conn)
    energe.columns = ['id', '修正熱量', '水分', '粗蛋白',
                      '粗脂肪', '飽和脂肪', '總碳水化合物']
    get_membership = "SELECT * FROM membership;"
    membership = pd.read_sql(get_membership, conn)
    dislike = membership.loc[membership["user_id"] == member_id, "disliked"].to_list()[0]
    
    # 從 view_recipe_energe 取出 recipe 的 id
    cache_id = id_list
    # 讀取 recipe_to_sql
    get_recipe = "SELECT * FROM recipe_to_sql_2;"
    recipes = pd.read_sql(get_recipe, conn)
    # 連接到 MongoDB
    mongo_info = "mongodb+srv://lukelee:cfb101@cluster0.lfpkd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_info)
    # MongoDB database
    db = client.food
    # MongoDB collection
    monrecipe = db.recipe
    outputs = list()
    for i in cache_id:
        recipe = recipes.loc[recipes["id"] ==i]
        mates = recipe["material_zh"].to_list()
        # 若包含該食譜所有食材
        if dislike not in mates:
            # get recipe info from MongoDB
            mongoData = monrecipe.find_one({'id': str(i)},
                                        {'id': 0, '_id': 0, '料理時間': 0, '簡介': 0, '作者': 0})
            output = [v for k,v in mongoData.items()]
            # get recipe_energe info from view_recipe_energe
            recipe_energe = energe.loc[energe["id"] == i].drop(["id"], axis=1).to_dict("records")[0]
            output.append(recipe_energe)
            outputs.append(output)
    return outputs








