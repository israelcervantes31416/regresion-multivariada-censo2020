# Regresión Lineal Multivariada Aplicada al Censo de Población y Vivienda 2020

Implementación matricial desde cero (sin librerías multivariadas dedicadas) de un modelo de regresión lineal multivariada para el análisis conjunto de indicadores de vulnerabilidad social a nivel municipal en México, con datos del Censo de Población y Vivienda 2020 del INEGI.

## Autor

**Israel Cervantes Juárez**  
Licenciatura en Matemáticas Aplicadas  
Facultad de Ciencias Físico Matemáticas  
Benemérita Universidad Autónoma de Puebla (BUAP)

Asesor: Dr. Bulmaro Juárez Hernández

## Resumen del proyecto

Sobre una base de $n = 2{,}469$ municipios se estima el modelo

$$Y = XB + U$$

donde $Y \in \mathbb{R}^{n \times 4}$ recoge cuatro variables respuesta de rezago social (limitación cognitiva, analfabetismo, desocupación, carencia de bienes en la vivienda) y $X \in \mathbb{R}^{n \times 11}$ agrupa el intercepto y diez covariables sociodemográficas. La implementación cubre:

- Estimación por MCO multivariado con verificación numérica de la descomposición $T = H + E$
- Pruebas globales con aproximaciones $F$ para Wilks, Pillai y Hotelling–Lawley; Roy se conserva como descriptor con cota superior de referencia cuando $s>1$
- Pruebas parciales tipo III por covariable
- Diagnóstico residual: normalidad multivariada de Mardia, heterocedasticidad tipo White multivariada, observaciones influyentes (leverage, distancia de Cook)
- Análisis de sensibilidad por exclusión de municipios influyentes
- Análisis canónico: cuatro direcciones interpretadas substantivamente

Resultados principales:

- $R^2_{\mathrm{tr}} \approx 0.77$, rechazo categórico de la nula global con todos los estadísticos
- Primera dirección canónica absorbe el 93.8% de la asociación, dominada por analfabetismo adulto ($\rho_1 \approx 0.98$)
- Jerarquía de predictores encabezada por proporción de población sin escolaridad y proporción de viviendas con piso de tierra

## Estructura del repositorio

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── regresion_multivariada_censo2020.ipynb
└── datos.csv  (NO INCLUIDO — ver sección "Obtención de datos")
```

## Requisitos

- Python 3.9 o superior
- Las dependencias listadas en `requirements.txt`

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/<TU_USUARIO>/<NOMBRE_REPO>.git
cd <NOMBRE_REPO>

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate          # macOS / Linux
venv\Scripts\activate             # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## Obtención de datos

El archivo `datos.csv` corresponde al **ITER 2020** del Censo de Población y Vivienda (INEGI). Por su tamaño (~143 MB) no se incluye en el repositorio.

Pasos para obtenerlo:

1. Ingresar a la página oficial del Censo 2020 de INEGI:  
   <https://www.inegi.org.mx/programas/ccpv/2020/>
2. Descargar el archivo **ITER Nacional CSV** desde la sección "Datos abiertos".
3. Renombrar el archivo descargado como `datos.csv` y colocarlo en la raíz del repositorio.

Las primeras tres filas del archivo (cabeceras descriptivas adicionales) se omiten al cargarlo: ver Celda 3 del notebook.

## Ejecución

Una vez instaladas las dependencias y colocado `datos.csv` en la raíz, abrir el notebook:

```bash
jupyter notebook regresion_multivariada_censo2020.ipynb
```

o bien con Jupyter Lab, VS Code o cualquier ejecutor de `.ipynb`. El notebook se compone de 18 celdas numeradas (`CELDA 1` a `CELDA 18`), ejecutables en orden secuencial:

| Celda | Contenido |
|---|---|
| 1 | Imports y configuración global (semilla, $\alpha = 0.05$, rutas) |
| 2 | Funciones auxiliares (MCO, SSCP, Mardia, White, vech, etc.) |
| 3 | Carga del archivo ITER y filtro a totales municipales |
| 4 | Especificación formal de variables del modelo |
| 5 | Construcción de tasas y proporciones |
| 6 | Transformación por raíz cuadrada |
| 7 | Construcción de matrices $X$ y $Y$ |
| 8 | Estimación MCO multivariada |
| 9 | Descomposición SSCP e inferencia global (con $H_0 : CB = 0$) |
| 10 | Pruebas parciales por predictor (con $H_{0j}$ por covariable) |
| 11 | Normalidad multivariada de residuos (Mardia) |
| 12 | Diagnóstico auxiliar de heterocedasticidad (White multivariado) |
| 13 | Diagnóstico estructural de residuos |
| 14 | Influencia multivariada (leverage, distancia de Cook) |
| 15 | Análisis de sensibilidad por exclusión de influyentes |
| 16 | Vistas alternativas del subespacio canónico |
| 17 | Interpretación de las cuatro direcciones canónicas |
| 18 | Visualizaciones de apoyo |

## Reproducibilidad

- Semilla global: `SEED = 2026`
- Nivel de significancia: `ALPHA = 0.05`
- Toda la estimación se realiza por álgebra lineal explícita; ninguna rutina se delega a librerías multivariadas externas.
- Las funciones de `scipy.stats` (`f`, `chi2`, `norm`) se usan únicamente para evaluar cuantiles y funciones de distribución acumulada.

## Citación

Si utilizas este código en un trabajo derivado, por favor cita:

```bibtex
@mastersthesis{cervantes2026regresionmultivariada,
  author       = {Cervantes Juárez, Israel},
  title        = {La regresión multivariada como marco estadístico para el análisis
                  conjunto de indicadores socioeconómicos: una aplicación al Censo
                  de Población y Vivienda 2020},
  school       = {Benemérita Universidad Autónoma de Puebla,
                  Facultad de Ciencias Físico Matemáticas},
  year         = {2026},
  type         = {Tesis de Licenciatura en Matemáticas Aplicadas}
}
```

## Licencia

Este código se distribuye bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para los términos completos.

Los datos del Censo de Población y Vivienda 2020 son propiedad del INEGI y se rigen por sus propios términos de uso (datos abiertos): <https://www.inegi.org.mx/inegi/terminos.aspx>.
