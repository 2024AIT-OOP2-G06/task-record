from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import Physical, User, Task
from peewee import fn

# Blueprintの作成
physical_bp = Blueprint('physical', __name__, url_prefix='/physicals')


@physical_bp.route('/')
def list():
    physicals = Physical.select()
    return render_template('physical_list.html', title='アンケート一覧', items=physicals)


@physical_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        temp = request.form['temp']
        task_id = request.form['task_id']
        bad_good = request.form['bad_good'] == '1'  # '1'ならTrue, それ以外はFalse
        bad_content = request.form.get('bad_content', '')  # 空でもOK
        Physical.create(user=user_id, temp=temp, task=task_id, bad_good=bad_good, bad_content=bad_content)
        return redirect(url_for('physical.list'))
    
    users = User.select()
    tasks = Task.select()
    return render_template('physical_add.html', users=users, tasks=tasks)


@physical_bp.route('/edit/<int:physical_id>', methods=['GET', 'POST'])
def edit(physical_id):
    physical = Physical.get_or_none(Physical.id == physical_id)
    if not physical:
        return redirect(url_for('physical.list'))

    if request.method == 'POST':
        physical.user = request.form['user_id']
        physical.temp = request.form['temp']
        physical.task = request.form['task_id']
        physical.bad_good = request.form['bad_good'] == '1'
        physical.bad_content = request.form.get('bad_content', '')
        physical.save()
        return redirect(url_for('physical.list'))

    users = User.select()
    tasks = Task.select()
    return render_template('physical_edit.html', physical=physical, users=users, tasks=tasks)


# データ一覧 (temp_chart.html)
# データベースから取得したデータを JSON 形式で返す
@physical_bp.route('/temp_chart_data', methods=['GET'])
def get_temperature_data():
    physicals = Physical.select()
    data = [
        {
            "user": physical.user.username,  # ユーザー名
            "temp": float(physical.temp),   # 体温(float型に変換)
            "bad_good": float(physical.bad_good),   # 体調不良の有無
            "bad_content": physical.bad_content,  # 体調不良の内容
            "id": physical.id               # ID
        }
        for physical in physicals
    ]
    return jsonify(data)


# グラフ表示 (temp_chart.html)
@physical_bp.route('/temp_chart', methods=['GET', 'POST'])
def show_chart():
    users = User.select()  # 全ユーザーを取得
    username = None        # 選択されたユーザー名（初期値）

    if request.method == 'POST':
        # フォームから選択されたユーザーIDを取得
        user_id = request.form.get('user_id')

        # ユーザーIDに基づいてデータベースからユーザーを取得
        selected_user = User.get_or_none(User.id == user_id)
        if selected_user:
            username = selected_user.username  # ユーザー名を取得

    return render_template('temp_chart.html', users=users, username=username)


# データ一覧 (task_chart.html)
@physical_bp.route('/task_chart_data', methods=['GET'])
def average_temp_by_task():
    # Peeweeのクエリで業務種別ごとの平均体温を計算
    query = (
        Physical
        .select(Task.task_name.alias('task_name'), fn.AVG(Physical.temp).alias('avg_temp'))
        .join(Task)
        .group_by(Task.task_name)
    )
    # 結果を辞書形式で作成
    data = [
        {
            "task": result.task.task_name,  # 業務種 (Physical.task経由でTask.task_nameにアクセス)
            "avg_temp": float(result.avg_temp)  # 平均体温
        } for result in query
    ]
    return jsonify(data)


# グラフ表示 (task_chart.html)
@physical_bp.route('/task_chart', methods=['GET'])
def show_task_chart():
    return render_template('task_chart.html')
