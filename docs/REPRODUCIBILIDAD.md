# Reproducibilidad y auditoría

## Propósito

Este documento describe cómo reconstruir el entorno, adquirir la fuente oficial, ejecutar el análisis de referencia y auditar su trazabilidad. Complementa el [README](../README.md), las [reglas de contribución](../CONTRIBUTING.md) y la [guía de pruebas](GUIA_DE_PRUEBAS.md).

El protocolo reduce fuentes de variación evitables, pero no afirma reproducibilidad absoluta entre equipos o versiones.

## Fuente de datos

El análisis utiliza el archivo nacional de **“Principales resultados por localidad (ITER) del Censo de Población y Vivienda 2020. Datos oportunos”**, publicado por el Instituto Nacional de Estadística y Geografía (INEGI).

- Cobertura: archivo nacional ITER 2020.
- Catálogo oficial: [ficha de descarga de INEGI](https://www.inegi.org.mx/app/descarga/ficha.html?tit=326108&ag=0&f=csv).
- Distribución configurada: dominio oficial `inegi.org.mx`.
- Archivo local principal: `iter_00_cpv2020_csv/iter_00_cpv2020/conjunto_de_datos/conjunto_de_datos_iter_00CSV20.csv`.

La estructura extraída no se versiona por su tamaño. Se obtiene mediante `scripts/descargar_iter2020.py`, el script de adquisición del proyecto, y conserva los directorios originales del ZIP; no debe reemplazarse por una copia de terceros. Un `datos.csv` en la raíz sólo se reconoce como compatibilidad heredada y no se crea automáticamente.

## Flujo de adquisición y análisis

```text
Fuente oficial de INEGI
        ↓
descarga temporal y validación
        ↓
extracción segura de la estructura original
        ↓
CSV canónico dentro de iter_00_cpv2020_csv/
        ↓
notebook ejecutado secuencialmente
        ↓
resultados y visualizaciones locales
```

El comando normal es:

```bash
python scripts/descargar_iter2020.py
```

El script descarga, valida y extrae antes de instalar atómicamente el árbol del proveedor. Para auditar la fuente canónica existente sin usar la red:

```bash
python scripts/descargar_iter2020.py --validate-only
```

`--dest DIRECTORIO` define otra raíz de extracción, dentro de la cual se conserva `iter_00_cpv2020/...`. `--force` solicita reemplazar el árbol extraído, pero el reemplazo sólo ocurre si la nueva descarga pasa las validaciones. `--force` y `--validate-only` son mutuamente excluyentes.

## Validaciones realizadas por el script

El script comprueba:

1. que la respuesta HTTP sea exitosa y que una redirección permanezca en el dominio oficial de INEGI;
2. que la descarga no esté vacía ni incompleta cuando se informa `Content-Length`;
3. el tipo real del archivo, sin confiar únicamente en el encabezado HTTP;
4. que una respuesta HTML de error no se acepte como ZIP o CSV;
5. que el ZIP sea legible y no contenga entradas dañadas;
6. que las rutas internas del ZIP sean seguras para la extracción;
7. que todas las entradas pertenezcan al árbol oficial `iter_00_cpv2020/` y que exista exactamente la ruta nacional esperada;
8. que el CSV sea UTF-8 válido, con o sin BOM, y use coma como separador;
9. que no haya encabezados vacíos o duplicados y estén presentes las columnas geográficas;
10. que estén presentes las variables y denominadores utilizados por el modelo;
11. que los tres registros nacionales iniciales tengan la estructura esperada;
12. que exista cobertura de las 32 entidades y registros `Total del Municipio`;
13. que una fuente canónica válida no se descargue ni sobrescriba sin `--force`;
14. que un árbol incompleto o inválido produzca un error útil;
15. que la instalación final del árbol del proveedor use escritura atómica, después de validar el candidato.

El reporte local incluye tamaño, SHA-256 calculado, codificación, separador, número de columnas, registros, entidades y totales municipales. El proyecto no publica en esta documentación un hash fijo de una versión de datos.

## Convención local de los datos

- La fuente principal reside bajo `iter_00_cpv2020_csv/`, carpeta ignorada por Git.
- El CSV canónico es `iter_00_cpv2020/conjunto_de_datos/conjunto_de_datos_iter_00CSV20.csv` dentro de esa raíz.
- `datos.csv` es únicamente una alternativa heredada, también ignorada; no es necesaria ni se genera automáticamente.
- La codificación confirmada es UTF-8, con aceptación de BOM; el separador confirmado es la coma.
- La primera fila es el encabezado.
- El notebook conserva ese encabezado y omite los tres registros agregados iniciales con `skiprows=range(1, 4)`.
- Esos tres registros son `Total nacional`, `Localidades de una vivienda` y `Localidades de dos viviendas`; no son cabeceras adicionales.
- Después, el notebook normaliza `NOM_LOC` y conserva los registros `TOTAL DEL MUNICIPIO` para construir la base municipal.

No es necesario copiar, editar, renombrar ni versionar manualmente el CSV para aplicar este protocolo.

## Entorno computacional

- Python 3.9 o superior, de acuerdo con las características usadas por la implementación y las versiones mínimas declaradas.
- Dependencias instaladas desde `requirements.txt`.
- Entorno virtual recomendado.
- Notebook ejecutado desde la raíz del repositorio y en orden secuencial.
- Semilla global confirmada: `SEED = 2026`.
- Nivel de significancia confirmado: `ALPHA = 0.05`.

Las dependencias se declaran mediante cotas mínimas, no mediante un entorno completamente fijado. Por ello, conviene registrar `python --version` y `python -m pip freeze` al investigar una diferencia, sin añadir ese inventario al repositorio salvo que forme parte justificada de una propuesta.

## Protocolo de réplica

1. Clone y entre en el repositorio:

   ```bash
   git clone https://github.com/israelcervantes31416/regresion-multivariada-censo2020.git
   cd regresion-multivariada-censo2020
   ```

2. Cree y active un entorno virtual según su sistema operativo.
3. Instale las dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Descargue y extraiga la estructura oficial:

   ```bash
   python scripts/descargar_iter2020.py
   ```

5. Valide explícitamente la fuente canónica instalada:

   ```bash
   python scripts/descargar_iter2020.py --validate-only
   ```

6. Inicie Jupyter desde la raíz:

   ```bash
   jupyter notebook regresion_multivariada_censo2020.ipynb
   ```

7. Reinicie el kernel y ejecute todas las celdas en orden.
8. Contraste las salidas con los resultados de referencia identificados en el README. Documente cualquier diferencia antes de atribuirla al modelo.

## Protocolo de auditoría

1. Revise `scripts/descargar_iter2020.py` y confirme la URL oficial, el nombre del CSV esperado y las validaciones activas.
2. Compare las columnas requeridas por el script con las variables, denominadores y nombres usados en el notebook.
3. Revise `skiprows=range(1, 4)`, el filtro de `NOM_LOC` y los filtros posteriores.
4. Trace cada variable derivada hasta su variable censal y denominador.
5. Confirme que la fuente enlazada corresponde al ITER nacional 2020 de INEGI.
6. Verifique que la estructura local y la compatibilidad heredada no estén bajo control de versiones:

   ```bash
   git check-ignore -v iter_00_cpv2020_csv/ datos.csv
   git ls-files iter_00_cpv2020_csv datos.csv
   git status
   ```

   El primer comando debe mostrar las reglas aplicables de `.gitignore`; el segundo no debe listar datos; y `git status` no debe presentarlos para confirmación.

7. Revise el historial o el *diff* de una propuesta para separar cambios documentales, técnicos y metodológicos.
8. Use las pruebas de [GUIA_DE_PRUEBAS.md](GUIA_DE_PRUEBAS.md) antes de aceptar cambios.

## Alcances y límites

- La fuente describe el Censo 2020; el repositorio no actualiza esos datos.
- El análisis es observacional y no establece causalidad.
- Los resultados son sensibles a filtros, variables, denominadores, transformaciones, versiones y cambios metodológicos.
- Diferencias de precisión numérica o renderizado pueden surgir entre entornos.
- Los resultados no representan automáticamente las condiciones actuales del país.
- Una extensión debe conservar el análisis original como referencia y declarar con precisión qué cambió.
