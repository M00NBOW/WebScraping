from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
import time
import json

def configure_chrome_driver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options = chrome_options)
    return driver

class Devedor:
    id = 0
    cpf_cnpj = ""
    valorDividaTotal = ""
    nome = ""

chrome = webdriver.Chrome()
chrome.get("https://www.listadevedores.pgfn.gov.br/")

elem = chrome.find_element_by_id("ufInput")
elem.send_keys("São Paulo")

time.sleep(5)

elem = chrome.find_element_by_id("municipioInput")
elem.send_keys("BARUERI")

labels = chrome.find_elements_by_tag_name("label")

for i in labels:
    if(i.text.upper() == "FGTS"):
        i.click()
        break

elem = chrome.find_element_by_tag_name("button")

if(elem.text.upper() == "CONSULTAR"):
    elem.click()

data = []
time.sleep(5)

rows = chrome.find_elements_by_tag_name("tr")

hasNewRows = any(rows)

qtd = chrome.find_element_by_class_name("total-mensagens")
if(qtd is not None):
    print(qtd.text)



for i in rows:
    if("SELECIONADA" not in i.text.upper()):
        aux = i.text.split(" ")
        row = Devedor()
        row.id = aux[0]
        row.cpf_cnpj = aux[1]
        row.valorDividaTotal = aux[-1]
        row.nome = i.text.replace(aux[0].strip().upper(), "").replace(aux[1].strip().upper(), "").replace(aux[-1].strip().upper(), "").strip()
        data.append(row)

jsonStr = json.dumps(data, default=lambda o: o.__dict__, 
               sort_keys=True, indent=4)

print(jsonStr)
