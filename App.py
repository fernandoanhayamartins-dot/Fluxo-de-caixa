import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="Dashboard de Fluxo de Caixa", layout="wide")

st.title("📊 BI de Gestão Financeira")
st.markdown("---")

# Carregamento dos dados (Simulação baseada nos seus arquivos)
@st.cache_data
def load_data():
    # Agora lendo direto do arquivo Excel e especificando as abas
    df_fin = pd.read_excel("modelo_fluxo_caixa_powerbi.xlsx", sheet_name="F_Financeiro")
    df_plano = pd.read_excel("modelo_fluxo_caixa_powerbi.xlsx", sheet_name="D_PlanoContas")
    
    # Convertendo datas
    df_fin['Data'] = pd.to_datetime(df_fin.get('Data', pd.Timestamp.now()))
    return df_fin, df_plano

try:
    df_fin, df_plano = load_data()

    # --- MÉTRICAS PRINCIPAIS ---
    receita = df_fin[df_fin['Valor'] > 0]['Valor'].sum()
    despesa = df_fin[df_fin['Valor'] < 0]['Valor'].sum()
    saldo = receita + despesa

    col1, col2, col3 = st.columns(3)
    col1.metric("Receita Total", f"R$ {receita:,.2f}", delta_color="normal")
    col2.metric("Despesa Total", f"R$ {abs(despesa):,.2f}", delta_color="inverse")
    col3.metric("Saldo Líquido", f"R$ {saldo:,.2f}")

    # --- GRÁFICOS ---
    st.markdown("### Análise Temporal e por Categoria")
    
    c1, c2 = st.columns(2)
    
    # Gráfico 1: Evolução Mensal
    df_temp = df_fin.resample('M', on='Data').sum().reset_index()
    fig_evol = px.line(df_temp, x='Data', y='Valor', title="Evolução do Fluxo de Caixa")
    c1.plotly_chart(fig_evol, use_container_width=True)

    # Gráfico 2: Composição de Gastos (exemplo por conta)
    fig_pizza = px.pie(df_fin[df_fin['Valor'] < 0], values=abs(df_fin['Valor']), names='ID_Conta', 
                       title="Distribuição de Despesas por Conta")
    c2.plotly_chart(fig_pizza, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar arquivos: {e}")
    st.info("Certifique-se de que os nomes dos arquivos CSV coincidem com os códigos.")
