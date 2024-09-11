import sqlite3
import requests

def get_github_user_info(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        print(f"Erro ao acessar a API do GitHub: {response.status_code}")
        return None

def save_user_info_to_db(user_info):
    conn = sqlite3.connect('github_infoUsers.db')

    # Crie um cursor para executar comandos SQL
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                name TEXT,
                location TEXT,
                bio TEXT
                )''')

    try:
        c.execute('''INSERT INTO users (username, name, location, bio) VALUES (?, ?, ?, ?)''',
                  (user_info['login'], user_info['name'], user_info['location'], user_info['bio']))
    except sqlite3.IntegrityError:
        print(f"Usuário '{user_info['login']}' já existe no banco de dados.")
    else:
        # Salva as alterações no banco
        conn.commit()

    # Fecha a conexão com o banco de dados
    conn.close()

while True:
    username = input("Digite o nome de usuário do GitHub (ou 0 para encerrar o programa): ")

    if username == '0':
        print('Fim do programa!!')
        break

    user_info = get_github_user_info(username)

    if user_info:
        print("Informações do usuário:")
        print(f"Nome: {user_info['name']}")
        print(f"Localização: {user_info['location']}")
        print(f"Bio: {user_info['bio']}")

        save_user_info_to_db(user_info)
        print("Informações do usuário salvas com sucesso no banco de dados.")

    else:
        print("Usuário não encontrado ou erro ao acessar a API do GitHub.")
