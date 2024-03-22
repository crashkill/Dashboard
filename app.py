import pandas as pd
import plotly.express as px
import streamlit as st
#from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="Dashboard de Vendas",
                   page_icon=":bar_chart:",
                   layout="wide")

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io='dataset\supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )
    return df

df = get_data_from_excel()
# -------------- Cria a animação Lottie -------------------------
#def load_lottiefile(filepath: str):
#    with open(filepath, "r") as f:
#        return json.load(f)
    
#lottie = ("lottie-animation\config-lottie.json")

# ------ Define o SIDEBAR 
st.sidebar.header("Selecione o Filtro Desejado:")

# --- Conjunto de Filtros -------#
# --- Filtro de Cidades
city = st.sidebar.multiselect(
    "Selecione a cidade",
    options=df["City"].unique(),
    default=df["City"].unique()
)

# --- Filtro de Tipo de Cliente
customer_type = st.sidebar.multiselect(
    "Selecione a cidade",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

# --- Filtro de genero
gender = st.sidebar.multiselect(
    "Selecione a cidade",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)
#------ Fim da montagem dos filtros

# ------ COncateno os filtros com as querys do Streamlit
# ------ Crio a variável df_selection 
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

#lotie_animatio_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
# ------- Colocando animação 
#st_lottie(
#   lottie,
#   speed=1,
#  reverse=False,
#  height=100,
#   width=100,
#   loop=True,
#   quality="high",
#   key="Hello",
#)
#st_lottie(lotie_animatio_url, key="user")

# ----- Criando a página de gráficos
st.title(":bar_chart: Dashboard de Vendas")
st.markdown("##")

# ---- Criando o topo do site
total_sales = df_selection["Total"].sum()
mean_sales = df_selection["Total"].mean()
average_rating = round(df_selection["Rating"].mean(), 2)
star_rating = ":star:" * int(round(average_rating, 2))
average_sale_by_transaction = round(mean_sales, 2)

left_collum, middle_collum, righ_collum = st.columns(3)
with left_collum:
    st.subheader("Total de Vendas")
    st.subheader(f"US $ {total_sales}")
with middle_collum:
    st.subheader("Média de Rating")
    st.subheader(f"{average_rating} {star_rating}")
with righ_collum:
    st.subheader("Média de Vendas por Transação")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")
# ---- Exibindo o Dataset 
st.dataframe(df_selection)

sales_by_product_sales = (
    df_selection.groupby(by=["Product line"]).sum(numeric_only=True)[["Total"]].sort_values(by="Total")
)

fig_product_sales = px.bar(
    sales_by_product_sales,
    x="Total",
    y=sales_by_product_sales.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_sales),
    template="plotly_white"
)

col1, col2, col3 = st.columns(3)

col1.plotly_chart(fig_product_sales)
col2.plotly_chart(fig_product_sales)
col3.plotly_chart(fig_product_sales)