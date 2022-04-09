#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import sys
from time import sleep
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import csv

#%%
s = Service('./src/chromedriver')
driver = webdriver.Chrome(service=s)
#%%
driver.get('https://dev.azure.com/neobpo')
driver.implicitly_wait(10)

sleep(3)

######## LOGIN AZURE DEVOPS
user = driver.find_element(by=By.XPATH, value='//*[@id="i0116"]')
user.clear()
user.send_keys('')
user.send_keys(Keys.ENTER)
driver.implicitly_wait(10)

sleep(3)
######## SENHA AZURE DEVOPS
passwd = driver.find_element(by=By.XPATH, value='//*[@id="i0118"]')
passwd.clear()
passwd.send_keys('')
passwd.send_keys(Keys.ENTER)
driver.implicitly_wait(10)

sleep(3)

### Manter usuário logado
driver.find_element(by=By.XPATH, value='/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input').click()

#%%
def carregapag ():
    driver.get('https://dev.azure.com/neobpo/NeoFlow/_git/CORE')
    driver.find_element(by=By.XPATH, value='//*[@id="__bolt-breadcrumb-extra-content"]/div/div/button').click()
    ### TELA PARA IMPORTAR PROJETOS DO GIT
    driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div/div/div/div[4]/button[2]').click()
    ### FLAGAR AUTENTICAÇÃO DO GIT
    driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div/div/div/div[3]/div/div[2]/div[2]/div[2]').click()
#%%

def migracao(url, nome_repos):
    driver.implicitly_wait(10) 
    url_clone_git = driver.find_element(by=By.XPATH, value = '/html/body/div[2]/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/input')
    url_clone_git.send_keys(Keys.CONTROL,"a")
    url_clone_git.send_keys(Keys.BACK_SPACE)
    url_clone_git.send_keys(url)

    driver.implicitly_wait(10)
    nome_novo_repos = driver.find_element(by=By.XPATH, value = '/html/body/div[2]/div/div/div/div/div/div[3]/div/div[5]/div/div/input')
    nome_novo_repos.send_keys(Keys.CONTROL,"a")
    nome_novo_repos.send_keys(Keys.BACK_SPACE)
    nome_novo_repos.send_keys(nome_repos)

    driver.implicitly_wait(10)
    usergit = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/input')
    usergit.send_keys(Keys.CONTROL,"a")
    usergit.send_keys(Keys.BACK_SPACE)
    usergit.send_keys('rodolfo')
    
    driver.implicitly_wait(10)
    passgit = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div/div/div/div/div/div[3]/div/div[4]/div/div/input')
    passgit.send_keys(Keys.CONTROL,"a")
    passgit.send_keys(Keys.BACK_SPACE)
    passgit.send_keys('t1v1t!@#')

lista = []

with open ('./clientes_1.csv', 'r') as f:
    csvReader = csv.reader(f)
    for row in csvReader:
        lista.append(row[0])

lista.pop(0)
#%%
#lista[0]
len(lista)
#%%
i = 0
while i < len(lista):
    carregapag()
    driver.implicitly_wait(15)
    migracao(lista[i].split(';')[2] + '.git', lista[i].split(';')[1])
    # Inicia importação
    driver.find_element(by=By.XPATH, value = '/html/body/div[2]/div/div/div/div/div/div[4]/div/button[2]/span').click()
    sleep(40)
    i+=1

#%%
driver.close()
