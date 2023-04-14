#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import joblib

import streamlit as st


# In[15]:


lista_colunas = ['host_is_superhost', 'host_listings_count', 'latitude', 'longitude',
       'accommodates', 'bathrooms', 'bedrooms', 'beds', 'extra_people',
       'minimum_nights', 'instant_bookable', 'mes', 'ano', 'n_amenities',
       'property_type_Apartment', 'property_type_Bed and breakfast',
       'property_type_Condominium', 'property_type_Guest suite',
       'property_type_Guesthouse', 'property_type_Hostel',
       'property_type_House', 'property_type_Loft', 'property_type_Outros',
       'property_type_Serviced apartment', 'room_type_Entire home/apt',
       'room_type_Hotel room', 'room_type_Private room',
       'room_type_Shared room', 'cancellation_policy_flexible',
       'cancellation_policy_moderate', 'cancellation_policy_strict',
       'cancellation_policy_strict_14_with_grace_period']


x_numericos = {'latitude': 0,  'longitude': 0, 'host_listings_count': 0, 'accommodates': 0, 
              'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0, 'minimum_nights': 0,
               'mes': 0, 'ano': 0, 'n_amenities': 0
              }

x_verdadeiro_falso = {'host_is_superhost': 0, 'instant_bookable':0 }


x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
            }


dicionario = {}
for chave, valores in x_listas.items():
    for valor in valores:
        dicionario[f'{chave}_{valor}'] = 0
    
    
for item in x_numericos:
    if item == 'latitude' or item == 'longitude':
        valor = st.number_input(f'{item}', step=0.00001, value=0.0, format='%.5f')
    elif item == 'extra_people':
        valor = st.number_input(f'{item}', step=0.01, value=0.0)
    else:
        valor = st.number_input(f'{item}', step=1, value=0)
    x_numericos[item] = valor

for item in x_verdadeiro_falso:
    valor = st.selectbox(f'{item}', ('Sim', 'Não'))
    if valor == 'Sim':
        x_verdadeiro_falso[item] = 1
    else: 
        x_verdadeiro_falso[item] = 0


for item in x_listas:
    valor = st.selectbox(f'{item}', x_listas[item])
    dicionario[f'{item}_{valor}'] = 1


butao = st.button('Prever o valor do imóvel')

if butao:
    dicionario.update(x_verdadeiro_falso)
    dicionario.update(x_numericos)
    valor_x = pd.DataFrame(dicionario, index=[0])
    valor_x = valor_x[lista_colunas]
    modelo = joblib.load('modelo.joblib')
    resposta = modelo.predict(valor_x)
    st.write(resposta[0])


# In[16]:




