import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate
import re
import time

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

url = 'https://www.amazon.com.br/s?i=electronics&rh=n%3A16243822011&s=popularity-rank&fs=true&ref=lp_16243822011_sar'
driver.get(url)

all_names = []
all_prices = []

price_pattern = r'R\$\s?(\d{1,3}(?:\.\d{3})*)(?:[^\d]*(\d{2}))?'

while True:
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-cy="title-recipe"]')
        names = [element.text.strip() for element in elements]

        elements_price = driver.find_elements(By.CSS_SELECTOR, 'div[data-cy="price-recipe"]')
        prices_F = [element.text.strip() for element in elements_price]

        prices = []
        for price in prices_F:
            cl_Price = ' '.join(price.split())
            match = re.search(price_pattern, cl_Price)
            if match:
                whole = match.group(1).replace('.', '')
                fraction = match.group(2) if match.group(2) else '00'
                formatted_price = f"R$ {whole},{fraction}"
                prices.append(formatted_price)
            else:
                prices.append("N/A")

        all_names.extend(names)
        all_prices.extend(prices)

        next_button = driver.find_element(By.CSS_SELECTOR, 'a.s-pagination-next')
        if "a.s-pagination-disabled" in next_button.get_attribute("class"):
            break
        next_button.click()

        time.sleep(2)
    except Exception as e:
        print(f"Erro durante a navegação: {e}")
        break

df = pd.DataFrame({
    "Tv's": all_names,
    "Preços": all_prices
})

print(tabulate(df, headers='keys', tablefmt='grid'))

df.to_csv("Tv's.csv", index=False)

driver.quit()