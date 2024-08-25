import boto3

# 建立 SNS 客戶端
sns_client = boto3.client('sns', region_name='us-east-1')  # 使用東京區域


# 發送簡訊
response = sns_client.publish(
    PhoneNumber='+886958883939',  # 替換成用戶的手機號碼
    Message='Your OTP code is 123456'  # 替換成你的 OTP 內容
)

# 打印回應
print(response)
