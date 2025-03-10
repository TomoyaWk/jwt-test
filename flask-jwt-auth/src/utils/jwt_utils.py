from flask_jwt_extended import (
    decode_token, verify_jwt_in_request, 
    create_access_token, create_refresh_token, 
    get_jwt_identity, get_jwt
)
from flask import jsonify, current_app
from datetime import datetime, timezone, timedelta
from functools import wraps

def generate_tokens(user_id):
    """
    ユーザーIDに基づいてアクセストークンとリフレッシュトークンを生成する
    
    Args:
        user_id (int): ユーザーID
        
    Returns:
        tuple: (access_token, refresh_token)
    """
    # アクセストークンには最小限の情報だけを含める
    access_token = create_access_token(
        identity=user_id,
        fresh=True,
        expires_delta=timedelta(minutes=15)  # 短い有効期限
    )
    
    # リフレッシュトークンはより長い有効期限を持つ
    refresh_token = create_refresh_token(
        identity=user_id,
        expires_delta=timedelta(days=30)  # 30日間有効
    )
    
    return access_token, refresh_token

def verify_jwt():
    """
    JWTトークンを検証するユーティリティ関数
    
    Returns:
        bool: トークンが有効な場合はTrue
    """
    try:
        verify_jwt_in_request()
        return True
    except Exception:
        return False

def get_token_data(token):
    """
    JWTトークンをデコードしてデータを取得する
    
    Args:
        token (str): JWTトークン
        
    Returns:
        dict: トークンに含まれるデータ
    """
    try:
        return decode_token(token)
    except Exception:
        return None

def token_required(f):
    """
    JWTトークンを必要とするエンドポイント用のデコレータ
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not verify_jwt():
            return jsonify({"msg": "Missing or invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """
    管理者権限を必要とするエンドポイント用のデコレータ
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not verify_jwt():
            return jsonify({"msg": "Missing or invalid token"}), 401
        
        # 現在のJWTからclaims(追加情報)を取得
        claims = get_jwt()
        if not claims.get('is_admin', False):  # adminフラグをチェック
            return jsonify({"msg": "Admin privilege required"}), 403
            
        return f(*args, **kwargs)
    return decorated

def is_token_blacklisted(jti):
    """
    トークンがブラックリストに登録されているかチェック
    実際の実装ではデータベースやRedisなどを使用する
    
    Args:
        jti (str): JWT ID
        
    Returns:
        bool: ブラックリストに含まれている場合はTrue
    """
    # 実際には、データベースやRedisを使ってJTIをチェックする
    # この例では簡易的な実装
    return False
