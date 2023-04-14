import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkcalendar import DateEntry
import pandas as pd
import requests
from datetime import datetime, date
import numpy as np


def pegar_cotacao():
    moeda = combobox_moedas.get()
    data = data_moeda.get()
    dia = data[:2]
    mes = data[3:5]
    ano = data[-4:]
    link = f'https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/?start_date={ano}{mes}{dia}&end_date={ano}{mes}{dia}'
    resposta = requests.get(link).json()
    label_resposta_cotacao['text'] = f'A cotação da moeda {moeda} na data {data} é de ' \
                                     f'R$ {resposta[0]["bid"].replace(".", ",")} reais'


def escolher_arquivo():
    caminho = askopenfilename(title='Selecione o arquivo xlsx')
    var_caminhoarquivo.set(caminho)
    if caminho:
        label_situacao_arquivo['text'] = caminho


def atualizar_cotacao():
    try:
        df = pd.read_excel(var_caminhoarquivo.get())
        moedas = df.iloc[:, 0]
        data_inicial = calendario_data_inicial.get()
        data_final = calendario_data_final.get()

        dia_inicial = data_inicial[:2]
        mes_inicial = data_inicial[3:5]
        ano_inicial = data_inicial[-4:]

        dia_final = data_final[:2]
        mes_final = data_final[3:5]
        ano_final = data_final[-4:]

        diferenca = date(int(ano_final), int(mes_final), int(dia_final)) - \
            date(int(ano_inicial), int(mes_inicial), int(dia_inicial))

        tempo = diferenca.days
        lista_df = []
        for moeda in moedas:
            link = f'https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/{tempo}?' \
                   f'start_date={ano_inicial}{mes_inicial}{dia_inicial}&end_date={ano_final}{mes_final}{dia_final}'
            cotacoes = requests.get(link)
            if cotacoes.status_code == 200:
                resposta_cotacoes = cotacoes.json()
                aux = []
                for resposta in resposta_cotacoes:
                    bid = float(resposta['bid'])
                    data = int(resposta['timestamp'])
    #                 dia, hora:minuto: segundo --> datetime -> 10/02/2015 10:30:20
    #                  dia --> date --> 10/02/2015
                    data = date.fromtimestamp(data)
                    aux.append((data, bid))
                novo_df = pd.DataFrame(aux, columns=['Data', moeda])
                lista_df.append(novo_df)
        if len(lista_df) == 0:
            label_arquivo['text'] = 'Não contém nenhuma moeda na coluna A. Selecione um arquivo válido'
            return
        primeiro_df = None
        for i, valor in enumerate(lista_df):
            if i == 0:
                primeiro_df = valor
            else:
                primeiro_df = pd.merge(primeiro_df, valor, on='Data', how='outer')
        primeiro_df.drop_duplicates('Data', keep='first', inplace=True)
        primeiro_df.set_index('Data', inplace=True)
        primeiro_df.sort_index(inplace=True)
        print(primeiro_df)
    except Exception as e:
        if isinstance(e, FileNotFoundError):
            label_arquivo['text'] = 'Arquivo não selecionado'
        if isinstance(e, ConnectionError):
            label_arquivo['text'] = 'Erro de conexão. Tente mais tarde'
        if isinstance(e, ValueError):
            label_arquivo['text'] = 'Formato de arquivo diferente'
    else:
        primeiro_df.to_excel('Juntos.xlsx')
        label_arquivo['text'] = 'Cotação Fianalizado com sucesso'



requisicao = requests.get('https://economia.awesomeapi.com.br/json/all').json()

lista_moedas = list(requisicao.keys())
janela = tk.Tk()
janela.title('Sistema de busca de cotações de moedas')

label_cotacao_moeda = tk.Label(text='Cotação de 1 moeda específica', borderwidth=2, relief='solid')
label_cotacao_moeda.grid(row=0, column=0, columnspan=3, sticky='nswe', padx=10, pady=10)

label_consultar_moeda = tk.Label(text='Selecione a moeda que deseja consultar:')
label_consultar_moeda.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

combobox_moedas = ttk.Combobox(janela, values=lista_moedas)
combobox_moedas.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)

label_data = tk.Label(text='Selecione o dia que deseja pegar a cotação da moeda')
label_data.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

data_moeda = DateEntry(locale='pt_br')
data_moeda.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)

label_resposta_cotacao = tk.Label()
label_resposta_cotacao.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

botao_pegar_cotacao = tk.Button(text='Pegar Cotação', command=pegar_cotacao)
botao_pegar_cotacao.grid(row=3, column=2, padx=10, pady=10, sticky='nsew')

label_cotacao_multiplas = tk.Label(text='Cotação de Múltiplas Moedas', borderwidth=2, relief='solid')
label_cotacao_multiplas.grid(row=4, column=0, columnspan=3, sticky='nswe', padx=10, pady=10)

label_selecionar_arquivo = tk.Label(text='Selecione um arquivo Excel com as Moedas na Coluna A:')
label_selecionar_arquivo.grid(row=5, column=0, columnspan=2, sticky='nswe', padx=10, pady=10)

var_caminhoarquivo = tk.StringVar()

botao_selecionar = tk.Button(text='Clique aqui para selecionar', command=escolher_arquivo)
botao_selecionar.grid(row=5, column=2, sticky='nsew', padx=10, pady=10)

label_situacao_arquivo = tk.Label(text='Nenhum arquivo selecionado', anchor='e')
label_situacao_arquivo.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

label_data_inicial = tk.Label(text='Data Inicial')
label_data_inicial.grid(row=7, column=0, padx=10, pady=10, sticky='nsew')

calendario_data_inicial = DateEntry(locale='pt_br')
calendario_data_inicial.grid(row=7, column=1, padx=10, pady=10, sticky='nsew')

label_data_final = tk.Label(text='Data Final')
label_data_final.grid(row=8, column=0, padx=10, pady=10, sticky='nsew')

calendario_data_final = DateEntry(locale='pt_br')
calendario_data_final.grid(row=8, column=1, padx=10, pady=10, sticky='nsew')

botao_atualizar = tk.Button(text='Atualizar Cotações', command=atualizar_cotacao)
botao_atualizar.grid(row=9, column=0, sticky='nsew', padx=10, pady=10)

label_arquivo = tk.Label()
label_arquivo.grid(row=9, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')

botao_fechar = tk.Button(text='Fechar', command=janela.quit)
botao_fechar.grid(row=10, column=2, padx=10, pady=10, sticky='nsew')
janela.mainloop()
