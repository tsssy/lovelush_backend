# test_user_management.py
import requests
import json
import time

base_url = "http://8.216.32.239:27017"

# 等待 Flask 应用启动，确保 /create_new_male_user 路由可用
time.sleep(3)

# --- 测试 POST 请求 (创建新男性用户) ---
print("--- 测试 POST 请求 (创建新男性用户) ---")
new_user_data = {
    "telegram_id": "telegram_user_123",
    "mode": "friends"
}
headers = {'Content-Type': 'application/json'}
response_new_user = requests.post(f"{base_url}/create_new_male_user", data=json.dumps(new_user_data), headers=headers)
print(f"POST 新用户响应状态码: {response_new_user.status_code}")
print(f"POST 新用户响应内容: {response_new_user.json()}")
print("-" * 30)

# --- 测试 POST 请求 (创建新男性用户 - 缺少 telegram_id) ---
print("--- 测试 POST 请求 (创建新男性用户 - 缺少 telegram_id) ---")
new_user_data_no_id = {
    "mode": "friends"
}
response_no_id = requests.post(f"{base_url}/create_new_male_user", data=json.dumps(new_user_data_no_id), headers=headers)
print(f"POST 无ID响应状态码: {response_no_id.status_code}")
if response_no_id.status_code == 200:
    print(f"POST 无ID响应内容: {response_no_id.json()}")
else:
    print(f"POST 无ID响应内容 (非 200): {response_no_id.text}")
print("-" * 30)

# --- 测试 POST 请求 (创建新男性用户 - 无效 mode) ---
print("--- 测试 POST 请求 (创建新男性用户 - 无效 mode) ---")
new_user_data_bad_mode = {
    "telegram_id": "telegram_user_456",
    "mode": "invalid_mode"
}
response_bad_mode = requests.post(f"{base_url}/create_new_male_user", data=json.dumps(new_user_data_bad_mode), headers=headers)
print(f"POST 无效模式响应状态码: {response_bad_mode.status_code}")
if response_bad_mode.status_code == 200:
    print(f"POST 无效模式响应内容: {response_bad_mode.json()}")
else:
    print(f"POST 无效模式响应内容 (非 200): {response_bad_mode.text}")
print("-" * 30) 