import requests

# Parâmetros
bot_id = ""
user_id = ""  # ou o número correto
token = ""
block_name = ""

# URL
url = f"https://api.chatfuel.com/bots/{bot_id}/users/me/send"

# Dados enviados como query string
params = {
    "chatfuel_token": token,
    "chatfuel_block_name": block_name,
    "first_name": "gustavo",
    "phone": "",
    "value": 200,
    "dueDate": "2024-11-27",
    "bankSlipUrl": "skkssk"
}

# Fazer a requisição GET
response = requests.get(url, params=params)

# Exibir o resultado
print("Status Code:", response.status_code)
print("Response Text:", response.text)
