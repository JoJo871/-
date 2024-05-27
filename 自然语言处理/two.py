import requests
import json

def send_message_to_ollama(prompt, port=11434):
    url = f"http://localhost:{port}/api/generate"
    payload = {
        "model": "llama2:latest",
        "prompt": prompt
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        response_content = ""
        for line in response.iter_lines():
            if line:
                response_content += json.loads(line)["response"]
        return response_content
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    background = "一家知名电子产品公司发布了一款新型智能手表，该手表配备了多项健康监测功能，包括心率监测、睡眠监测、运动追踪等，并且能够自动识别用户的活动状态和健康异常。"
    question = "你认为这款智能手表对用户的健康管理是否有重要意义？"

    prompt = f"{background} {question}"
    response = send_message_to_ollama(prompt)
    print("Ollama's response:")
    print(response)
