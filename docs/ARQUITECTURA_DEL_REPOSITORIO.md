# Arquitectura del repositorio

## Propósito

Esta guía resume la organización funcional y documental del proyecto. Los procedimientos operativos están en el [README](../README.md), la [guía de reproducibilidad](REPRODUCIBILIDAD.md) y la [guía de pruebas](GUIA_DE_PRUEBAS.md).

## Archivos principales

- `README.md`: presenta el contexto académico, instalación, fuente, ejecución, resultados de referencia y límites de interpretación.
- `CONTRIBUTING.md`: define el flujo y los criterios para proponer cambios.
- `CHANGELOG.md`: registra cambios documentados sin inventar versiones o publicaciones.
- `regresion_multivariada_censo2020.ipynb`: carga el ITER local, construye variables, estima el modelo, ejecuta diagnósticos y produce resultados y visualizaciones.
- `scripts/descargar_iter2020.py`: descarga desde INEGI, valida el contenido, conserva la estructura original del ZIP e instala el árbol de forma segura.
- `requirements.txt`: declara las dependencias mínimas de Python para el notebook.
- `LICENSE`: aplica la licencia MIT al código y distingue los términos aplicables a los datos.
- `docs/`: contiene las guías de arquitectura, reproducibilidad y pruebas.
- `.github/pull_request_template.md`: normaliza la información mínima para revisar propuestas.
- `.gitignore`: excluye datos, ZIPs, entornos, cachés y salidas locales.
- `iter_00_cpv2020_csv/`: estructura oficial extraída, local y no versionada; contiene el CSV canónico.
- `datos.csv`: compatibilidad heredada opcional; no forma parte de la distribución ni se genera automáticamente.

## Flujo lógico

```text
ZIP oficial de INEGI
        ↓
script de descarga, extracción y validación
        ↓
estructura original extraída localmente
        ↓
notebook
        ↓
resultados y visualizaciones
```

El notebook no descarga datos. El script no ejecuta el análisis. Esta separación permite auditar la adquisición antes de interpretar resultados.

## Separación de responsabilidades

### Datos

INEGI publica la fuente ITER 2020. El árbol `iter_00_cpv2020_csv/` conserva la estructura del proveedor, está ignorado por Git y contiene la fuente local canónica. `datos.csv` sólo se admite como fallback heredado.

### Adquisición

`scripts/descargar_iter2020.py` concentra la URL oficial, descarga, validaciones estructurales, extracción segura del árbol completo, protección del destino y sustitución atómica.

### Análisis

`regresion_multivariada_censo2020.ipynb` contiene las decisiones analíticas: carga, filtro municipal, variables, transformaciones, modelo, inferencia, diagnósticos, sensibilidad y visualizaciones.

### Documentación

El README orienta al usuario; `docs/` explica auditoría, pruebas y arquitectura; el changelog deja constancia de cambios documentados.

### Contribución

`CONTRIBUTING.md` y la plantilla de *pull request* obligan a declarar pruebas e impactos, especialmente cuando una propuesta puede modificar resultados.

## Reglas de trazabilidad

- No mezcle cambios metodológicos con cambios documentales si pueden revisarse por separado.
- No suba `iter_00_cpv2020_csv/`, `datos.csv`, ZIPs, copias ejecutadas del notebook ni salidas pesadas.
- Documente todo cambio que afecte variables, filtros, denominadores, transformaciones, inferencia o resultados.
- Mantenga los resultados originales como referencia; presente alternativas como extensiones o análisis de sensibilidad.
- Conserve el vínculo entre variables del notebook, columnas ITER y fuente oficial.
- Valide la adquisición antes de ejecutar el análisis y ejecute el notebook en orden.
