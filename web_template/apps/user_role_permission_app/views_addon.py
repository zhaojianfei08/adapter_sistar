from flask import render_template, request, jsonify, session, redirect
from sqlalchemy import or_
from web_template.rbac import login_required
from . import user_role_permisson_app
from .models import User


@user_role_permisson_app.route('/index')
@login_required()
def index():
    login_user = session.get('login_user')
    return render_template('main.html', login_user=login_user)


@user_role_permisson_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name_or_email = request.json.get('loginEmail')
        password = request.json.get('loginPassword')
        user = User.query.filter(or_(User.name == name_or_email, User.email == name_or_email)).first()
        if not user:
            return jsonify({'status': False, 'message': 'User not found! please register first!'})
        login_user = user.check_password(password)
        if not login_user:
            return jsonify({'status': False, 'message': 'User or Password is not valid'})
        # 1 设置session 字段login_user
        session['login_user'] = user.name
        # 2 设置session 字段
        permission_list = []
        for role in user.roles:
            for permission in role.permissions:
                permission_list.append(permission.name)
        session['user_permissions'] = permission_list
        return jsonify({'status': True, 'message': 'Login success!'})
    return render_template('login.html')


@user_role_permisson_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.json.get('registerName')
            email = request.json.get('registerEmail')
            password = request.json.get('registerPassword')
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()
            return jsonify({'status': True, 'message': 'User created'})
        except Exception as e:
            return jsonify({'status': False, 'message': str(e)})
    return render_template('register.html')


@user_role_permisson_app.route('/logout')
@login_required()
def logout():
    try:
        session.pop('login_user')
        session.pop('user_permissions')
        return redirect('/rbac/login')
    except Exception as e:
        return jsonify({'status': True, 'message': str(e)})



