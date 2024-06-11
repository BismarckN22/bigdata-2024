import pandas as pd 
import plotly.express as px 
import streamlit as st  

st.set_page_config(page_title="Painel de Vendas", page_icon=":bar_chart:", layout="wide")

# dados da planilha vendas
@st.cache_data
def get_data_from_excel(file_path):
    df = pd.read_excel(
        io=file_path,
        engine="openpyxl",
        sheet_name="Vendas"
    )
    return df

# caminho da planilha
data_path = "vendas.xlsx"  
df = get_data_from_excel(data_path)

# barra lateral para selecionar os dados desejados
st.sidebar.header("Filtre aqui:")
cidade = st.sidebar.multiselect(
    "Selecione a cidade do comprador:",
    options=df["Cidade do comprador"].unique(),
    default=df["Cidade do comprador"].unique()
)

categoria = st.sidebar.multiselect(
    "Selecione o produto:",
    options=df["Título"].unique(),
    default=df["Título"].unique(),
)

estado_pagamento = st.sidebar.multiselect(
    "Selecione o estado do pagamento:",
    options=df["Estado do pagamento"].unique(),
    default=df["Estado do pagamento"].unique()
)

df_selection = df.query(
    "(`Cidade do comprador` == @cidade) & (`Título` == @categoria) & (`Estado do pagamento` == @estado_pagamento)"
)

# olha se o df está vazio com base na selecao e informa ao usuario
if df_selection.empty:
    st.warning("Nenhum dado disponível com base nos filtros atuais!")
    st.stop()

# página principal
st.title(":bar_chart: Painel de Vendas")
st.markdown("##")

# KPI
vendas_totais = df_selection["Preço total"].sum()
preco_medio_por_transacao = df_selection["Preço total"].mean()

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Vendas totais:")
    st.subheader(f"R$ {vendas_totais:,.2f}")
with right_column:
    st.subheader("Preço médio por transação:")
    st.subheader(f"R$ {preco_medio_por_transacao:.2f}")

st.markdown("""---""")

# Vendas por categoria do produto - bar chart
vendas_por_produto = df_selection.groupby(by=["Título"])[["Preço total"]].sum().sort_values(by="Preço total")
fig_produto_vendas = px.bar(
    vendas_por_produto,
    x="Preço total",
    y=vendas_por_produto.index,
    orientation="h",
    title="<b>Vendas por produto</b>",
    color_discrete_sequence=["#ffd700"] * len(vendas_por_produto),
    template="plotly_white",
)
fig_produto_vendas.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# Unidades vendidas por produto - bar chart
unidades_por_produto = df_selection.groupby(by=["Título"])[["Unidades vendidas"]].sum().sort_values(by="Unidades vendidas")
fig_unidades_vendidas = px.bar(
    unidades_por_produto,
    x="Unidades vendidas",
    y=unidades_por_produto.index,
    orientation="h",
    title="<b>Unidades vendidas por produto</b>",
    color_discrete_sequence=["#bada55"] * len(unidades_por_produto),
    template="plotly_white",
)
fig_unidades_vendidas.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# Vendas por data - line chart
vendas_por_data = df_selection.groupby(by=["Data"])[["Preço total"]].sum()
fig_data_vendas = px.line(
    vendas_por_data,
    x=vendas_por_data.index,
    y="Preço total",
    title="<b>Vendas por data</b>",
    color_discrete_sequence=["#00ff00"],
    template="plotly_white",
)
fig_data_vendas.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_data_vendas, use_container_width=True)
right_column.plotly_chart(fig_produto_vendas, use_container_width=True)

# unidade vendida por produto
st.plotly_chart(fig_unidades_vendidas, use_container_width=True)


