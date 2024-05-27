import requests
import json


class OllamaClient:
    def __init__(self, port=11434):
        self.port = port
        self.base_url = f"http://localhost:{port}/api/generate"

    def send_message(self, model, prompt):
        payload = {
            "model": model,
            "prompt": prompt
        }
        response = requests.post(self.base_url, json=payload)

        if response.status_code == 200:
            response_content = ""
            for line in response.iter_lines():
                if line:
                    response_content += json.loads(line)["response"]
            return response_content
        else:
            return f"Error: {response.status_code} - {response.text}"


class QuestionAnswerPrompt:
    def __init__(self, background, question):
        self.background = background
        self.question = question

    def generate_prompt(self):
        # 根据实际情况调整prompt的格式
        prompt = f"Background: {self.background}\nQuestion: {self.question}\nAnswer:"
        return prompt

    # 使用示例


if __name__ == "__main__":
    ollama_client = OllamaClient()
    prompt_obj = QuestionAnswerPrompt(
        background="Ollama is a powerful language model. It can answer questions and generate text.",
        question="What are the main uses of Ollama?"
    )
    prompt = prompt_obj.generate_prompt()

    # 发送请求到Ollama API
    response_content = ollama_client.send_message("llama2:latest", prompt)
    print(response_content)