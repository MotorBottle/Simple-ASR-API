import requests

# 设置服务的 URL
url = "http://192.168.50.18:17869/asr"

# 准备音频文件路径
audio_path = "./requestSound.wav"

# 发送 POST 请求
with open(audio_path, "rb") as audio_file:
    response = requests.post(url, files={"audio": audio_file})

# 输出结果
if response.status_code == 200:
    print("Recognition Result:", response.json()["text"])
else:
    print("Error:", response.json())