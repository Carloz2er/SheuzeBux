from flask import session, redirect, url_for, flash, current_app
from functools import wraps
from models import User
from bson import ObjectId
import jwt
import datetime

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Acesso negado. Faça login como administrador.', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.find_by_id(session['user_id'])
        if not user:
            flash('Usuário não encontrado.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Verificar se o usuário tem role de admin
        if user.get('role') not in ['admin', 'super_admin']:
            flash('Acesso negado. Permissões insuficientes.', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Acesso negado.', 'danger')
                return redirect(url_for('auth.login'))
            
            user = User.find_by_id(session['user_id'])
            if not user:
                flash('Usuário não encontrado.', 'danger')
                return redirect(url_for('auth.login'))
            
            # Super admin tem acesso a tudo
            if user.get('role') == 'super_admin':
                return f(*args, **kwargs)
            
            # Admin precisa ter a permissão específica
            if user.get('role') == 'admin':
                user_permissions = user.get('permissions', [])
                if permission in user_permissions:
                    return f(*args, **kwargs)
            
            flash('Permissões insuficientes para esta ação.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return decorated_function
    return decorator

def generate_token(user_id):
    payload = {
        'user_id': str(user_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None