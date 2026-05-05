# portafolio-de-inversion
# Simulador de Portafolio de Inversión

Este proyecto es una aplicacion interactiva desarrollada en Python usando Streamlit que permite simular la evolucion de un portafolio de inversión con datos historicos del mercado


# Características

- Selección de multiples activos (acciones)
- Simulación con capital inicial 
- Cálculo de rentabilidad
- Visualización interactiva con gráficos (Plotly)
- Distribución del portafolio
- Aplicación de comisión del broker


# ¿Como funciona?


- Descarga datos históricos de las acciones usando yfinance
- Calcula los retornos diarios
- Distribuye el capital de forma equitativa entre los activos
- Simula la evolución del portafolio en el tiempo
- Aplica una comisión sobre la inversión
- Muestra resultados visuales 

# librerias utilizadas

- Streamlit
- yfinance
- pandas
- numpy
- plotly

---

# Como correr el programa

- Clona este repositorio:


git clone https://github.com/juanfeolguin123-cmyk/portafolio-de-inversion


- Entra a la carpeta:

cd portafolio-de-inversion

- Instala las librerias :

python -m pip install streamlit yfinance plotly pandas numpy

- Ejecuta la aplicación:


python -m streamlit run app.py





