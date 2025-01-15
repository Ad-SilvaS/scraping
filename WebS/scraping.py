import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tabulate import tabulate

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

url = 'https://www.kabum.com.br/hardware/placa-de-video-vga'

driver.get(url)

name_elements = driver.find_elements(By.CLASS_NAME, 'nameCard')
names = [element.text for element in name_elements]

price_elements = driver.find_elements(By.CLASS_NAME, 'priceCard')
prices = [element.text for element in price_elements]

nameList = names
priceList = prices

df = pd.DataFrame({
    'Placa de Vídeo': nameList,
    ' Preço': priceList
})

print(tabulate(df, headers='keys', tablefmt='grid'))

df.to_csv('placas.csv', index=False)