import os
import json
from models import User
from collections import Counter

def export_json():
    try:
        # ユーザーの年齢データを取得
        ages = [user.age for user in User.select()]
        print("Exporting JSON with ages:", ages)  # デバッグ用

         # 年齢のカウントを取得
        age_counts = Counter(ages)
        print("Age counts:", age_counts)  # デバッグ用

        # 保存するデータ（辞書形式）
        data_to_export = dict(age_counts)
        print("Data to export:", data_to_export)  # デバッグ用

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
            json.dump(data_to_export, file, ensure_ascii=False, indent=4)
            print("JSON export successful!")  # デバッグ用
    except Exception as e:
        print("Error in export_json:", e)  # エラーをログに出力