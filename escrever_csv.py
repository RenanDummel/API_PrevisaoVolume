from csv import writer, DictWriter


def escreverCsv(data, documentos):
    try:
        with open('../PrevisaovolumeEmissao/arquivos/testes.csv', 'a', newline='') as arquivo:
            campos = ['dia', 'qtdDia']
            writer = DictWriter(arquivo, fieldnames=campos, delimiter=";")
            writer.writerow({'dia': data[0], 'qtdDia': documentos})

        return
    except:
        return "Ocorreu um erro ao tentar escrever a data no arquivo CSV.", 500
