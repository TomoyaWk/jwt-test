from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.models.user import User
from src.utils.jwt_utils import token_required, admin_required  

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
    } for user in users]), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
    }), 200

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    現在ログインしているユーザーの情報を取得するエンドポイント
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    return jsonify({
        "id": user.id,
        "username": user.username,
        'password': user.password_hash
    }), 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    # 管理者またはユーザー自身のみ更新可能
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    
    if current_user_id != user_id and not is_admin:
        return jsonify({"msg": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    if 'username' in data:
        # ユーザー名の重複チェック
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"msg": "Username already exists"}), 400
        user.username = data['username']
    if 'password' in data:
        user.set_password(data['password'])
    
    user.save()
    return jsonify({"msg": "User updated successfully"}), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    # 管理者またはユーザー自身のみ削除可能
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    
    if current_user_id != user_id and not is_admin:
        return jsonify({"msg": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    user.delete()
    return jsonify({"msg": "User deleted successfully"}), 200

@users_bp.route('/admin', methods=['GET'])
@admin_required
def admin_users():
    """
    管理者専用のユーザー一覧取得エンドポイント
    より詳細な情報を含む
    """
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'created_at': user.created_at if hasattr(user, 'created_at') else None,
        'updated_at': user.updated_at if hasattr(user, 'updated_at') else None
    } for user in users]), 200

@users_bp.route('/check-token', methods=['GET'])
@token_required
def check_auth():
    """
    トークンの有効性を確認し、ユーザー情報を返すエンドポイント
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"valid": True, "authenticated": False, "msg": "User not found"}), 404
        
    return jsonify({
        "valid": True, 
        "authenticated": True,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }), 200
