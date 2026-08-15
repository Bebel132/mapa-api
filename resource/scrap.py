import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Infografico Acesso a Internet no Brasil (https://github.com/Bebel132; contato: emanuel2005batista@gmail.com)"
}

# ========== 1. PORCENTAGEM DE ACESSO À INTERNET ==========
pagina1 = requests.get('https://pt.wikipedia.org/wiki/Lista_de_unidades_federativas_do_Brasil_por_acesso_%C3%A0_Internet', headers=headers)
dados_pagina = BeautifulSoup(pagina1.content, 'html.parser')

tabela = dados_pagina.find("table", class_="wikitable")
linhas = tabela.find_all("tr")[1:]

tabela_dados = []

for linha in linhas:    
    td = linha.find_all("td")
    # Pula linhas que não têm células suficientes
    if len(td) < 3:
        continue
    
    estado = td[1].get_text(strip=True)
    if estado != 'Brasil':
        dado = {
            'estado': estado,
            'porcentagem': td[2].get_text(strip=True)
        }
        tabela_dados.append(dado)


# ========== 2. ÁREA DO BRASIL ==========
pagina2 = requests.get('https://pt.wikipedia.org/wiki/Lista_de_unidades_federativas_do_Brasil_por_%C3%A1rea', headers=headers)
dados_pagina = BeautifulSoup(pagina2.content, 'html.parser')

tabela = dados_pagina.find("table", class_="wikitable")
linhas = tabela.find_all("tr")

for linha in linhas:
    td = linha.find_all("td")
    # A tabela de área tem cabeçalhos extras; precisamos de pelo menos 2 colunas
    if len(td) < 2:
        continue
    
    # Na tabela de área, o estado está em td[0] (bandeira + nome) e a área em td[1]
    estado_na_tabela = td[0].get_text(strip=True)
    area_texto = td[1].get_text(strip=True).replace('\xa0', '').replace(' ', '').replace(',', '.')
    
    for tabela_linha in tabela_dados:
        if tabela_linha['estado'] == estado_na_tabela:
            try:
                tabela_linha['area'] = float(area_texto)
            except ValueError:
                tabela_linha['area'] = None
            break


# ========== 3. QUANTIDADE DE PESSOAS (POPULAÇÃO) ==========
pagina3 = requests.get("https://pt.wikipedia.org/wiki/Lista_de_unidades_federativas_do_Brasil_por_popula%C3%A7%C3%A3o", headers=headers)
dados_pagina = BeautifulSoup(pagina3.content, 'html.parser')

tabela = dados_pagina.find("table", class_="wikitable")
linhas = tabela.find_all("tr")

for linha in linhas:
    td = linha.find_all("td")
    if len(td) < 2:
        continue
    
    # O estado pode estar dentro de um link <a> ou direto no texto
    estado_na_tabela = td[0].get_text(strip=True)
    pessoas_texto = td[1].get_text(strip=True).replace('\xa0', '').replace(' ', '').replace(',', '.')
    
    for tabela_linha in tabela_dados:
        if tabela_linha["estado"] == estado_na_tabela:
            try:
                # Remove a parte decimal se houver (ex: "11.123.456,00" -> 11123456)
                if '.' in pessoas_texto and pessoas_texto.rfind('.') > pessoas_texto.rfind(','):
                    # Formato brasileiro: pontos como milhar, vírgula como decimal
                    pessoas_texto = pessoas_texto.replace('.', '').replace(',', '.')
                else:
                    pessoas_texto = pessoas_texto.replace(',', '').replace('.', '')
                
                tabela_linha["pessoas"] = int(float(pessoas_texto))
            except ValueError:
                tabela_linha["pessoas"] = None
            break