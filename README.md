# Curso-Python
 
### Automação Web

- Ler uma base com dois produtos e a partir disso, realizar a busca em dois sites (Google shopping e bucape);
- a busca realizada respeitou o valor mínimo e máximo definidos, bem como, as palavras banidas para excluir produtos que diferem da busca planejada;
- salvando o resultado de cada busca dos produtos em um arquivo Excel com o respectivo nome do produto, organizando os dados do menor para o maior valor;
- após isso, mandou um e-mail com os dois arquivos Excel como anexo.

### Automação de processo

- Importar as bases de dados: loja, vendas e e-mail;
- juntar as tabelas de vendas e lojas a partir do 'ID Loja'. Percorrer depois essa tabela para separar cada loja;
- criar uma pasta 'Backup Arquivos Lojas' e salvar cada tabela da loja em um arquivo Excel contendo o mês, dia o nome da loja no arquivo Excel;
- calcular os indicadores: faturamento, diversidade de produtos no ano e no dia, ticket médio do ano e no dia para cada uma das 25 lojas;
- enviar um e-mail para cada gerente da loja com uma tabela em html para saber se bateu as metas ou não, juntamente com um anexo do arquivo Excel da loja;
- realizar o ranking para a diretoria, enviando depois através do e-mail o ranking do dia e do ano.


### Projeto 3 - Ciência de dados
- Ler as bases de dados do Airbnb do estado RJ entre os anos 2018 e 2020, juntando essas baes;
- depois salvar em um arquivo de 1000 linhas essa base para fazer uma análise qualitativa;
- retirar as colunas que não serão úteis para precificar o valor do imóvel;
- tratar os valores faltante e análise do tipo de dado da coluna;
- fazera análise exploratória;
- verificar a correlação entre as colunas;
- excluir ou não os Outlier através de análises gráficas e lógica (se de fato pode excluir o Outlier );
- fazer o encoding das variáveis categóricas;
- definir os critérios de avaliação: R² (coeficiente de determinação) e RSME(Raiz quadrada do erro médio);
- treinar os modelos e avaliar o resultado de cada um;
- escolher o melhor modelo e fazer melhoria;
- salvar o melhor modelo, ou seja, salvar em arquivo o modelo já treinado;
- depois fazer um Deploy do modelo através do streamlit.

### Controle de estoque
- Criação de uma interface gráfica com o uso da biblioteca tkinter;
- conexão com o banco de dados SQL através do pyodbc;
- comando CRUD no banco de dados através dos botões da janela consumir, visualizar, adicionar e deletar insumos.


### Projeto de cotação de moedas
- Criação de interface gráfica através do tkinter;
— conexão com awesome API (api de moedas) através da biblioteca request;
- duas opções de busca de moedas na tela;
— primeira opção: seleciona a moeda disponível da API através da lista suspensa, bem como a data para fazer a busca da moeda;
— segunda opção: seleciona um arquivo Excel contendo as moedas para fazer a busca. Seleciona a data inicial e final, sendo depois realizada uma consulta na APi e com os dados retornado convertido em um arquivo Excel com cada coluna referente a uma moeda.


