import os

def rename_images(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                # 獲取完整路徑
                old_file_path = os.path.join(root, filename)
                # 獲取目錄名稱
                dir_name = os.path.basename(root)
                # 替換空格和特殊符號
                formatted_dir_name = dir_name.replace(' ', '-').replace('/', '-')
                # 構造新的檔案名稱
                file_extension = os.path.splitext(filename)[1]
                new_filename = f"{formatted_dir_name}{file_extension}"
                counter = 1
                # 確保新檔名不重複
                while os.path.exists(os.path.join(root, new_filename)):
                    new_filename = f"{formatted_dir_name}{counter:02d}{file_extension}"
                    counter += 1
                new_file_path = os.path.join(root, new_filename)
                # 重新命名檔案
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} to {new_file_path}")

# 設定基礎資料夾路徑
base_directory = '/Users/guobaichen/Desktop/商品'
rename_images(base_directory)