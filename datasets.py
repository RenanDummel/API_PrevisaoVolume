import pickle
import pandas as pd
from datas_feriados import formatarData
from sklearn.linear_model import LogisticRegression
from datas_feriados import verificaFeriadoNacional, verificaFeriadoEstadual


def criarModelo():
    try:
        #dados no csv são fictícios
        dataset = pd.read_csv("../PrevisaovolumeEmissao/arquivos/testes.csv",
                              sep=";", skipinitialspace=True, parse_dates=['dia'])
        modelo = LogisticRegression(solver='newton-cholesky')

        dataset['dia_semana'] = dataset['dia'].dt.day_name()
        dataset['dia_mes'] = dataset['dia'].dt.day
        dataset['mes'] = dataset['dia'].dt.month
        dataset['ano'] = dataset['dia'].dt.year

        # se dada data for feriado, recebe o valor 1 na coluna. se não for, recebe 0
        dataset['feriado_nacional'] = dataset['dia'].apply(
            lambda x: 1 if verificaFeriadoNacional(x) else 0)
        dataset['feriado_estadual'] = dataset['dia'].apply(
            lambda x: 1 if verificaFeriadoEstadual(x) else 0)

        # dias da semana dividido em colunas binárias separadas - melhora a precisão do modelo
        dataset['isDomingo'] = dataset['dia_semana'].apply(
            lambda x: 1 if x == 'Sunday' else 0)
        dataset['isSegunda'] = dataset['dia_semana'].apply(
            lambda x: 1 if x == 'Monday' else 0)
        dataset['isTerca'] = dataset['dia_semana'].apply(
            lambda x: 1 if x == 'Tuesday' else 0)
        dataset['isQuarta'] = dataset['dia_semana'].apply(
            lambda x: 1 if x == 'Wednesday' else 0)
        dataset['isQuinta'] = dataset['dia_semana'].apply(
            lambda x: 1 if x == 'Thursday' else 0)
        dataset['isSexta'] = dataset['dia_semana'].apply(
            lambda x: 1 if x == 'Friday' else 0)
        dataset['isSabado'] = dataset['dia_semana'].apply(
            lambda x: 1 if x == 'Saturday' else 0)
        # deleta coluna que contém os dias da semana
        dataset.drop(columns=['dia_semana',], inplace=True)

        x = dataset.drop(columns=['dia', 'qtdDia'])
        y = dataset['qtdDia']

        modelo.fit(x, y)
        pickle.dump(modelo, open(
            "../PrevisaovolumeEmissao/arquivos/testes.sav", 'wb'))

        return "Ok"
    except:
        return "Modelo não pôde ser criado", 500


def previsaoModelo(dia, mes, ano):
    try:
        data, erro = formatarData(dia, mes, ano)
        previsao = pd.DataFrame(columns=(
            'dia_mes',
            'mes',
            'ano',
        )
        )
    except:
        return erro
    
    try:
        previsao.loc[0] = [dia, mes, ano]
        previsao['data'] = data
        previsao['dia_semana'] = previsao['data'].dt.day_name()
        previsao['feriado_nacional'] = previsao['data'].apply(
            lambda x: 1 if verificaFeriadoNacional(x) else 0)
        previsao['feriado_estadual'] = previsao['data'].apply(
            lambda x: 1 if verificaFeriadoEstadual(x) else 0)
        previsao.drop(columns=['data'], inplace=True)
        previsao['isDomingo'] = previsao['dia_semana'].apply(
            lambda x: 1 if x == 'Sunday' else 0)
        previsao['isSegunda'] = previsao['dia_semana'].apply(
            lambda x: 1 if x == 'Monday' else 0)
        previsao['isTerca'] = previsao['dia_semana'].apply(
            lambda x: 1 if x == 'Tuesday' else 0)
        previsao['isQuarta'] = previsao['dia_semana'].apply(
            lambda x: 1 if x == 'Wednesday' else 0)
        previsao['isQuinta'] = previsao['dia_semana'].apply(
            lambda x: 1 if x == 'Thursday' else 0)
        previsao['isSexta'] = previsao['dia_semana'].apply(
            lambda x: 1 if x == 'Friday' else 0)
        previsao['isSabado'] = previsao['dia_semana'].apply(
            lambda x: 1 if x == 'Saturday' else 0)
        previsao.drop(columns=['dia_semana'], inplace=True)
    except:
        return "Não foi possível criar um data frame para a previsão", 500
    
    try:
        modelo = pickle.load(
            open("../PrevisaovolumeEmissao/arquivos/testes.sav", 'rb'))
        resultado = modelo.predict(previsao)
        return resultado, 200
    except:
        return "Modelo não foi encontrado.", 500
