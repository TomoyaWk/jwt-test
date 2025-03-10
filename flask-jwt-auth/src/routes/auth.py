from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt,
    create_access_token
)
from src.models.user import User  # モジュールパスを修正
from src.utils.jwt_utils import verify_jwt, generate_tokens  # モジュールパスを修正

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 400

    new_user = User(username=username, password=password)
    new_user.save()

    return jsonify({"msg": "User created successfully", "user_id": new_user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.verify_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    # アクセストークンとリフレッシュトークンを生成
    access_token, refresh_token = generate_tokens(user.id)

    return jsonify({
        "msg": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username
        },
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # リフレッシュトークンが必要
def refresh():
    """
    リフレッシュトークンを使用して新しいアクセストークンを生成する
    """
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        "access_token": new_access_token
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    ログアウトエンドポイント - トークンを無効にする
    実際の実装ではブラックリストに追加するなどの処理が必要
    """
    jti = get_jwt()['jti']
    # ここでJTIをブラックリストに追加する処理を実装
    # 例: blacklist.add(jti)
    
    return jsonify({"msg": "Successfully logged out"}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    認証が必要なエンドポイントの例
    """
    current_user_id = get_jwt_identity()
    
    return jsonify({
        "msg": "Access to protected resource granted",
        "user_id": current_user_id
    }), 200