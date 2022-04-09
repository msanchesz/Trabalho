#%%
from pickle import TRUE
import mechanize
from bs4 import BeautifulSoup as bs
from http import cookiejar ## http.cookiejar in python3
import pandas as pd

cj = cookiejar.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open("http://191.96.225.72/users/sign_in")

br.select_form(nr=0)
br.form['user[login]'] = ''
br.form['user[password]'] = ''
br.submit()

print (br.response().read())
# %%
############# PROJETOS CIELO
i = 1
url = 'http://191.96.225.72/search?group_id=&project_id=&repository_ref=&scope=projects&search=cielo&page={}'
br.open(url.format(i))
#print(br.response().read())
#%%
############# PROJETOS NEOFLOW
i = 1
url = 'http://191.96.225.72/search?utf8=%E2%9C%93&snippets=&scope=&search=neoflow&group_id=3'
br.open(url.format(i))

#%%
############# PROJETOS CLIENTES
i = 1
url = 'http://191.96.225.72/search?group_id=10&page={}&scope=&search=clientes&snippets=&utf8=%E2%9C%93'
br.open(url.format(i))
# %%
soup = bs(br.response().read())
projetos = soup.findAll('li', {'class': 'project-row'})
qtd_projetos = float(soup.find('li', {'class' : 'active'}).text.strip().replace('Projects', '').strip())
tipo_projeto = soup.find('span', {'class': 'namespace-name'}).text.strip().replace('\n', '')
nome_projeto = soup.find('span', {'class': 'project-name filter-title'}).text.strip().replace('\n', '')
descricao_projeto = soup.find('div', {'class': 'description'}).text.strip().replace('\n', '')
#url_git = soup.find('a', {'class': 'project'}).text.strip()
# %%
projetos.find('a', href=True)
#nome_projeto
#descricao_projeto
#print(float(soup.find('li', {'class' : 'active'}).text.strip().replace('Projects', '').strip()))
#url_git
# %%
len(projetos)
#%%
qtd_projetos
# %%
df = pd.DataFrame(
    columns=[
        'tipo_projeto',
        'nome_projeto',
        #'descricao_projeto',
        'url_git',
    ]
)
i = 0

#%%
projeto = projetos[0]
#%%
projeto
#%%
while qtd_projetos > df.shape[0]:
    i += 1
    print(f"Valor i: {i} \t\t qtd_projetos: {df.shape[0]}")
    br.open(url.format(i))
    soup = bs(br.response().read())
    projetos = soup.findAll('li', {'class': 'project-row'})
    for projeto in projetos:
        #print(projeto)
        try: 
            tipo_projeto = projeto.find('span', {'class': 'namespace-name'}).text.replace('\n', '').strip()
        except:
            tipo_projeto = None
        try: 
            nome_projeto = projeto.find('span', {'class': 'project-name filter-title'}).text.replace('\n', '').strip()
        except:
            nome_projeto = None
        #try: 
        #    descricao_projeto = projeto.find('div', {'class': 'description'}).text.replace('\n', '').strip()
        #except:
        #    descricao_projeto = None
        try: 
            urltmp = projeto.find('a', {'class': 'project'}, href = True).text.replace('\n', '').replace('C','').replace('S','').replace('J','').replace('N','').replace('P','').replace('D','').replace('G','').replace('E','').replace('B','').replace('V','').replace('R','').replace('T','').replace('I','').replace('Q','').replace('A','').strip()
            url_git = 'http://191.96.225.72/' + urltmp
        except:
            url_git = None

        df.loc[df.shape[0]] = [
        tipo_projeto,
        nome_projeto,
        #descricao_projeto,
        url_git,
        ]

#%%
df
#%%
df.to_csv('cielo.csv', sep=';', index=False)
# %%
df.to_csv('neoflow.csv', sep=';', index=False)
# %%
df.to_csv('clientes.csv', sep=';', index=False)
# %%
