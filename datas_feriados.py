import holidays
import numpy as np

lista_feriados_nacionais = holidays.CountryHoliday('BR')
lista_feriados_estaduais = sum([holidays.BR(subdiv=x)
                               for x in holidays.BR.subdivisions])


def formatarData(dia, mes, ano):
    try:
        dia = str(dia).zfill(2)
        mes = str(mes).zfill(2)
        data = np.datetime64(f'{ano}-{mes}-{dia}')
        return data, 200
    except:
        return f"Não foi possível converter {dia}/{mes}/{ano} em um objeto de data.", 500


def verificaFeriadoEstadual(data):
    return data in lista_feriados_estaduais


def verificaFeriadoNacional(data):
    return data in lista_feriados_nacionais
