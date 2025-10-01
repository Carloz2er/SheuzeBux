from datetime import datetime, timedelta
from bson import ObjectId
import bcrypt
from flask_pymongo import PyMongo

mongo = PyMongo()

class User:
    @staticmethod
    def create_user(username, email, password, role='user', permissions=None, created_by=None):
        # Converter a senha para bytes antes de fazer hash
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        
        user_data = {
            'username': username,
            'email': email,
            'password': hashed,
            'role': role,
            'balance': 0.0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True,
            'permissions': permissions or [],
            'created_by': ObjectId(created_by) if created_by else None
        }
        
        return mongo.db.users.insert_one(user_data)
    
    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({'email': email})
    
    @staticmethod
    def find_by_id(user_id):
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        return mongo.db.users.find_one({'_id': user_id})
    
    @staticmethod
    def verify_password(user, password):
        if not user or 'password' not in user:
            return False
        
        # Converter ambos para bytes
        stored_password = user['password']
        input_password = password.encode('utf-8')
        
        # Se a senha armazenada é string, converter para bytes
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')
        
        return bcrypt.checkpw(input_password, stored_password)
    
    @staticmethod
    def update_user(user_id, update_data):
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        
        # Se estiver atualizando a senha, fazer hash
        if 'password' in update_data:
            password_bytes = update_data['password'].encode('utf-8')
            update_data['password'] = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        
        update_data['updated_at'] = datetime.utcnow()
        return mongo.db.users.update_one({'_id': user_id}, {'$set': update_data})
    
    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({'email': email})
    
    @staticmethod
    def find_by_id(user_id):
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        return mongo.db.users.find_one({'_id': user_id})
    
    @staticmethod
    def verify_password(user, password):
        if not user or 'password' not in user:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user['password'])
    
    @staticmethod
    def update_user(user_id, update_data):
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        
        update_data['updated_at'] = datetime.utcnow()
        return mongo.db.users.update_one({'_id': user_id}, {'$set': update_data})

class Product:
    @staticmethod
    def create_product(data, created_by):
        product = {
            'name': data['name'],
            'description': data['description'],
            'price': float(data['price']),
            'original_price': float(data.get('original_price', data['price'])),
            'category': data['category'],
            'type': data['type'],  # digital, physical, gift_card
            'stock': int(data['stock']),
            'images': data.get('images', []),
            'tags': data.get('tags', []),
            'is_active': True,
            'created_by': ObjectId(created_by),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'metadata': data.get('metadata', {})
        }
        
        return mongo.db.products.insert_one(product)

class Order:
    @staticmethod
    def create_order(order_data):
        order = {
            'user_id': ObjectId(order_data['user_id']),
            'items': order_data['items'],
            'total': order_data['total'],
            'status': 'pending',
            'payment_method': order_data.get('payment_method', 'paymenter'),
            'paymenter_invoice_id': order_data.get('paymenter_invoice_id'),
            'coupon_code': order_data.get('coupon_code'),
            'discount_amount': order_data.get('discount_amount', 0),
            'final_total': order_data.get('final_total', order_data['total']),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        return mongo.db.orders.insert_one(order)

class Coupon:
    @staticmethod
    def create_coupon(data, created_by):
        coupon = {
            'code': data['code'].upper(),
            'discount_type': data['discount_type'],
            'discount_value': float(data['discount_value']),
            'min_order_value': float(data.get('min_order_value', 0)),
            'max_discount': float(data.get('max_discount', 0)),
            'usage_limit': int(data.get('usage_limit', 0)),
            'used_count': 0,
            'valid_from': datetime.strptime(data['valid_from'], '%Y-%m-%d'),
            'valid_until': datetime.strptime(data['valid_until'], '%Y-%m-%d'),
            'is_active': True,
            'created_by': ObjectId(created_by),
            'created_at': datetime.utcnow(),
            'applicable_categories': data.get('applicable_categories', []),
            'applicable_products': data.get('applicable_products', [])
        }
        
        return mongo.db.coupons.insert_one(coupon)

class Advertisement:
    @staticmethod
    def create_ad(data, created_by):
        ad = {
            'title': data['title'],
            'description': data['description'],
            'image_url': data['image_url'],
            'target_url': data['target_url'],
            'position': data['position'],
            'is_active': True,
            'start_date': datetime.strptime(data['start_date'], '%Y-%m-%d'),
            'end_date': datetime.strptime(data['end_date'], '%Y-%m-%d'),
            'clicks': 0,
            'impressions': 0,
            'created_by': ObjectId(created_by),
            'created_at': datetime.utcnow()
        }
        
        return mongo.db.advertisements.insert_one(ad)