import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuracion de la pagina
st.set_page_config(page_title="Simulador de Portafolio", layout="wide")

st.title("Simulador de Portafolio")
st.markdown("Simula inversión en multiples empresas con datos reales del mercado")

#lista de empresas
empresas = ["TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "JPM", "KO", "NFLX"]


col1, col2, col3 = st.columns(3)

with col1:
    capital_inicial = st.number_input("Capital inicial (USD)", value=1000)

with col2:
    empresas_seleccionadas = st.multiselect(
        "Selecciona empresas",
        empresas,
        default=empresas[:5]
    )

with col3:
    comision = st.slider("Comision del broker (%)", 0.0, 5.0, 1.0) / 100

# simulacion
if st.button("Ejecutar simulación"):

    if len(empresas_seleccionadas) == 0:
        st.warning("Selecciona al menos una empresa")
        st.stop()

    datos = yf.download(empresas_seleccionadas, period="3mo")["Close"]

    # limpiar datos
    datos = datos.dropna()

    retornos = datos.pct_change().dropna()

    # distribucion igual
    pesos = np.array([1/len(empresas_seleccionadas)] * len(empresas_seleccionadas))

    # Simulacion portafolio
    portafolio = (retornos @ pesos) + 1
    portafolio = portafolio.cumprod()

    portafolio_total = capital_inicial * portafolio * (1 - comision)

    # resultados 
    resultados_individuales = []

    for empresa in empresas_seleccionadas:
        serie = datos[empresa] / datos[empresa].iloc[0]
        resultados_individuales.append(capital_inicial * serie)

    valor_final = portafolio_total.iloc[-1]
    rentabilidad = ((valor_final - capital_inicial) / capital_inicial) * 100

    col1, col2, col3 = st.columns(3)

    col1.metric("Valor final", f"${valor_final:.2f}")
    col2.metric("Rentabilidad", f"{rentabilidad:.2f}%")
    col3.metric("Activos", len(empresas_seleccionadas))

    #grafica
    fig = go.Figure()

    # Líneas individuales
    for i, empresa in enumerate(empresas_seleccionadas):
        fig.add_trace(go.Scatter(
            y=resultados_individuales[i],
            mode='lines',
            name=empresa,
            opacity=0.4
        ))

    # linea principal del portafolio
    fig.add_trace(go.Scatter(
        y=portafolio_total,
        mode='lines',
        name='Portafolio total',
        line=dict(width=4)
    ))

    fig.update_layout(
        title="Evolución del portafolio",
        xaxis_title="Días",
        yaxis_title="Valor (USD)",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Distribución del portafolio")

    valores_finales = [r.iloc[-1] for r in resultados_individuales]

    fig_pie = go.Figure(data=[go.Pie(
        labels=empresas_seleccionadas,
        values=valores_finales,
        hole=0.4
    )])

    fig_pie.update_layout(template="plotly_dark")

    st.plotly_chart(fig_pie, use_container_width=True)

# instrucciones
with st.expander("¿Como funciona nuestro simulador ?"):
    st.write("""
    Este simulador calcula la evolución de un portafolio de inversión
    usando datos históricos reales de mercado.

    - Se distribuye el capital equitativamente
    - Se calculan retornos diarios
    - Se aplica una comisión del broker
    - Se muestra la evolución del portafolio en el tiempo
    """)
