# -# 项目介绍
    本项目是用于远程部署文言一心大模型与本地部署ollama大模型
 
# 环境依赖
 import requests
 import json
 
# 目录结构描述
    ├── ReadMe.md           // 帮助文档
    
    ├── one.py,twe.py,three.py,four.py    // 对本地部署ollama以及对之前本地部署chatglm的尝试
    
    ├── open.py             // 远程部署文言一心
 
# 使用说明
（逐行解释）
 open.py:
     # 定义一个函数 ask_Q，它接受一个参数 question，表示要询问的问题  
    def ask_Q(question):  
        # 创建一个URL字符串，用于与百度API进行通信。注意，这里假设 get_access_token() 函数能够正确返回access_token  
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()  
      
        # 创建一个JSON格式的payload，包含用户要询问的问题  
        payload = json.dumps({  
            "messages": [  
                {  
                    "role": "user",  # 表明这是一个用户角色发送的消息  
                    "content": question  # 消息的内容，即用户的问题  
                }  
            ]  
        })  
      
        # 设置HTTP请求的headers，指明发送的数据类型为JSON  
        headers = {  
            'Content-Type': 'application/json'  
        }  
      
        # 使用requests库发送POST请求到指定的URL，并带上headers和payload  
        response = requests.request("POST", url, headers=headers, data=payload)  
      
        # 从响应中解析JSON数据并返回  
        return response.json()  
      
      
    # 定义一个函数 get_access_token，它用于获取百度API的访问令牌（access_token）  
    def get_access_token():  
        """  
        使用 AK（App Key），SK（Secret Key）生成鉴权签名（Access Token）  
        :return: access_token，或是None(如果错误)  
        """  
        # 百度API的URL，用于获取access_token  
        url = "https://aip.baidubce.com/oauth/2.0/token"  
      
        # 准备参数，包括grant_type、client_id（API_KEY）和client_secret（SECRET_KEY）。注意这里假设了API_KEY和SECRET_KEY是全局变量  
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}  
      
        # 发送请求并获取响应，然后从响应的JSON数据中提取access_token并返回。注意这里假设了响应中一定包含access_token  
        return str(requests.post(url, params=params).json().get("access_token"))  
      
      
    # 定义一个列表 questions，包含要询问的问题  
    questions = [  
        "一家知名电子产品公司发布了一款新型智能手表，该手表配备了多项健康监测功能，包括心率监测、睡眠监测、运动追踪等，并且能够自动识别用户的活动状态和健康异常。",  
        "你认为这款智能手表对用户的健康管理是否有重要意义？"  
        # 在这里添加更多问题  
    ]  
      
    # 定义一个空列表 answers，用于存储每个问题的回答  
    answers = []  
      
    # 遍历 questions 列表中的每个问题  
    for question in questions:  
        # 调用 ask_Q 函数询问问题，并将返回的结果（包含答案的JSON数据）存储在 answer 变量中  
        answer = ask_Q(question)  
      
        # 从 answer 中提取 'result' 字段（这里假设它是答案的内容）并添加到 answers 列表中  
        answers.append(answer['result'])  
      
    # 输出每个问题及其对应的答案  
    for question, answer in zip(questions, answers):  
        print("问题:", question)  
        print("答案:", answer)  
        print()
 three.py:
 # 定义一个名为OllamaClient的类，该类表示与Ollama API交互的客户端。  
class OllamaClient:  
      
        # 初始化方法，设置默认的端口和URL，以及模型名称。  
        def __init__(self, port=11434):  
            self.port = port  # 设置端口  
            self.url = f"http://localhost:{port}/api/generate"  # 根据端口生成URL  
            self.model_name = "llama2:latest"  # 设置模型名称为"llama2:latest"  
      
        # 定义一个方法send_message_to_ollama，用于向Ollama发送消息并获取响应。  
        def send_message_to_ollama(self, prompt):  
            # 构造payload，包括模型名称和要发送的提示。  
            payload = {  
                "model": self.model_name,  
                "prompt": prompt  
            }  
            # 发送POST请求到之前定义的URL，并带上payload。  
            response = requests.post(self.url, json=payload)  
      
            # 如果响应状态码为200，说明请求成功。  
            if response.status_code == 200:  
                response_content = ""  # 初始化响应内容为空字符串  
                # 遍历响应的每一行（因为可能是一个流式响应）。  
                for line in response.iter_lines():  
                    if line:  # 如果该行不为空  
                        # 加载该行内容为JSON并获取其中的"response"字段。  
                        response_content += json.loads(line)["response"]  
                # 返回完整的响应内容。  
                return response_content  
            else:  
                # 如果响应状态码不是200，返回错误信息。  
                return f"Error: {response.status_code} - {response.text}"  
      
        # 定义一个方法chat，该方法接受一个提示列表，并返回模型生成的回复列表。  
        def chat(self, prompts):  
            """  
            与Ollama模型进行对话。  
      
            Args:  
            - prompts (list of str): 用户输入的文本列表  
      
            Returns:  
            - list of str: 模型生成的回复列表  
            """  
            responses = []  # 初始化回复列表为空列表  
            # 遍历每个提示  
            for prompt in prompts:  
                # 发送消息并获取响应  
                response = self.send_message_to_ollama(prompt)  
                # 将响应添加到回复列表中  
                responses.append(response)  
            # 返回回复列表  
            return responses  
      
    # 使用示例  
    if __name__ == "__main__":  
        # 创建一个OllamaClient实例  
        ollama_client = OllamaClient()  
          
        # 设置背景信息和问题  
        background = "一家知名电子产品公司发布了一款新型智能手表，该手表配备了多项健康监测功能，包括心率监测、睡眠监测、运动追踪等，并且能够自动识别用户的活动状态和健康异常。"  
        question = "你认为这款智能手表对用户的健康管理是否有重要意义？"  
      
        # 将背景信息和问题合并为一个提示字符串  
        prompts = f"{background} {question}"  
      
        # 与模型对话，并获取回复  
        responses = ollama_client.chat([prompts])  # 注意这里需要将prompts放在一个列表中，因为chat方法接受的是列表  
      
        # 遍历并打印每个提示和对应的回复  
        for i, response in enumerate(responses):  
            print(f"Prompt {i+1}: {prompts}")  # 这里有误，prompts应该只有一个元素，所以这里总是打印整个prompts  
            print(f"Response {i+1}: {response}\n")
 
 
# 版本内容更新
###### v1.0.0: 
 
 
