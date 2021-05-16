import requests
from bs4 import BeautifulSoup
import smtplib
import os

email = os.environ["EMAIL"]
password = os.environ["PASSWORD"]

url = "https://www.amazon.ca/Bluetooth-Headphones-Waterproof-Earphones-Canceling/dp/B08Z3MQC21/ref=zg_bsnr_electronics_home_3?_encoding=UTF8&psc=1&refRID=RC5JR95BGX85QCZGA4W1"

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56",
"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
}

response = requests.get(url, headers=headers)
response.raise_for_status()
# print(response.text)

soup = BeautifulSoup(response.text, "html.parser")
price = float(soup.find(id="priceblock_ourprice").getText().split("$")[1])
title = soup.find(id="productTitle").getText().strip()

if price < 30:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(
            from_addr=email,
            to_addrs=email,
            msg=f"Subject:Amazon Price Alert!\n\n{title} is now ${price}\n{url}"
        )