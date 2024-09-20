from datetime import datetime, date
from matplotlib import pyplot as plt
import numpy as np
from bcb import sgs


capital = float(input("Informe o Capital investido: "))
frequencia = input("Informe a frequência do periodo (Y, M, D): ")
inicio = input("Informe a data inicial Maior que 1995/01/01 no formato YYYY/MM/DD: ")
final = input("Informe a data final no formato YYYY/MM/DD: ")

#Y maiusculo significa ano em formato YYYY, para informar o nome do mes trocar m por b
data_inicial = datetime.strptime(inicio, "%Y/%m/%d").date()  
data_final = datetime.strptime(final, "%Y/%m/%d").date()  

#Obter dados SELIC - sgs Banco central - Obter codigos de series temporais
taxas_SELIC = sgs.get({"selic": 11}, start=data_inicial, end=data_final)


taxas_SELIC = taxas_SELIC/100

capital_acomulado = capital * (1 + taxas_SELIC["selic"]).cumprod() - 1

capital_com_frequencia = capital_acomulado.resample(frequencia).last() #fechamento
# capital_com_frequencia = capital_acomulado.resample(frequencia).mean() #Media da frequencia


# ==================[QUESTAO 2]=============================


data_inicial_Q2 = date(2000,1,1)
data_final_Q2 = date(2022, 3, 31)

taxas_SELIC_Q2 = sgs.get({"selic": 11}, start=data_inicial, end=data_final)
janela_500D = ((1 + taxas_SELIC_Q2).rolling(window = 500)).apply(np.prod)



print(f"Taxa em janela de 500D: \n {taxas_SELIC_Q2}")

janela_500D = janela_500D.reset_index() #trasnformar o index em uma coluna

janela_500D["data_inicial"] = janela_500D["date"].shift(500)

janela_500D = janela_500D.dropna

janela_500D.columns = ["Data_Final", "Retorno_Selic_500D", "Data_Inicial"]

print(janela_500D)


#pegar maior retorno da tabela
maior_retorno = janela_500D["Retorno_Selic_500D"].max()

gabarito = janela_500D["Retorno_Selic_500D"] == maior_retorno

print(f"Janela de Maior Retorno: \n{gabarito}")
