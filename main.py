import numpy as np
import pandas as pd
from flask import Flask, request
from escrever_csv import escreverCsv
from datas_feriados import formatarData
from datasets import criarModelo, previsaoModelo

app = Flask(__name__)


@app.route('/concatDataset', methods=['POST'])
def concatDataset():
    dataset = pd.read_csv("../PrevisaovolumeEmissao/arquivos/testes.csv",
                          sep=";", skipinitialspace=True, parse_dates=['dia'])

    dados = request.json
    dia = dados.get('dia')
    mes = dados.get('mes')
    ano = dados.get('ano')
    documentos = dados.get('documentos')

    dataset['dia_mes'] = dataset['dia'].dt.day
    dataset['mes'] = dataset['dia'].dt.month
    dataset['ano'] = dataset['dia'].dt.year

    data = formatarData(dia, mes, ano)
    ultima_linha = formatarData(
        dataset['dia_mes'].iloc[-1], dataset['mes'].iloc[-1], dataset['ano'].iloc[-1])

    # nao permite adicinar algo no csv caso a data seja igual à mais recente do csv, ou anterior a ela
    if data > ultima_linha:
        escreverCsv(data, documentos)
        return "Ok", 200
    else:
        return "Data inválida", 400


@app.route('/treinarModelo', methods=['POST', 'GET'])
def treinarModelo():
    try:
        criarModelo()
        return "Ok"
    except:
        return "Não foi possível criar/treinar o modelo", 500


@app.route('/previsao', methods=['GET'])
def prever():
    dia = request.args.get('dia')
    mes = request.args.get('mes')
    ano = request.args.get('ano')

    resultado, codigo = previsaoModelo(dia, mes, ano)

    if (codigo == 200):
        return str(resultado)
    else:
        return f"Erro {codigo}: Não foi possível realizar uma previsão."


app.run()
