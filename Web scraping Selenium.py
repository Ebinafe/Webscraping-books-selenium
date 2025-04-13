from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3

service=Service()
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # executa sem abrir a janela do navegador
options.add_argument('--disable-gpu')

nav = webdriver.Chrome(service=service, options=options)
nav.get('https://books.toscrape.com/')
nav.maximize_window()

#criação das listas
titlelist = []
stocklist = []

WebDriverWait(nav, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article.product_pod h3 a')))
books = nav.find_elements(By.CSS_SELECTOR, 'article.product_pod h3 a')

for i in range(len(books)):
    # busca direta pelo título completo do livro
    books = nav.find_elements(By.CSS_SELECTOR, 'article.product_pod h3 a')
    book = books[i]
    title = book.get_attribute('title')
    book.click()

    try:
        stock = WebDriverWait(nav, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'p.instock.availability'))
        )
        stock_text = stock.text.strip()
    except:
        stock_text = 'Not found'

    titlelist.append(title)
    stocklist.append(stock_text)

    nav.back()
    time.sleep(5)

#para gerar uma lista enumerada de forma organizada
for i, (title, stock) in enumerate(zip(titlelist,stocklist), 1):
    print(f"{i:02d}. {title} - {stock}")

conn = sqlite3.connect("livros.db")  # Cria o arquivo do banco se não existir
cursor = conn.cursor()

# Criação da tabela (se não existir)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        estoque TEXT
    )
''')

# Inserção dos dados
for titulo, estoque in zip(titlelist, stocklist):
    cursor.execute('INSERT INTO livros (titulo, estoque) VALUES (?, ?)', (titulo, estoque))

conn.commit()
conn.close()

print("Dados salvos em livros.db com sucesso.")