"""
WARNING:

Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
in order to get all the dependencies on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the dependencies.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at
https://documentation.botcity.dev/tutorials/python-automations/web/
"""


# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *
from webdriver_manager.chrome import ChromeDriverManager
from botcity.plugins.http import BotHttpPlugin
import pandas as pd
import mysql.connector

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def pegar_produto():
    http = BotHttpPlugin('http://127.0.0.1:5000/produto')
    retornoJson = http.get_as_json()

    # Acessa a lista de produtos
    produtos = retornoJson.get("dados", []) 

    print("Produtos sem o valor em dolar: \n")

    for item in produtos: 
        for chave, valor in item.items():
            if chave != "id":
                print(f"{chave}: {valor}") 
        print() 

    print("Produtos com o valor em dolar: \n")

    resultados = []

    # Obtém a cotação do dólar
    cotacao_dolar = calcular_preco_dolar()

    # Verifica se a cotação foi obtida corretamente
    if isinstance(cotacao_dolar, float):
        for item in produtos:
            preco_real = float(item.get("preco_real", 0))
            preco_dolar = preco_real * cotacao_dolar  # Calcula o preço em dólar

            # Atualiza o produto com o preço em dólar
            item["preco_dolar"] = preco_dolar

            resultados.append({
                "Descrição": item.get("descricao", ""),
                "Unidade": item.get("unidade", ""),
                "Quantidade": item.get("quantidade", 0),
                "Preço Real": preco_real,
                "Preço Dólar":  f"{preco_dolar:.2f}"  # Corrigido aqui para usar a variável preco_dolar
            })

            # Exibe as informações do produto
            for chave, valor in item.items():
                if chave != "id":
                    if isinstance(valor, (int, float)):
                        print(f"{chave}: {valor:.2f}") 
                    else:
                        print(f"{chave}: {valor}") 
            print()

            # Atualiza o valor no banco de dados
            atualizar_preco_dolar_no_banco(item["id"], preco_dolar)

        # Cria um arquivo Excel com os resultados
        df = pd.DataFrame(resultados)
        df.to_excel("produtos.xlsx", index=False)
    else:
        print("Erro ao obter a cotação do dólar.")


def calcular_preco_dolar():
    api_dolar = BotHttpPlugin('https://economia.awesomeapi.com.br/last/USD-BRL')
    retornoJson = api_dolar.get_as_json()

    if "USDBRL" in retornoJson:
        return float(retornoJson["USDBRL"]["high"])
    else:
        return None  # Retorna None se não conseguir obter o valor


def atualizar_preco_dolar_no_banco(produto_id, preco_dolar):
    # Conexão com o banco de dados (exemplo com MySQL)
    conexao = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='',
        database='banco'
    )

    cursor = conexao.cursor()

    # Query de atualização
    query = "UPDATE produto SET preco_dolar = %s WHERE id = %s"
    valores = (preco_dolar, produto_id)

    cursor.execute(query, valores)

    conexao.commit()  # Salva as alterações no banco de dados
    cursor.close()
    conexao.close()
    


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.CHROME

    # Uncomment to set the WebDriver path
    bot.driver_path =  ChromeDriverManager().install()

    # Opens the BotCity website.
    #bot.browse("https://www.botcity.dev")

    # Implement here your logic...
    pegar_produto()
 

    # Wait 3 seconds before closing
    bot.wait(3000)

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
