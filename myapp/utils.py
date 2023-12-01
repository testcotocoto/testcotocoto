# utils.py

import requests

def send_request_to_api(data):
    # APIエンドポイントとAPIキーを設定
    API_ENDPOINT = 'https://example.com/api/endpoint'
    API_KEY = 'your_api_key'

    # APIにリクエストを送信
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.post(API_ENDPOINT, json=data, headers=headers)

    # レスポンスを返す
    return response
