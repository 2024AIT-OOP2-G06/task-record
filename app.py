from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
import sqlite3

app = Flask(__name__)

# データベースの初期化
# initialize_database()
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table;")

tables = cursor.fetchall()
if tables:
    print('テーブルあります')
else:
    initialize_database()
conn.close()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
