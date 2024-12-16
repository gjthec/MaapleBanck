import requests
from datetime import datetime, timedelta
import schedule
import time


# Configurações da API do Asaas
ASAAS_API = 'https://sandbox.asaas.com/api/v3/payments'
ASAAS_TOKEN = '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwODgwMzY6OiRhYWNoX2ExMGM1ZjQyLTVmMTctNDNlOS04NzU5LTgxM2Q5YzM5YzIxMg=='  # Substitua pela sua chave da API


def send_to_chatfuel(phone, name, value, due_date, payment_link):
    """
    Envia informações para o Chatfuel via API.

    Args:
        phone (str): Número de telefone do cliente (usado como identificador no Chatfuel).
        name (str): Nome do cliente.
        value (float): Valor do boleto.
        due_date (str): Data de vencimento do boleto.
        payment_link (str): Link para pagamento.
    """
    # Configurações da API do Chatfuel
    CHATFUEL_API_URL = "https://api.chatfuel.com/bots/67532c2ffdc1d12fb3d990ba/users/9785416860/send"

    CHATFUEL_TOKEN = "TAZRdawS0kXiagTVrbbk0FnQvCBxMs8Rx2tMfgVlYeOnYBwyh1RVCkNCHhr4dFul"
    BLOCK_NAME = "Coletar_informações"

    payload = {
        "chatfuel_token": CHATFUEL_TOKEN,
        "chatfuel_user_id": phone,  # Pode ser o número do cliente
        "block_name": BLOCK_NAME,
        "first_name": name,
        "value": value,
        "dueDate": due_date,
        "bankSlipUrl": payment_link
    }

    try:
        print(f"[INFO] Enviando dados para o Chatfuel: {name} ({phone})...")
        response = requests.post(CHATFUEL_API_URL, json=payload)
        response.raise_for_status()
        print(f"[SUCCESS] Dados enviados com sucesso para {name} ({phone})")
    except Exception as e:
        print(f"[ERROR] Erro ao enviar dados para o Chatfuel: {e}")


# Função para testar a conexão com a API do Asaas
def test_connection():
    try:
        print("Testando conexão com a API do Asaas...")
        response = requests.get(ASAAS_API, headers={
            'access_token': f'{ASAAS_TOKEN}',
            'Content-Type': 'application/json',
            'User-Agent' : 'teste_gjtechsolucions'
        })

        if response.status_code == 200:
            print("Conexão com a API do Asaas bem-sucedida!")
        else:
            print(f"Erro ao conectar com a API do Asaas. Código HTTP: {response.status_code}")
            print("Verifique sua chave de API ou a URL.")
            exit()  # Finaliza o script se não houver conexão
    except Exception as e:
        print(f"Erro ao tentar conectar com a API do Asaas: {e}")
        exit()

def calculate_days_to_due(due_date):
    """
    Calcula os dias restantes até a data de vencimento do boleto.

    Args:
        due_date (str): Data de vencimento no formato 'YYYY-MM-DD'.

    Returns:
        int: Número de dias restantes (pode ser negativo se já estiver vencido).
    """
    try:
        today = datetime.now().date()
        due_date_obj = datetime.strptime(due_date, '%Y-%m-%d').date()
        days_to_due = (due_date_obj - today).days
        return days_to_due
    except Exception as e:
        print(f"Erro ao calcular dias para o vencimento: {e}")
        return None

# Função para buscar boletos pendentes no Asaas
def fetch_boletos():
    try:
        print("Buscando_boletos")
        response = requests.get(ASAAS_API, headers={
            'access_token': f'{ASAAS_TOKEN}',
            'Content-Type': 'application/json',
            'User-Agent': 'teste_gjtechsolucions'
        })

        response.raise_for_status()
        boletos = response.json()['data']

        if not boletos:
            print("Nenhum boleto pendente encontrado.")
            return []

        print(f"Encontrados {len(boletos)} boletos pendentes:")
        for boleto in boletos:
            days_to_due = calculate_days_to_due(boleto['dueDate'])
            customer_id = boleto.get("customer")

            # Pega informações do cliente
            customer_response = requests.get(f"{ASAAS_API}/customers/{customer_id}", headers={
                'access_token': f'{ASAAS_TOKEN}',
                'Content-Type': 'application/json',
                'User-Agent': 'teste_gjtechsolucions'
            })
            customer_response.raise_for_status()
            customer = customer_response.json()

            # Dados do cliente e boleto
            name = customer.get("name", "N/A")
            phone = customer.get("phone", "N/A")
            value = boleto['value']
            due_date = boleto['dueDate']
            payment_link = boleto['bankSlipUrl']

            # Envia ao Chatfuel
            send_to_chatfuel(phone, name, value, due_date, payment_link)

        return boletos

    except Exception as e:
        print(f"[ERROR] Erro ao buscar boletos: {e}")
        return []




def check_and_notify():
    print(f"\n--- Verificação iniciada em {datetime.now()} ---")
    boletos = fetch_boletos()
    print("Processo concluído.\n")



schedule.every().day.at("15:16").do(check_and_notify) # <---------------------------------------------Alterar o horario senao o programa nao vai disparar


test_connection()
if __name__ == "__main__":
    # Enviar dados de teste para o Chatfuel
    send_to_chatfuel(
        phone="19997007539",
        name="Gustavo",
        value="200",
        due_date="2024-11-27",
        payment_link="skkssk"
    )

# Loop para manter o script rodando
print("Agendador configurado. O script rodará todos os dias às 9h.")
while True:
    schedule.run_pending()
    time.sleep(1)

