import requests
import json

class OllamaClient:
    def __init__(self, port=11434):
        self.port = port
        self.url = f"http://localhost:{port}/api/generate"
        self.model_name = "llama2:latest"

    def send_message_to_ollama(self, prompt):
        payload = {
            "model": self.model_name,
            "prompt": prompt
        }
        response = requests.post(self.url, json=payload)
        if response.status_code == 200:
            response_content = ""
            for line in response.iter_lines():
                if line:
                    response_content += json.loads(line)["response"]
            return response_content
        else:
            return f"Error: {response.status_code} - {response.text}"

    def chat(self, prompts):
        """
        与Ollama模型进行对话。

        Args:
        - prompts (list of str): 用户输入的文本列表

        Returns:
        - list of str: 模型生成的回复列表
        """
        responses = []
        for prompt in prompts:
            response = self.send_message_to_ollama(prompt)
            responses.append(response)
        return responses

# 使用示例
if __name__ == "__main__":
    ollama_client = OllamaClient()
    background = "一家知名电子产品公司发布了一款新型智能手表，该手表配备了多项健康监测功能，包括心率监测、睡眠监测、运动追踪等，并且能够自动识别用户的活动状态和健康异常。"
    question = "你认为这款智能手表对用户的健康管理是否有重要意义？"

    prompts = f"{background} {question}"
    responses = ollama_client.chat(prompts)
    for i, response in enumerate(responses):
        print(f"Prompt {i+1}: {prompts[i]}")
        print(f"Response {i+1}: {response}\n")