Markdown

# Demand Planning: Sistema de Pronóstico de Ventas y Optimización de Inventario

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)
![XGBoost](https://img.shields.io/badge/ML-XGBoost-orange)
![Statsmodels](https://img.shields.io/badge/Stats-SARIMA-purple)

Este proyecto es una solución integral de Business Intelligence y Machine Learning diseñada para predecir la demanda futura de una cadena de retail, utilizando como base el dataset "Superstore". El sistema permite a la gerencia tomar decisiones proactivas sobre la gestión de inventario basándose en el análisis de datos históricos y modelos predictivos avanzados.



## Tabla de Contenidos
1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Características Principales](#características-principales)
3. [Arquitectura Técnica](#arquitectura-técnica)
4. [Instalación y Ejecución](#instalación-y-ejecución)
5. [Modelos Utilizados](#modelos-utilizados)
6. [Capturas de Pantalla](#capturas-de-pantalla)



## Descripción del Proyecto

La gestión eficiente de inventario representa un desafío crítico en el sector retail: el exceso de stock genera costos de almacenamiento y capital inmovilizado, mientras que la falta de stock resulta en pérdida de ventas y clientes. Este sistema aborda dicha problemática mediante:

* **Análisis Histórico:** Exploración profunda de 4 años de transacciones para identificar tendencias y estacionalidad.
* **Predicción de Demanda:** Generación de pronósticos a 12 meses (o intervalos personalizados) para anticipar los requerimientos de stock.
* **Segmentación de Negocio:** Análisis granular filtrado por Región Geográfica y Categoría de Producto.

El proyecto fue desarrollado como parte del Seminario de Titulación (Analítica con Python).



## Características Principales

### 1. Dashboard Interactivo (Frontend)
* **Panel de Pronóstico:** Selección dinámica de modelos predictivos (SARIMA vs XGBoost), horizonte de tiempo y filtros de negocio.
* **Visión General (KPIs):** Visualización de métricas ejecutivas en tiempo real, incluyendo Ventas Totales, Margen de Ganancia y Ticket Promedio.
* **Análisis Detallado:** Mapas de calor para rentabilidad geográfica, gráficos de participación de mercado y rankings de productos por desempeño.

### 2. API Robusta (Backend)
* Arquitectura desacoplada basada en **FastAPI**.
* Endpoints dedicados para la configuración del sistema, cálculo de KPIs y generación de pronósticos bajo demanda.
* Procesamiento eficiente de series de tiempo utilizando **Pandas**.



## Arquitectura Técnica

El proyecto implementa una arquitectura de microservicios simplificada, separando la lógica de negocio de la capa de presentación.


## Instalación y Ejecución
Siga los siguientes pasos para ejecutar el proyecto en un entorno local.

Prerrequisitos
Python 3.8 o superior

Git

1. Clonar el repositorio
Bash

git clone [https://github.com/dev-x-mj/titulacion_g4.git](https://github.com/dev-x-mj/titulacion_g4.git)

cd titulacion_g4
2. Configurar el entorno virtual
Bash

# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Instalar dependencias
Bash

pip install -r requirements.txt
4. Ejecutar la Aplicación
El sistema requiere la ejecución simultánea del backend y el frontend en dos terminales separadas.

Terminal 1: Backend (API)

Bash

uvicorn backend.main:app --reload
El backend iniciará en: http://127.0.0.1:8000

Terminal 2: Frontend (Dashboard)

Bash

streamlit run frontend/app.py
El dashboard se abrirá automáticamente en el navegador predeterminado.

Modelos Utilizados
El sistema implementa y compara dos enfoques metodológicos distintos para el pronóstico de series de tiempo:

1. SARIMA (Seasonal ARIMA)
Justificación: El Análisis Exploratorio de Datos (EDA) reveló una fuerte estacionalidad anual (Lag 12) y una tendencia creciente en las ventas.

Configuración: Se utiliza un componente de diferenciación (d=1), validado mediante la prueba de Dickey-Fuller, junto con componentes estacionales mensuales.

Aplicación: Ideal para series de tiempo con patrones históricos claros y cíclicos.

2. XGBoost (Extreme Gradient Boosting)
Justificación: El análisis de autocorrelación permitió transformar el problema de series de tiempo en un problema de aprendizaje supervisado.

Feature Engineering: Se generan variables de rezago (Lags) dinámicas según la frecuencia seleccionada (Mensual/Trimestral) para capturar la memoria de la serie.

Aplicación: Eficaz para capturar relaciones no lineales y adaptarse a cambios abruptos en la demanda.
___
Autor: Christian Masaquiza Jerez, Seminario de Titulación 2025