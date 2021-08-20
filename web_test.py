from flask import Flask, request, abort,render_template, redirect, flash, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)

#mysql連線
app.secret_key = "super secret key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "mysql"
app.config['MYSQL_DB'] = 'ques_data'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('Questionnaire.html')

    elif request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            gender = request.form['gender']
            age = request.form['age']
            height = request.form['height']
            weight = request.form['weight']
            disliked = request.form['disliked']
            health = request.form['health']
            fried = request.form['fried']
            vegetable = request.form['vegetable']
            activity = request.form['activity']

            cur = mysql.connection.cursor()
            increase = f"""INSERT INTO USER VALUES(
            '{username}',{email},{gender},{age},{height},{weight},{disliked},{health},{fried},{vegetable},{activity})"""
            cur.execute(increase)
            mysql.connection.commit()
            # mysql.connection.close()
            print('Item Created.')
            return '輸入完成請關掉此頁'

        except:
            print('Invalid input.')
            return '填寫失敗，可能原因(1)你已經填過(2)資料輸入格式有勿再試一次'

if __name__ == "__main__":
    app.run(debug = True)