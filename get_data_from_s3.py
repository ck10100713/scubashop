import boto3
import os

# 初始化 S3 客戶端
s3 = boto3.client('s3')

# 設定 S3 bucket 名稱和本地下載目錄
bucket_name = 'scubashopbucket'
local_download_dir = '/Users/guobaichen/Documents/MyProgram/scubashop/test'

def download_s3_folder(bucket_name, s3_folder, local_dir):
    print('step1')
    # 列出 S3 資料夾中的所有物件
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_folder)
    
    print('step2')
    print(objects)
    for obj in objects.get('Contents', []):
        # 獲取 S3 物件的 key
        s3_key = obj['Key']
        
        # 計算本地文件路徑
        local_file_path = os.path.join(local_dir, os.path.relpath(s3_key, s3_folder))
        
        # 創建本地目錄（如果不存在）
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        
        # 下載 S3 物件到本地文件
        s3.download_file(bucket_name, s3_key, local_file_path)
        print(f'Downloaded {s3_key} to {local_file_path}')

# 設定要下載的 S3 資料夾
s3_folder = 'media/'

# 下載 S3 資料夾到本地
download_s3_folder(bucket_name, s3_folder, local_download_dir)