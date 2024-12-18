from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from models import User

# Blueprintの作成
user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/')
def list():
    
    # データ取得
    users = User.select()

    return render_template('user_list.html', title='ユーザー一覧', items=users)


@user_bp.route('/add', methods=['GET', 'POST'])
def add():
    # print("\n\n\n\n"+request.method+"\n\n\n\n\n")
    if request.method == 'POST':
        username = request.form['username']
        age = int(request.form['age'])
        
        # print("\n\n\n\n"+username+"\n\n\n\n\n")
        # print(type(username))
        # print("\n\n\n\n"+age+"\n\n\n\n\n")
        # print(type(age))
        # db.connect()
        # user_create = f"insert into users(username, age) values({username}, {age})"
        # db.execute_sql(user_create)
        # db.close()
        # return redirect(url_for('user.list'))
        User.create(username=username, age=age)

        # JSONファイルを更新
        from routes.circle import export_json
        export_json()

        return redirect('/users/')
    
    return render_template('user_add.html')


@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        user.username = request.form['username']
        user.age = request.form['age']
        user.save()

        # JSONファイルを更新
        from routes.circle import export_json
        export_json()

        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=user)

@user_bp.route("/test")
def test():
    return render_template("age_test.html")

# データ一覧（確認用）
# データベースから取得したデータを JSON 形式で返す
@user_bp.route('/data', methods=['GET'])
def get_age_data():
    users = User.select()
    data = [
        {
            "user": user.username,  # ユーザー名
            "age": int(user.age),   # 体温(float型に変換)
            "id": user.id               # 体温ID(横軸になる)

        }
        for user in users
    ]
    return jsonify(data)

@user_bp.route('/chart', methods=['GET'])
def show_chart():
    users = User.select()
    chart_data = [{"user": user.username, "age": user.age} for user in users]
    return render_template('age_test.html', title='年齢グラフ', chart_data=chart_data)
