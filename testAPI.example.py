import requests
import time

# 设置服务的 URL
url = "http://localhost:7869/asr"

# 准备音频文件路径
audio_path = "./requestSound.wav"

# 定义 hotwords
hotwords = "移到 挪到"

# 记录开始时间
start_time = time.time()

# 发送 POST 请求
with open(audio_path, "rb") as audio_file:
    response = requests.post(url, files={"audio": audio_file}, data={"hotwords": hotwords})

# 计算耗时
end_time = time.time()
time_consumed = end_time - start_time

# 输出结果
if response.status_code == 200:
    try:
        print("Recognition Result:", response.json()["text"])
        print(f"Time consumed: {time_consumed:.3f} seconds")
    except ValueError:
        print("Non-JSON response:", response.text)  # Print the raw response
        print(f"Time consumed: {time_consumed:.3f} seconds")
else:
    print("Error:", response.text)  # Print the raw error message
    print(f"Time consumed: {time_consumed:.3f} seconds")
