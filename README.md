# API - Acesso à Internet no Brasil

Esta API fornece dados estruturados sobre o acesso à internet nos estados brasileiros. Ela é utilizada para alimentar o infográfico interativo do projeto, permitindo que o frontend consulte informações atualizadas de forma dinâmica e eficiente.

## Visão Geral

A API foi construída com Flask e Flask-RESTX, utilizando SQLAlchemy para persistência dos dados em um banco SQLite. Os dados são coletados automaticamente via web scraping de fontes confiáveis da Wikipédia.

## Dados Disponíveis

Cada estado possui os seguintes atributos:

- `id`: Identificador único
- `estado`: Nome do estado
- `porcentagem`: Percentual da população com acesso à internet
- `area`: Área territorial em km²
- `pessoas`: População total
- `densidade`: Densidade demográfica (habitantes por km²)

## Endpoints

### `GET /estados/`

Retorna uma lista com os dados de todos os estados brasileiros.

#### Exemplo de resposta:
```json
[
  {
    "id": 1,
    "estado": "Ceará",
    "porcentagem": "74,3%",
    "area": 148825.6,
    "pessoas": 9240580,
    "densidade": 62
  },
  ...
]
```

## Coleta de Dados

Os dados são extraídos por meio do script `scrap.py`, que realiza scraping das seguintes páginas da Wikipédia:

- Percentual de acesso à internet por estado:
    - https://pt.wikipedia.org/wiki/Lista_de_unidades_federativas_do_Brasil_por_acesso_%C3%A0_Internet
- Área territorial por estado
    - https://pt.wikipedia.org/wiki/Lista_de_unidades_federativas_do_Brasil_por_%C3%A1rea
- População estimada por estado
    - https://pt.wikipedia.org/wiki/Lista_de_unidades_federativas_do_Brasil_por_popula%C3%A7%C3%A3o
