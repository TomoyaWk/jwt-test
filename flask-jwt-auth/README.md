# Flask JWT Authentication Sample App

(Copilotへの指示を元に作成、一部手を加えて調整)
このプロジェクトは、Python、Flask、SQLAlchemyを使用したJWT認証のサンプルアプリケーションです。SQLiteデータベースを使用し、ユーザー名とパスワードの登録、認証、JWTトークンの返却、トークンの有効期限管理を行います。また、Dockerを使用してアプリケーションを動作させることができます。

## 構成

- `src/app.py`: アプリケーションのエントリーポイント。Flaskアプリを初期化し、データベース接続を設定し、ルートを登録します。
- `src/config.py`: Flaskアプリケーションの設定を含むファイル。データベースURIやJWTシークレットキーを設定します。
- `src/models/user.py`: `User`モデルを定義し、ユーザーの作成やクエリを行うメソッドを含みます。
- `src/routes/auth.py`: ユーザー登録やログインを含む認証ルートを定義します。JWTトークンの生成と検証を処理します。
- `src/utils/jwt_utils.py`: JWTトークンの生成と検証のためのユーティリティ関数を含むファイル。
- `tests/test_auth.py`: 認証ルートのユニットテストを含むファイル。

## プロジェクト構成

```
flask-jwt-auth
├── src
│   ├── app.py
│   ├── config.py
│   ├── models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── auth.py
│   └── utils
│       ├── __init__.py
│       └── jwt_utils.py
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   └── test_auth.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## セットアップ

1. リポジトリをクローンします。
   ```bash
   git clone <repository-url>
   cd flask-jwt-auth
   ```

2. 必要なパッケージをインストールします。
   ```bash
   pip install -r requirements.txt
   ```

3. 環境変数を設定します。`.env.example`をコピーして`.env`を作成し、必要な値を設定します。

4. アプリケーションを実行します。
   ```bash
   python src/app.py
   ```

## Dockerでの実行

1. Dockerイメージをビルドします。
   ```bash
   docker-compose build
   ```

2. アプリケーションを起動します。
   ```bash
   docker-compose up
   ```

## 使用例

- ユーザー登録: `POST /auth/register`
- ユーザーログイン: `POST /auth/login`
- JWTトークンを使用して保護されたリソースにアクセスします。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。