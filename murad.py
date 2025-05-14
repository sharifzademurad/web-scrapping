from selenium import webdriver
from bs4 import BeautifulSoup
import openpyxl
import time, os

# Excel hazırla
wb = openpyxl.Workbook()
ws = wb.active
ws.append(["Başlıq", "Qiymət", "Şəhər", "Tarix", "Link"])

# Chrome-u başlıqsız aç
driver = webdriver.Chrome()
url = "https://tap.az/elanlar?keywords_source=typewritten&order=&q%5Buser_id%5D=&q%5Bcontact_id%5D=&q%5Bprice%5D%5B%5D=&q%5Bprice%5D%5B%5D=&q%5Bregion_id%5D=420&q%5Bkeywords%5D=macbook"
driver.get(url)
time.sleep(5)  # səhifə yüklənsin

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Elanları tap
for item in soup.select("div.products-i"):
    title = item.select_one(".products-name")
    price = item.select_one(".products-price")
    region = item.select_one(".products-region")
    date = item.select_one(".products-added")
    link_tag = item.select_one("a.products-link")

    link = "https://tap.az" + link_tag['href'] if link_tag and link_tag.has_attr('href') else ""

    ws.append([
        title.text.strip() if title else "",
        price.text.strip() if price else "",
        region.text.strip() if region else "",
        date.text.strip() if date else "",
        link
    ])

# Excel faylını saxla
wb.save("scrapping.xlsx")
print("✅ Məlumat uğurla 'scrapping.xlsx' faylına yazıldı.")
