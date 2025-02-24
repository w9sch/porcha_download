
import tkinter as tk
import customtkinter as ctk
import requests
import json

def send_request():
    user_message = input_text.get("1.0", tk.END).strip()
    # selected_model = model_var.get()




    url = "https://www.blackbox.ai/api/chat"
    payload = json.dumps({
        "messages": [
            {
                "id": "12123",
                "content": user_message,
                "role": "user"
            }
        ],
        "agentMode": {},
        "id": "fwivmAv",
        "previewToken": None,
        "userId": None,
        "codeModelMode": True,
        "trendingAgentMode": {},
        "isMicMode": False,
        "userSystemPrompt": None,
        "maxTokens": 1024,
        "playgroundTopP": None,
        "playgroundTemperature": None, #случайность отвт
        "isChromeExt": False,
        "githubToken": "",
        "clickedAnswer2": False,
        "clickedAnswer3": False,
        "clickedForceWebSearch": False,
        "visitFromDelta": False,
        "isMemoryEnabled": False,
        "mobileClient": False,
        "userSelectedModel": None,
        "validated": "00f37b34-a166-4efb-bce5-1312d87f2f94",
        "imageGenerationMode": False,
        "webSearchModePrompt": False,
        "deepSearchMode": False,
        "domains": None,
        "vscodeClient": False,
        "codeInterpreterMode": False,
        "customProfile": {
            "name": "",
            "occupation": "",
            "traits": [],
            "additionalInfo": "",
            "enableNewChats": False
        },
        "session": None,
        "isPremium": True,
        "subscriptionCache": None,
        "beastMode": True
    })

    headers = {
        # 'accept': '*/*',
        # 'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://www.blackbox.ai',
        # 'priority': 'u=1, i',
        'referer': 'https://www.blackbox.ai/',
        # 'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-origin',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
        # 'x-kl-kfa-ajax-request': 'Ajax_Request',
        # 'Cookie': 'render_app_version_affinity=dep-cupbsbrtq21c739pub20; sessionId=9ea957ca-9076-4338-b390-5f67137f3000'
    }
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        try:
            response_data = response.json()
            if 'content' in response_data:
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, response_data['content'])
            else:
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, json.dumps(response_data, ensure_ascii=False, indent=4))
        except json.JSONDecodeError:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "\n" + response.text)
    else:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {response.status_code} - {response.text}")

root = ctk.CTk()
root.title("Chat API Interface")

input_label = ctk.CTkLabel(root, text="Введите сообщение:")
input_label.pack()

input_text = ctk.CTkTextbox(root, height=100, width=500)
input_text.pack()

# model_label = ctk.CTkLabel(root, text="Выберите модель:")
# model_label.pack()

# models = [
#     "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
#     "Qwen/QwQ-32B-Preview",
#     "databricks/dbrx-instruct",
#     "deepseek-ai/deepseek-llm-67b-chat",
#     "mistralai/Mistral-Small-24B-Instruct-2501",
#     "deepseek-ai/DeepSeek-R1",
#     "deepseek-ai/DeepSeek-V3"
# ]

# model_var = ctk.StringVar(value=models[0])
# model_menu = ctk.CTkComboBox(root, variable=model_var, values=models)
# model_menu.pack()

send_button = ctk.CTkButton(root, text="Отправить", command=send_request)
send_button.pack()

output_label = ctk.CTkLabel(root, text="Ответ:")
output_label.pack()

output_text = ctk.CTkTextbox(root, height=200, width=500)
output_text.pack()

root.mainloop()

