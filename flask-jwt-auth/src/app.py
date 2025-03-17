import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.models import db
from src.config import Config

def create_app(config_name=None):
    app = Flask(__name__)
    
    # CORSの設定を追加
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # データベースディレクトリを確保
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config.from_object(Config)
        # インスタンスディレクトリを作成
        instance_path = os.path.join(os.path.dirname(__file__), '..', 'instance')
        os.makedirs(instance_path, exist_ok=True)
        os.chmod(instance_path, 0o777)  # 権限を設定
        
        # データベースファイルパスを設定
        db_path = os.path.join(instance_path, 'app.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    db.init_app(app)
    jwt = JWTManager(app)
    
    from src.routes.auth import auth_bp
    from src.routes.users import users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')