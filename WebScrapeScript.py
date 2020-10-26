import requests
import time
from bs4 import BeautifulSoup
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",           ##input your own details
    database="pe"
)

with open('market_tickers.txt', 'r') as reader:
    market_type = ""
    for line in reader.readlines():
        if not line.isupper():
            market_type = line
            print("here")
        else:
            time.sleep(4)
            web_address = 'http://finance.yahoo.com/quote/' + line + '/'
            page = requests.get(web_address)
            soup = BeautifulSoup(page.content, 'html.parser')
            data = [entry.text for entry in soup.find_all('span', {'class': 'Trsdu(0.3s)'})]

            print(web_address)
            print(soup.prettify())
            print(data)
            pe_ratio = data[19]

            mycursor = mydb.cursor()

            sqlFormula = "INSERT INTO pe (Ticker, Industry, PE_ratio) VALUES (%s, %s, %f)"
            output = line + ", " + market_type + ", " + pe_ratio
            ##could use an array and execute many

            if type(pe_ratio == float):
                mycursor.execute(sqlFormula, output)
                mydb.commit()

            print(line + " " + pe_ratio)









