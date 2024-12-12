import os
import json
from models import User

def export_json():
    try:
        # ユーザーの年齢データを取得
        ages = [user.age for user in User.select()]
        print("Exporting JSON with ages:", ages)  # デバッグ用

        # staticフォルダのパスを取得
        static_folder = os.path.join(os.path.dirname(__file__), '..', 'static')
        print("Static folder path:", static_folder)  # デバッグ用

        # JSONファイルの保存先
        file_path = os.path.join(static_folder, 'age.json')
        print("JSON file path:", file_path)  # デバッグ用

        # staticフォルダが存在しない場合は作成
        os.makedirs(static_folder, exist_ok=True)

        # JSONデータを書き出し
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(ages, file, ensure_ascii=False, indent=4)
            print("JSON export successful!")  # デバッグ用
    except Exception as e:
        print("Error in export_json:", e)  # エラーをログに出力