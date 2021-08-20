from predict2 import Pred
import os
import pymysql
from ECdic import ECdic


# 資料庫設定
db_settings = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '7511',
    'db': 'food'
}
# Ingredients_List = ['bean_sprout', 'tofu_skin']
# 抓取營養素function
def Find_Nutrients(Ingredients_List):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT *
            FROM test
            ;
            """)
            record = cursor.fetchall()

        for Ingredient in Ingredients_List:
            print(Ingredient)
            for Nutrients in record:
                if Ingredient in Nutrients[0]:
                    # 轉list
                    Ingredient_to_list = list(Nutrients)
                    # 轉中文
                    Ingredient_name = Ingredient_to_list[0]
                    Ingredient_to_list[0] = ECdic().EtoC(Ingredient_name)
                    Ingredient_to_tuple = tuple(Ingredient_to_list)
                    print(Ingredient_to_tuple)
                    # print(Nutrients)
    except Exception as e:
        print(e.args)

# Find_Nutrients(Ingredients_List)
if __name__=="__main__":
    IMG = os.listdir("./img")
    for I in IMG:
        filepath = "./img"+"/"+ I
        classname = list(set(Pred().get_pred(filepath)))
        Pred().get_img(filepath)
        # os.remove(filepath)
    Ingredients_List = classname
    Find_Nutrients(Ingredients_List)

