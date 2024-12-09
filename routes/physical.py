from flask import Blueprint, render_template, request, redirect, url_for
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
