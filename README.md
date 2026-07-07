# Regresión lineal multivariada aplicada al Censo de Población y Vivienda 2020

Implementación matricial, sin librerías multivariadas dedicadas, de un modelo de regresión lineal multivariada para analizar conjuntamente indicadores de vulnerabilidad social a nivel municipal en México con información del Censo de Población y Vivienda 2020 del Instituto Nacional de Estadística y Geografía (INEGI).

## Contexto académico

El repositorio acompaña la tesis de Licenciatura en Matemáticas Aplicadas titulada *La regresión multivariada como marco estadístico para el análisis conjunto de indicadores socioeconómicos: una aplicación al Censo de Población y Vivienda 2020*.

**Autor:** Israel Cervantes Juárez<br>
**Programa:** Licenciatura en Matemáticas Aplicadas<br>
**Institución:** Facultad de Ciencias Físico Matemáticas, Benemérita Universidad Autónoma de Puebla (BUAP)<br>
**Asesor:** Dr. Bulmaro Juárez Hernández

## Objetivo del análisis

El análisis estima conjuntamente cuatro variables respuesta de rezago social a partir de diez covariables sociodemográficas. Sobre una base de $n = 2{,}469$ municipios, $Y \in \mathbb{R}^{n \times 4}$ contiene las respuestas y $X \in \mathbb{R}^{n \times 11}$ contiene el intercepto y las covariables.

El modelo general es:

$$Y = XB + U$$

La implementación comprende estimación por mínimos cuadrados ordinarios multivariados; verificación de la descomposición $T = H + E$; contrastes globales de Wilks, Pillai y Hotelling–Lawley; descripción espectral de Roy; pruebas parciales tipo III; diagnósticos residuales y de influencia; análisis de sensibilidad; y análisis canónico.

## Alcance del repositorio

El repositorio contiene el notebook del análisis, las dependencias, un script reproducible para adquirir y validar la fuente oficial y documentación para instalar, ejecutar, probar y auditar el proyecto. No distribuye el archivo censal ni pretende actualizarlo: el periodo de referencia es el Censo 2020.

Las propuestas que cambien variables, filtros, transformaciones, supuestos o procedimientos estadísticos deben tratarse como extensiones metodológicas y no como sustituciones silenciosas del análisis original. Consulte [CONTRIBUTING.md](CONTRIBUTING.md).

## Estructura del repositorio

```text
.
├── .github/
│   └── pull_request_template.md
├── docs/
│   ├── ARQUITECTURA_DEL_REPOSITORIO.md
│   ├── GUIA_DE_PRUEBAS.md
│   └── REPRODUCIBILIDAD.md
├── outputs/                         # salidas locales ignoradas por Git
├── scripts/
│   └── descargar_iter2020.py
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── IsraelCervantesJuarez.pdf
├── LICENSE
├── README.md
├── regresion_multivariada_censo2020.ipynb
├── requirements.txt
└── datos.csv                        # archivo local ignorado; no se distribuye
```

La separación funcional se explica en [docs/ARQUITECTURA_DEL_REPOSITORIO.md](docs/ARQUITECTURA_DEL_REPOSITORIO.md).

## Requisitos

- Python 3.9 o superior. La implementación usa características del lenguaje disponibles desde Python 3.9 y las versiones mínimas declaradas en `requirements.txt`.
- Dependencias de `requirements.txt`: NumPy, pandas, SciPy, Matplotlib, IPython, Jupyter y Notebook.
- Windows, macOS o Linux con Python y Jupyter disponibles.
- Acceso a internet para la descarga inicial desde INEGI. La validación local con `--validate-only` no utiliza la red.
- Espacio suficiente para el ZIP temporal y el CSV nacional.

Se recomienda un entorno virtual para aislar las dependencias. Las versiones mínimas están declaradas, pero cambios de versión pueden producir diferencias numéricas o visuales.

## Instalación desde cero

Clone el repositorio y entre en él:

```bash
git clone https://github.com/israelcervantes31416/regresion-multivariada-censo2020.git
cd regresion-multivariada-censo2020
```

### Windows (PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si el comando `py` no está disponible, use `python -m venv .venv`.

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

En algunas distribuciones de Linux puede ser necesario instalar previamente el paquete del sistema que proporciona `venv`.

## Descarga de datos

Desde la raíz del repositorio ejecute:

```bash
python scripts/descargar_iter2020.py
```

El script descarga la fuente configurada en el dominio oficial de INEGI, comprueba la respuesta y el contenido, extrae únicamente el CSV nacional esperado, valida su estructura y lo instala como `datos.csv` mediante escritura atómica. Si el destino ya existe y es válido, no vuelve a descargarlo.

Para validar el `datos.csv` existente sin usar la red:

```bash
python scripts/descargar_iter2020.py --validate-only
```

Las opciones adicionales confirmadas son `--dest RUTA`, para usar otro destino, y `--force`, para solicitar el reemplazo seguro de un destino existente. `--force` sólo reemplaza el archivo después de validar la nueva descarga y no puede combinarse con `--validate-only`.

### Sobre `datos.csv`

- No se incluye en GitHub por su tamaño.
- Se obtiene localmente desde la distribución oficial de INEGI.
- El script lo valida antes de instalarlo o utilizarlo como copia aceptada.
- Está ignorado por Git y no debe subirse al repositorio.
- No debe sustituirse por copias de terceros, porque se perdería la trazabilidad de la fuente.

No renombre ni elimine una copia válida para probar el proyecto; use `--dest` cuando necesite una descarga aislada.

## Fuente oficial

El conjunto utilizado es **“Principales resultados por localidad (ITER) del Censo de Población y Vivienda 2020. Datos oportunos”**, archivo nacional ITER 2020, publicado por el INEGI.

- [Ficha del catálogo de descarga de INEGI](https://www.inegi.org.mx/app/descarga/ficha.html?tit=326108&ag=0&f=csv)
- [Términos de libre uso de la información del INEGI](https://www.inegi.org.mx/inegi/terminos.html)

## Ejecución del notebook

Antes de abrir el notebook, debe existir un `datos.csv` válido en la raíz. El notebook no descarga los datos automáticamente; si el archivo falta, indica que debe ejecutarse el script de descarga.

```bash
jupyter notebook regresion_multivariada_censo2020.ipynb
```

También puede usarse JupyterLab o un editor compatible con `.ipynb`. Ejecute todas las celdas secuencialmente, desde la primera hasta la última, porque las celdas posteriores dependen del estado construido por las anteriores.

### Recorrido del análisis

| Celda | Contenido |
|---|---|
| 1 | Imports, rutas, semilla y configuración global. |
| 2 | Funciones auxiliares para estimación, SSCP y diagnósticos. |
| 3 | Carga del ITER y filtro a totales municipales. |
| 4 | Especificación formal de variables del modelo. |
| 5 | Construcción de tasas y proporciones. |
| 6 | Transformación por raíz cuadrada. |
| 7 | Construcción de las matrices $X$ y $Y$. |
| 8 | Estimación MCO multivariada. |
| 9 | Descomposición SSCP e inferencia global. |
| 10 | Pruebas parciales tipo III por predictor. |
| 11 | Normalidad multivariada de residuos mediante Mardia. |
| 12 | Diagnóstico auxiliar tipo White multivariado. |
| 13 | Diagnóstico estructural de residuos. |
| 14 | Influencia multivariada. |
| 15 | Análisis de sensibilidad por exclusión de influyentes. |
| 16 | Vistas del subespacio canónico. |
| 17 | Interpretación de las cuatro direcciones canónicas. |
| 18 | Visualizaciones de apoyo. |

La carga conserva el encabezado de la primera fila y omite los tres registros agregados iniciales mediante:

```python
pd.read_csv(DATA_PATH, skiprows=range(1, 4), encoding="utf-8")
```

Esos registros son `Total nacional`, `Localidades de una vivienda` y `Localidades de dos viviendas`; no son cabeceras adicionales. Después de la carga, el notebook selecciona los registros cuyo `NOM_LOC` es `TOTAL DEL MUNICIPIO`.

## Reproducibilidad

El análisis de referencia se apoya en:

- la fuente nacional oficial ITER 2020;
- las dependencias declaradas en `requirements.txt`;
- la semilla global confirmada `SEED = 2026`;
- el nivel de significancia `ALPHA = 0.05`;
- la validación previa de `datos.csv`;
- la ejecución secuencial del notebook;
- la comparación con los resultados de referencia del análisis original.

La estimación se implementa mediante álgebra lineal explícita. Las funciones `f`, `chi2` y `norm` de `scipy.stats` se usan para evaluar distribuciones y cuantiles, no para delegar el ajuste a una biblioteca multivariada dedicada.

Esto favorece la reproducción, pero no garantiza identidad absoluta entre entornos. Cambios en filtros, variables, transformaciones, versiones de dependencias o decisiones metodológicas pueden modificar los resultados. El protocolo completo y los puntos de auditoría están en [docs/REPRODUCIBILIDAD.md](docs/REPRODUCIBILIDAD.md).

## Resultados principales

Los siguientes son **resultados de referencia del análisis original** y no resultados recalculados por esta documentación:

- $R^2_{\mathrm{tr}} \approx 0.77$ y rechazo de la hipótesis nula global con Wilks, Pillai y Hotelling–Lawley.
- La primera dirección canónica absorbe el 93.8 % de la asociación y está dominada por analfabetismo adulto ($\rho_1 \approx 0.98$).
- La jerarquía de predictores está encabezada por la proporción de población sin escolaridad y la proporción de viviendas con piso de tierra.

## Límites de interpretación

- La fuente corresponde al Censo de Población y Vivienda 2020.
- El análisis es observacional; una asociación estadística no implica causalidad.
- Los resultados no deben trasladarse automáticamente a periodos, poblaciones o escalas territoriales diferentes.
- No deben emplearse para describir sin actualización y validación independiente la situación actual del país.
- Los diagnósticos y resultados dependen de las variables, filtros, transformaciones y versiones utilizadas en el análisis original.

## Contribución, auditoría y pruebas

- Para proponer cambios: [CONTRIBUTING.md](CONTRIBUTING.md).
- Para reproducir y auditar la trazabilidad: [docs/REPRODUCIBILIDAD.md](docs/REPRODUCIBILIDAD.md).
- Para ejecutar verificaciones antes de contribuir: [docs/GUIA_DE_PRUEBAS.md](docs/GUIA_DE_PRUEBAS.md).

## Licencia y datos

El código se distribuye bajo la licencia MIT; consulte [LICENSE](LICENSE). La licencia del código no se extiende a los datos. La información censal es publicada por el INEGI y está sujeta a sus propios términos de uso. El autor del repositorio no se atribuye la propiedad de esos datos.

## Citación

Si utiliza este código en un trabajo derivado, cite:

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
