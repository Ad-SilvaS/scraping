from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import re
from tabulate import tabulate

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

url = 'https://www.amazon.com.br/s?i=electronics&rh=n%3A16243822011&s=popularity-rank&fs=true&ref=lp_16243822011_sar'

driver.get(url)

all_names = []
all_prices = []

price_pattern = r'R\$\s?(\d{1,3}(?:\.\d{3})*)(?:[^\d]*(\d{2}))?'
wait = WebDriverWait(driver, 10)

while True:
    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-cy="title-recipe"]')))
        names = [element.text.strip() for element in elements]

        elements_price = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-cy="price-recipe"]')))
        prices_full = [element.text.strip() for element in elements_price]

        prices= []
        for i in range(len(names)):
            if i < len(prices_full):
                cl_price = ' '.join(prices_full[i].split())
                match = re.search(price_pattern, cl_price)
                if match:
                    whole = match.group(1).replace('.', '')
                    fraction = match.group(2) if match.group(2) else '00'
                    formatted_price = f"R$ {whole},{fraction}"
                    prices.append(formatted_price)
                else:
                    print(f"Preço não encontrado no produto {i + 1}: {cl_price}")
                    prices.append("N/A")
            else:
                print(f"Preço não encontrado no produto {i + 1}")
                prices.append("N/A")

        all_names.extend(names)
        all_prices.extend(prices)

        nxt_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.s-pagination-next')))
        if 's-pagination-disabled' in nxt_button.get_attribute('class'):
            break
        nxt_button.click()

    except (NoSuchElementException, TimeoutException) as e:
        print(f'Erro durante a navegação: {e}')
        break

df = pd.DataFrame({
    "TV's": all_names,
    "Preços": all_prices
})

print(tabulate(df, headers='keys', tablefmt='grid'))

df.to_csv('tvs.csv', index=False)

driver.quit()