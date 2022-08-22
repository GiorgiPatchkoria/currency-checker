import requests
from bs4 import BeautifulSoup
import mysql.connector
import time    

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'giorgi',
    password = 'password123',
    database = 'currency'
)

cursor = mydb.cursor()

url = "https://myvaluta.ge/"
request = requests.get(url) 
sp = BeautifulSoup(request.content, 'html5lib') 


def main():
    choose_currency = input('Welcome! Choose currencies which you want to check: money/crypto  ').lower()
    if choose_currency == 'money':
        money()
    elif choose_currency == 'crypto':
        crypto()
    else:
        print('You should only write money or crypto, nothing else')
        main()

def repeat():
    repeating = input('Do you want to check currency again? Yes/No ').lower()
    if repeating == 'yes':
        main()
    elif repeating == 'no':
        exit()
    else:
        print('Your input is incorrect, please write only yes/no')
        repeat()


def money():    
    # The following line will generate a list of HTML content for each table
    div = sp.find_all("div", attrs={"class": "exchange-table"})
    # scraping first table with HTML code div[0]
    table1 = div[0]
    body = table1.find_all('tr')
    # creating empty list and dictionaries to fill them with information 
    currency = []
    dictionary1 = {}
    dictionary2 = {}
    for i in range(1,44):
        # Declare empty list to keep Columns names
        currencies = body[i]
        for item in currencies.find_all("td"): # loop through all td elements
            # convert the td elements to text and strip
            item = (item.text).strip()
            # append the clean column name to the list
            currency.append(item)

        name = currency[0]      # name of currencies
        amount = currency[1]    # amount of currencies, for example 1 USD or 1000 AMD
        price = currency[2]    # price of currencies
        dictionary1[name] = price       # adding name and price in dictionary
        dictionary2[price] = amount     # adding price and amount in dictionary
        currency.clear()        # clearing list to add next column in empty list

    def checking_currency():
        choose = input('Choose one of them: ').upper()
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        if choose in dictionary1:
            money = dictionary1[choose]         
            print(dictionary2[money] + ' ------> ' + money)      # printing name and price of currency
            # recording name, price and time in database
            sql = ("insert into money (name, price, time) values (%s, %s, %s)")  
            values = (dictionary2[money], money, now)
            cursor.execute(sql, values)
            mydb.commit()
            repeat()    # asking user if he/she wants to start program again
        else: 
            print('The currency which you entered does not exists')
            checking_currency()

    key_name = str([key for key in dictionary1]).strip("[]")         # separating names in dictionary
    print('Here are names of currencies:    ' + key_name)       # showing existing currencies to user in order to choose which one he/she wants to check
    checking_currency()



def crypto():
    # following line will generate a list of HTML content for each table
    div = sp.find_all("div", attrs={"class": "exchange-table"})
    # scraping first table with HTML code div[0]
    table2 = div[1]
    body = table2.find_all('tr')
    # creating empty list and dictionary to fill them with information 
    currency = []
    dictionary = {}
    for i in range(1,101):
        # Declare empty list to keep Columns names
        currencies = body[i]
        for item in currencies.find_all("td"):    # loop through all td elements
            item = (item.text).strip()      # convert the td elements to text and strip
            currency.append(item)       # append the clean column name to the list

        shorting = currency[0]    # shorting name of currencies
        name = shorting[24:].strip()   # name of currencies
        price = currency[1]      # price of currencies
        dictionary[name] = price     # adding values in dictionary
        currency.clear()        # clearing list to add next column in empty list

    def check_currency():
        choose = input('Choose one of them: ').upper()
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        if choose in dictionary:
            crypto = dictionary[choose]
            print(choose + ' ------> ' + crypto)         # printing name and price of currency
            #  recording name, price and time in database
            sql = ("insert into crypto (name, price, time) values (%s, %s, %s)")
            values = (choose, crypto, now)
            cursor.execute(sql, values)
            mydb.commit()
            repeat()      # asking user if he/she wants to start program again
        else: 
            print('The currency which you entered does not exists')
            check_currency()

    key_name = str([key for key in dictionary]).strip("[]")      # separating names in dictionary
    print('Here are names of currencies:     ' + key_name)      # showing existing currencies to user in order to choose which one he/she wants to check
    check_currency()


main()