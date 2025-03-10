#!/bin/sh
set -e

# instanceディレクトリが存在することを確認
mkdir -p /app/instance
chmod 777 /app/instance

# データベースファイルが存在する場合、適切な権限を設定
if [ -f /app/instance/app.db ]; then
    chmod 666 /app/instance/app.db
fi

# アプリケーションを起動
exec python3 src/app.py
