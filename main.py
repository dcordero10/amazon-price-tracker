import smtplib

import requests
import lxml
from bs4 import BeautifulSoup
from datetime import *
import os

url = "https://www.amazon.com/dp/B07KGVB6D6/ref=rn?pf_rd_r=77JX9G01VV3DBKWXSPAC&pf_rd_" \
      "p=2766766c-2bcd-49ca-aa83-83593d18e634"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}


response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")
print(soup.prettify())

price = soup.find(id="priceblock_dealprice").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)

date = datetime.now().strftime("%m/%d/%Y")
print(date)

price_history = {}

daily_info = {
    "date": date,
    "price": price_as_float
}

dict.update(daily_info)

my_gmail_email = os.environ["MY_GMAIL"]
password = os.environ["MY_PASS"]

if price_as_float < 700.00:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_gmail_email, password=password)
        connection.sendmail(
            from_addr=my_gmail_email,
            to_addrs=my_gmail_email,
            msg=f"Subject: Price low, buy now! \n\n Buy now!"
        )