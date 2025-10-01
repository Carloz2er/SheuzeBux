from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from models import User, mongo
from auth import login_required
from bson import ObjectId
import bcrypt
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user_id' in session:
            user = User.find_by_id(session['user_id'])
            if user:
                if user.get('role') in ['admin', 'super_admin']:
                    return redirect(url_for('admin.dashboard'))
                else:
                    return redirect(url_for('index'))
        return render_template('auth/login.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('auth/login.html')
        
        user = User.find_by_email(email)
        
        # Debug: Verificar o que está retornando
        print(f"DEBUG: User found: {user is not None}")
        if user:
            print(f"DEBUG: User role: {user.get('role')}")
            print(f"DEBUG: Password type: {type(user.get('password'))}")
        
        if user and User.verify_password(user, password):
            if not user.get('is_active', True):
                flash('Sua conta está desativada. Entre em contato com o suporte.', 'danger')
                return render_template('auth/login.html')
            
            # Login bem-sucedido
            session['user_id'] = str(user['_id'])
            session.permanent = True
            
            flash(f'Bem-vindo de volta, {user["username"]}!', 'success')
            
            if user.get('role') in ['admin', 'super_admin']:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos.', 'danger')
            return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect(url_for('index'))
        return render_template('auth/register.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validações
        if not all([username, email, password, confirm_password]):
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'danger')
            return render_template('auth/register.html')
        
        # Verificar se email já existe
        if User.find_by_email(email):
            flash('Este email já está cadastrado.', 'danger')
            return render_template('auth/register.html')
        
        # Verificar se username já existe
        if mongo.db.users.find_one({'username': username}):
            flash('Este nome de usuário já está em uso.', 'danger')
            return render_template('auth/register.html')
        
        try:
            # Criar usuário
            result = User.create_user(
                username=username,
                email=email,
                password=password,
                role='user'
            )
            
            if result.inserted_id:
                flash('Conta criada com sucesso! Faça login para continuar.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Erro ao criar conta. Tente novamente.', 'danger')
            
        except Exception as e:
            print(f"DEBUG: Error creating user: {e}")
            flash('Erro ao criar conta. Tente novamente.', 'danger')
        
        return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    user = User.find_by_id(session['user_id'])
    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.login'))
    
    orders = list(mongo.db.orders.find({'user_id': ObjectId(session['user_id'])}).sort('created_at', -1))
    
    return render_template('store/profile.html', user=user, orders=orders)

@auth_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        
        user = User.find_by_id(session['user_id'])
        if not user:
            flash('Usuário não encontrado.', 'danger')
            return redirect(url_for('auth.profile'))
        
        update_data = {}
        
        # Verificar senha atual para alterações sensíveis
        if username != user['username'] or email != user['email'] or new_password:
            if not current_password or not User.verify_password(user, current_password):
                flash('Senha atual incorreta.', 'danger')
                return redirect(url_for('auth.profile'))
        
        # Atualizar username se necessário
        if username != user['username']:
            if mongo.db.users.find_one({'username': username, '_id': {'$ne': ObjectId(session['user_id'])}}):
                flash('Este nome de usuário já está em uso.', 'danger')
                return redirect(url_for('auth.profile'))
            update_data['username'] = username
        
        # Atualizar email se necessário
        if email != user['email']:
            if User.find_by_email(email):
                flash('Este email já está cadastrado.', 'danger')
                return redirect(url_for('auth.profile'))
            update_data['email'] = email
        
        # Atualizar senha se fornecida
        if new_password:
            if len(new_password) < 6:
                flash('A nova senha deve ter pelo menos 6 caracteres.', 'danger')
                return redirect(url_for('auth.profile'))
            update_data['password'] = new_password
        
        if update_data:
            User.update_user(session['user_id'], update_data)
            flash('Perfil atualizado com sucesso!', 'success')
        else:
            flash('Nenhuma alteração foi feita.', 'info')
        
        return redirect(url_for('auth.profile'))
    
    except Exception as e:
        print(f"DEBUG: Error updating profile: {e}")
        flash('Erro ao atualizar perfil.', 'danger')
        return redirect(url_for('auth.profile'))

@auth_bp.route('/orders')
@login_required
def user_orders():
    user = User.find_by_id(session['user_id'])
    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.login'))
    
    orders = list(mongo.db.orders.find({'user_id': ObjectId(session['user_id'])}).sort('created_at', -1))
    
    return render_template('store/orders.html', user=user, orders=orders)