# Guía de pruebas

## Propósito

Esta guía reúne las verificaciones recomendadas antes de enviar cambios. Supone que se trabaja desde la raíz del repositorio y que los comandos usan el entorno virtual activo.

Documentos relacionados: [README](../README.md), [CONTRIBUTING](../CONTRIBUTING.md) y [REPRODUCIBILIDAD](REPRODUCIBILIDAD.md).

## Matriz de pruebas

| Prueba | Propósito | Comando | Resultado esperado | Si falla |
|---|---|---|---|---|
| 1. Dependencias | Confirmar que el entorno puede instalar el proyecto. | `python -m pip install -r requirements.txt` | Instalación sin errores de resolución ni compilación. | Verifique Python 3.9+, activación del entorno, conectividad y mensajes de `pip`. No cambie versiones sin justificarlo. |
| 2. Sintaxis | Detectar errores sintácticos en el script. | `python -m py_compile scripts/descargar_iter2020.py` | Salida vacía y código de retorno 0. | Revise el error y el cambio causante. `__pycache__` está ignorado por Git. |
| 3. Validación local | Comprobar el CSV canónico sin red. | `python scripts/descargar_iter2020.py --validate-only` | Reporte que termina en `Validación completada correctamente.` | Confirme la estructura extraída, la fuente y el contenido. No sustituya el archivo por una copia de terceros. |
| 4. Descarga aislada | Probar descarga, extracción completa, validación y escritura fuera del repositorio. | Use los comandos de «Descarga limpia» más abajo. | Estructura oficial válida en una raíz temporal y ningún cambio dentro del repositorio. | Revise conexión, respuesta de INEGI, espacio disponible y error específico del script. |
| 5. Idempotencia | Confirmar que una fuente canónica válida no se descarga de nuevo. | Repita el comando de descarga con el mismo valor de `--dest`. | Mensaje `La fuente oficial extraída ya está disponible; no se descargará de nuevo.` | Compruebe que reutilizó exactamente el mismo directorio y que la primera ejecución terminó correctamente. |
| 6. Archivo faltante | Verificar el mensaje del notebook sin tocar los datos reales. | Use la copia temporal descrita en «Prueba controlada de archivo faltante». | La celda de carga produce `FileNotFoundError`, menciona la fuente canónica y muestra el comando de descarga. | Confirme que la copia temporal se ejecutó sin la estructura canónica ni `datos.csv`; no mueva los datos reales. |
| 7. Notebook secuencial | Detectar dependencias ocultas entre celdas y cambios de resultados. | `jupyter nbconvert --to notebook --execute regresion_multivariada_censo2020.ipynb --output-dir outputs --output ejecucion_verificacion.ipynb` | Ejecución completa, en orden, con salida de verificación dentro de `outputs/`. | Reinicie el kernel, revise la primera celda fallida y compare entorno, datos y orden de ejecución. |
| 8. Estado de Git | Revisar el conjunto exacto de cambios. | `git status` | Sólo aparecen archivos intencionalmente modificados. | Retire de la propuesta artefactos, salidas o cambios no relacionados sin borrar trabajo ajeno. |
| 9. Reglas de exclusión | Confirmar que la estructura local, la compatibilidad heredada y los ZIPs permanecen ignorados. | `git check-ignore -v iter_00_cpv2020_csv/ datos.csv iter_00_cpv2020_csv.zip` | Se muestra una regla de `.gitignore` para cada ruta. | Detenga la propuesta y revise la contradicción antes de añadir archivos pesados. |

## Descarga limpia a un directorio temporal

Estos comandos crean una ruta única fuera del repositorio y usan la opción real `--dest`.

### Windows (PowerShell)

```powershell
$dest = Join-Path $env:TEMP ("iter2020-prueba-" + [guid]::NewGuid())
python scripts/descargar_iter2020.py --dest "$dest"
```

### macOS o Linux

```bash
dest="$(mktemp -d)/iter_00_cpv2020_csv"
python scripts/descargar_iter2020.py --dest "$dest"
```

Para probar idempotencia, repita en la misma sesión:

```bash
python scripts/descargar_iter2020.py --dest "$dest"
```

`--dest` designa la raíz de extracción; el script conserva dentro de ella la estructura `iter_00_cpv2020/...`. No use `--force` para la prueba de idempotencia.

## Prueba controlada de archivo faltante

La prueba se realiza sobre una copia temporal del notebook; no se mueve ni renombra la estructura canónica real.

### Windows (PowerShell)

```powershell
$tmp = Join-Path $env:TEMP ("iter2020-sin-datos-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $tmp | Out-Null
Copy-Item regresion_multivariada_censo2020.ipynb $tmp
Push-Location $tmp
jupyter nbconvert --to notebook --execute regresion_multivariada_censo2020.ipynb --output prueba_sin_datos.ipynb
Pop-Location
```

### macOS o Linux

```bash
tmp="$(mktemp -d)"
cp regresion_multivariada_censo2020.ipynb "$tmp/"
(cd "$tmp" && jupyter nbconvert --to notebook --execute regresion_multivariada_censo2020.ipynb --output prueba_sin_datos.ipynb)
```

La ejecución debe terminar con error en la celda de carga. Ese código de retorno distinto de cero es el resultado esperado de esta prueba negativa.

## Ejecución secuencial y comparación

La prueba 7 usa `nbconvert` para ejecutar el notebook en orden desde un kernel nuevo. El propio notebook crea `outputs/`, que está ignorado por Git. Después de ejecutar:

- confirme que no hubo celdas fuera de orden;
- compare los resultados principales con los resultados de referencia del README;
- investigue diferencias antes de actualizar conclusiones;
- no añada la copia ejecutada ni las salidas al *commit*.

## Comprobación final

Ejecute:

```bash
git status
git status --ignored --short
git check-ignore -v iter_00_cpv2020_csv/ datos.csv iter_00_cpv2020_csv.zip
```

`iter_00_cpv2020_csv/`, un eventual `datos.csv` heredado, los ZIPs y `outputs/` pueden aparecer como ignorados en la segunda consulta, pero no deben aparecer preparados, disponibles para *commit* ni ya versionados. Si algún dato aparece listo para confirmar, deténgase y corríjalo antes de abrir el *pull request*.
