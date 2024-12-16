import requests

# Parâmetros
bot_id = "67532c2ffdc1d12fb3d990ba"
user_id = "19785416860"  # ou o número correto
token = "TAZRdawS0kXiagTVrbbk0FnQvCBxMs8Rx2tMfgVlYeOnYBwyh1RVCkNCHhr4dFul"
block_name = "Flow"

# URL
url = f"https://api.chatfuel.com/bots/{bot_id}/users/me/send"

# Dados enviados como query string
params = {
    "chatfuel_token": token,
    "chatfuel_block_name": block_name,
    "first_name": "gustavo",
    "phone": "19997007539",
    "value": 200,
    "dueDate": "2024-11-27",
    "bankSlipUrl": "skkssk"
}

# Fazer a requisição GET
response = requests.get(url, params=params)

# Exibir o resultado
print("Status Code:", response.status_code)
print("Response Text:", response.text)