from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import json
def configure_chrome_driver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options = chrome_options)
    return driver
class Devedor:
    id = 0
    cpf_cnpj = ""
    nome = ""
    valor_divida_selecionada = ""
Chrome = webdriver.Chrome()
Chrome.get("https://www.listadevedores.pgfn.gov.br/")
elem = Chrome.find_element_by_id("ufInput")
elem.send_keys("São Paulo")
time.sleep(3)
elem = Chrome.find_element_by_id("municipioInput")
elem.send_keys("Barueri")
labels = Chrome.find_elements_by_tag_name("label")
for i in labels:
    if (i.text.upper() == "FGTS"):
        i.click()
        break
time.sleep(1)
elem = Chrome.find_element_by_class_name("btn-warning")
elem.click()
data = []
time.sleep(5)

rows = Chrome.find_elements_by_tag_name("tr")

hasNewRows = any(rows)

qtd = Chrome.find_element_by_class_name("total-mensagens")
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
Chrome.close()
