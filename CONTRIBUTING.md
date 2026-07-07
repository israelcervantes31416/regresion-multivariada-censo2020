# Contribuir al proyecto

## Propósito

Esta guía ayuda a proponer cambios verificables sin perder la trazabilidad del análisis de tesis. Antes de contribuir, revise el [README](README.md), el [protocolo de reproducibilidad](docs/REPRODUCIBILIDAD.md) y la [guía de pruebas](docs/GUIA_DE_PRUEBAS.md).

## Alcance del proyecto

Este es un repositorio académico. El modelo, las variables y los resultados de referencia forman parte del análisis original y no deben modificarse sin una justificación explícita.

Clasifique la propuesta en una de estas categorías:

- **Corrección técnica:** corrige un error de implementación sin cambiar deliberadamente el planteamiento metodológico.
- **Mejora de reproducibilidad:** fortalece la adquisición, validación, ejecución o trazabilidad del análisis.
- **Mejora documental:** aclara el uso del proyecto sin modificar su comportamiento.
- **Cambio metodológico:** altera variables, filtros, transformaciones, supuestos, estimadores, pruebas o interpretación; debe presentarse como extensión o análisis de sensibilidad.

No mezcle cambios metodológicos y documentales en una misma propuesta cuando puedan revisarse por separado.

## Flujo recomendado

1. Cree un *fork* o una rama con un nombre descriptivo.
2. Cree y active un entorno virtual.
3. Instale las dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Descargue la estructura oficial o valide la fuente canónica local:

   ```bash
   python scripts/descargar_iter2020.py
   python scripts/descargar_iter2020.py --validate-only
   ```

5. Ejecute el notebook secuencialmente para establecer la referencia local.
6. Implemente el cambio y realice las pruebas pertinentes.
7. Documente su impacto en reproducibilidad y resultados.
8. Abra un *pull request* pequeño y revisable.

## Reglas obligatorias

- No suba `iter_00_cpv2020_csv/`, `datos.csv`, ZIPs, descargas parciales, cachés, salidas pesadas ni archivos temporales.
- No sustituya la fuente oficial de INEGI por fuentes de terceros.
- No cambie nombres de variables censales sin documentar la correspondencia con la fuente.
- No añada dependencias sin explicar su necesidad, versión mínima e impacto.
- Mantenga la compatibilidad operativa con Windows; si añade comandos, incluya una alternativa cuando difieran de macOS o Linux.
- No modifique conclusiones ni resultados de referencia sin explicar el cambio y su impacto.
- No sobrescriba el análisis original con una extensión metodológica.

## Validación mínima

Con el CSV canónico válido dentro de la estructura extraída, ejecute:

```bash
python -m py_compile scripts/descargar_iter2020.py
python scripts/descargar_iter2020.py --validate-only
git status
```

La compilación sintáctica puede crear un directorio `__pycache__`, que está ignorado por Git. Revise siempre que `git status` no muestre datos, ZIPs ni artefactos listos para confirmar.

## Validación adicional del análisis

Si modifica el análisis, las funciones estadísticas, la carga o las transformaciones:

1. Ejecute el notebook completo desde un kernel limpio.
2. Verifique que las celdas se ejecuten en orden y sin depender de estado previo.
3. Compare los resultados principales con los resultados de referencia del README.
4. Explique toda diferencia numérica, inferencial o visual, incluso si parece pequeña.
5. Registre las versiones relevantes del entorno utilizado para la prueba.

## Protocolo para cambios metodológicos

- Abra primero un *issue* o describa claramente la propuesta en el *pull request*.
- Justifique la decisión con bibliografía estadística pertinente.
- Conserve los resultados originales como referencia.
- Presente los resultados alternativos como extensión, robustez o sensibilidad.
- Mantenga la trazabilidad completa de variables, denominadores, filtros y transformaciones.
- Separe las diferencias debidas al método de las debidas al entorno computacional.

## Contenido de un pull request

Incluya:

- problema atendido y alcance;
- archivos modificados;
- pruebas realizadas y su resultado;
- impacto en reproducibilidad;
- impacto esperado u observado en resultados;
- referencias metodológicas, cuando corresponda.

Use la plantilla de `.github/pull_request_template.md`. Para ampliar las comprobaciones, consulte [docs/GUIA_DE_PRUEBAS.md](docs/GUIA_DE_PRUEBAS.md); para revisar el origen y flujo de los datos, consulte [docs/REPRODUCIBILIDAD.md](docs/REPRODUCIBILIDAD.md).
