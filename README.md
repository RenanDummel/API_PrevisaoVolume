# Previsão de volume de emissão
Algoritmo para prever a quantidade de documentos emitidos em uma determinada data
Projeto desenvolvido por RenanDummel durante o estágio obrigatório do Curso Técnico em Informática na empresa Migrate - 14/02/2024 a 02/05/2024

## Rodando o projeto
Para rodar o projeto, é necessário cloná-lo em sua máquina, além de ter Python 3 instalado.<br>
Após isso, execute o arquivo `main.py` em um terminal, e utilize o endereço disponibilizado pelo Flask para fazer chamadas à API

## Rotas
- `[POST, GET] /treinarModelo`: treina e salva o modelo do algoritmo.<br>
  Exemplo: <br>```/treinarModelo```

- `[GET] /previsao`: Envia uma data para receber a previsão de documentos emitidos.<br>
  Exemplo: <br>`/previsao?dia=24&mes=04&ano=2024`

- `[POST] /concatDataset`: Envia uma data e uma quantidade de documentos para adicionar à base de dados.<br>
  Exemplo: <br>`/concatDataset`<br>
  Corpo:
  ```json
  {
    "dia": "11",
    "mes": "01",
    "ano": "2021",
    "documentos": "223476"
  }