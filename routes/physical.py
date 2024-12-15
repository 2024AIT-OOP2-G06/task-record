from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import Physical, User

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
        bad_good = request.form['bad_good'] == '1'  # '1'ならTrue, それ以外はFalse
        bad_content = request.form.get('bad_content', '')  # 空でもOK
        Physical.create(user=user_id, temp=temp, bad_good=bad_good, bad_content=bad_content)
        return redirect(url_for('physical.list'))
    
    users = User.select()
    return render_template('physical_add.html', users=users)


@physical_bp.route('/edit/<int:physical_id>', methods=['GET', 'POST'])
def edit(physical_id):
    physical = Physical.get_or_none(Physical.id == physical_id)
    if not physical:
        return redirect(url_for('physical.list'))

    if request.method == 'POST':
        physical.user = request.form['user_id']
        physical.temp = request.form['temp']
        physical.bad_good = request.form['bad_good'] == '1'
        physical.bad_content = request.form.get('bad_content', '')
        physical.save()
        return redirect(url_for('physical.list'))

    users = User.select()
    return render_template('physical_edit.html', physical=physical, users=users)


# データ一覧（確認用）
# データベースから取得したデータを JSON 形式で返す
@physical_bp.route('/data', methods=['GET'])
def get_temperature_data():
    physicals = Physical.select()
    data = [
        {
            "user": physical.user.username,  # ユーザー名
            "temp": float(physical.temp),   # 体温(float型に変換)
            "id": physical.id               # 体温ID(横軸になる)
        }
        for physical in physicals
    ]
    return jsonify(data)


# グラフ表示
@physical_bp.route('/chart', methods=['GET'])
def show_chart():
    return render_template('temp_chart.html', title='体温グラフ')
