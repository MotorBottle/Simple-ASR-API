import requests

# 设置服务的 URL
url = "http://127.0.0.1:7869/asr"

# 准备音频文件路径
audio_path = "./requestSound.wav"

# 定义 hotwords
hotwords = "移到 挪到"

# 发送 POST 请求
with open(audio_path, "rb") as audio_file:
    response = requests.post(url, files={"audio": audio_file}, data={"hotwords": hotwords})

# 输出结果
if response.status_code == 200:
    try:
        print("Recognition Result:", response.json()["text"])
    except ValueError:
        print("Non-JSON response:", response.text)  # Print the raw response
else:
    print("Error:", response.text)  # Print the raw error message