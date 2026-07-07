#!/usr/bin/env python3
"""Descarga y valida el archivo nacional ITER 2020 publicado por INEGI."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import shutil
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Iterable


for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")


OFFICIAL_URL = (
    "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/"
    "datosabiertos/iter/iter_00_cpv2020_csv.zip"
)
EXPECTED_CSV_BASENAME = "conjunto_de_datos_iter_00CSV20.csv"
DEFAULT_DEST = Path(__file__).resolve().parent.parent / "datos.csv"

GEOGRAPHIC_COLUMNS = {
    "ENTIDAD",
    "MUN",
    "LOC",
    "NOM_ENT",
    "NOM_MUN",
    "NOM_LOC",
}
MODEL_COLUMNS = {
    "PCDISC_MEN",
    "P15YM_AN",
    "PDESOCUP",
    "VPH_SNBIEN",
    "VPH_PISOTI",
    "VPH_NDEAED",
    "PRO_OCUP_C",
    "P3HLINHE",
    "PHOG_IND",
    "POB_AFRO",
    "PSINDER",
    "P15YM_SE",
    "PSIN_RELIG",
    "PRESOE15",
}
DENOMINATOR_COLUMNS = {
    "P_3YMAS",
    "P_5YMAS",
    "POBHOG",
    "POBTOT",
    "PEA",
    "TVIVHAB",
}
REQUIRED_COLUMNS = GEOGRAPHIC_COLUMNS | MODEL_COLUMNS | DENOMINATOR_COLUMNS
P15_DENOMINATOR_ALIASES = {"P_15YMAS", "P15YMAS"}
EXPECTED_ENTITY_CODES = {f"{number:02d}" for number in range(1, 33)}


class IterError(Exception):
    """Error controlado durante la descarga o validación del ITER."""


@dataclass(frozen=True)
class ValidationReport:
    path: Path
    size: int
    sha256: str
    encoding: str
    delimiter: str
    columns: int
    records: int
    municipal_records: int
    entities: int


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalized(value: str) -> str:
    return " ".join(value.strip().casefold().split())


def validate_initial_national_rows(
    rows: list[list[str]], indexes: dict[str, int]
) -> None:
    expected = [
        ("0000", "total nacional"),
        ("9998", "localidades de una vivienda"),
        ("9999", "localidades de dos viviendas"),
    ]
    for physical_line, (row, (location, name)) in enumerate(
        zip(rows, expected), start=2
    ):
        if (
            row[indexes["ENTIDAD"]].strip() != "00"
            or row[indexes["MUN"]].strip() != "000"
            or row[indexes["LOC"]].strip() != location
            or normalized(row[indexes["NOM_LOC"]]) != name
        ):
            raise IterError(
                "La estructura nacional inicial del ITER no coincide con la esperada "
                f"(fila física {physical_line})."
            )


def validate_csv(path: Path) -> ValidationReport:
    if not path.is_file():
        raise IterError(f"No existe un archivo CSV en: {path}")

    with path.open("rb") as source:
        raw_prefix = source.read(1024)
    has_bom = raw_prefix.startswith(b"\xef\xbb\xbf")
    prefix = raw_prefix.removeprefix(b"\xef\xbb\xbf").lstrip()
    lowered = prefix.lower()
    if lowered.startswith((b"<!doctype html", b"<html")) or b"<html" in lowered:
        raise IterError("El archivo recibido es HTML, no el CSV del ITER.")

    encoding_label = "UTF-8 con BOM" if has_bom else "UTF-8"
    expected_width = 0
    records = 0
    municipal_records = 0
    entity_codes: set[str] = set()

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as source:
            reader = csv.reader(source, delimiter=",")
            try:
                raw_header = next(reader)
            except StopIteration as exc:
                raise IterError("El CSV está vacío.") from exc

            header = [column.strip().upper() for column in raw_header]
            expected_width = len(header)
            if expected_width == 0 or any(not column for column in header):
                raise IterError("El encabezado del CSV está vacío o incompleto.")
            if len(set(header)) != expected_width:
                raise IterError("El CSV contiene nombres de columnas duplicados.")

            missing = sorted(REQUIRED_COLUMNS - set(header))
            if not (P15_DENOMINATOR_ALIASES & set(header)):
                missing.append("P_15YMAS (o P15YMAS)")
            if missing:
                raise IterError(
                    "Faltan columnas requeridas por el proyecto: " + ", ".join(missing)
                )

            indexes = {name: header.index(name) for name in GEOGRAPHIC_COLUMNS}
            initial_rows: list[list[str]] = []
            for physical_line in range(2, 5):
                try:
                    row = next(reader)
                except StopIteration as exc:
                    raise IterError(
                        "El CSV termina antes de los tres registros nacionales iniciales."
                    ) from exc
                if len(row) != expected_width:
                    raise IterError(
                        f"La fila física {physical_line} tiene {len(row)} campos; "
                        f"se esperaban {expected_width}."
                    )
                initial_rows.append(row)
                records += 1

            validate_initial_national_rows(initial_rows, indexes)

            for physical_line, row in enumerate(reader, start=5):
                if len(row) != expected_width:
                    raise IterError(
                        f"La fila física {physical_line} tiene {len(row)} campos; "
                        f"se esperaban {expected_width}."
                    )
                records += 1
                entity = row[indexes["ENTIDAD"]].strip()
                if entity in EXPECTED_ENTITY_CODES:
                    entity_codes.add(entity)
                if normalized(row[indexes["NOM_LOC"]]) == "total del municipio":
                    municipal_records += 1
    except UnicodeDecodeError as exc:
        raise IterError("El CSV no tiene una codificación UTF-8 válida.") from exc
    except csv.Error as exc:
        raise IterError(f"El contenido no es un CSV legible: {exc}") from exc

    missing_entities = sorted(EXPECTED_ENTITY_CODES - entity_codes)
    if missing_entities:
        raise IterError(
            "El archivo no tiene cobertura nacional; faltan entidades: "
            + ", ".join(missing_entities)
        )
    if municipal_records == 0:
        raise IterError("No se encontraron registros 'Total del Municipio'.")

    return ValidationReport(
        path=path,
        size=path.stat().st_size,
        sha256=sha256_file(path),
        encoding=encoding_label,
        delimiter=",",
        columns=expected_width,
        records=records,
        municipal_records=municipal_records,
        entities=len(entity_codes),
    )


def ensure_safe_member_names(infos: Iterable[zipfile.ZipInfo]) -> None:
    for info in infos:
        name = info.filename.replace("\\", "/")
        path = PurePosixPath(name)
        has_drive = bool(path.parts and path.parts[0].endswith(":"))
        if path.is_absolute() or ".." in path.parts or has_drive:
            raise IterError(f"El ZIP contiene una ruta insegura: {info.filename!r}")


def extract_expected_csv(zip_path: Path, destination: Path) -> None:
    if not zipfile.is_zipfile(zip_path):
        raise IterError("La descarga anunciada como ZIP no es un ZIP legible.")
    try:
        with zipfile.ZipFile(zip_path) as archive:
            infos = archive.infolist()
            ensure_safe_member_names(infos)
            damaged = archive.testzip()
            if damaged is not None:
                raise IterError(f"El ZIP está dañado en la entrada: {damaged}")

            matches = [
                info
                for info in infos
                if not info.is_dir()
                and PurePosixPath(info.filename.replace("\\", "/")).name.casefold()
                == EXPECTED_CSV_BASENAME.casefold()
            ]
            if len(matches) != 1:
                raise IterError(
                    "El ZIP no contiene exactamente un CSV nacional esperado "
                    f"({EXPECTED_CSV_BASENAME})."
                )

            with archive.open(matches[0], "r") as source, destination.open("wb") as target:
                shutil.copyfileobj(source, target, length=1024 * 1024)
    except zipfile.BadZipFile as exc:
        raise IterError("El ZIP descargado no es legible.") from exc


def classify_download(path: Path, content_type: str) -> str:
    with path.open("rb") as source:
        prefix = source.read(1024).removeprefix(b"\xef\xbb\xbf").lstrip()
    lowered = prefix.lower()
    if lowered.startswith((b"<!doctype html", b"<html")) or b"<html" in lowered:
        raise IterError(
            "INEGI respondió con HTML en lugar del archivo de datos "
            f"(Content-Type: {content_type or 'no informado'})."
        )
    if zipfile.is_zipfile(path):
        return "zip"
    try:
        prefix.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise IterError("La descarga no es un ZIP ni un CSV UTF-8 válido.") from exc
    return "csv"


def verify_official_response_url(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").casefold()
    if parsed.scheme != "https" or not (host == "inegi.org.mx" or host.endswith(".inegi.org.mx")):
        raise IterError(f"La descarga fue redirigida fuera del dominio oficial de INEGI: {url}")


def download_to_temp(url: str, destination: Path) -> tuple[str, int]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "iter2020-reproducible/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            status = getattr(response, "status", None)
            if status is None or not 200 <= status < 300:
                raise IterError(f"Respuesta HTTP no exitosa: {status}")
            verify_official_response_url(response.geturl())
            content_type = response.headers.get_content_type()
            expected_length = response.headers.get("Content-Length")
            total = 0
            with destination.open("wb") as target:
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    target.write(block)
                    total += len(block)
    except urllib.error.HTTPError as exc:
        raise IterError(f"INEGI respondió con HTTP {exc.code}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise IterError(f"No fue posible conectar con INEGI: {exc.reason}") from exc

    if expected_length is not None and total != int(expected_length):
        raise IterError(
            f"Descarga incompleta: se recibieron {total} bytes de {expected_length}."
        )
    if total == 0:
        raise IterError("INEGI devolvió un archivo vacío.")
    return content_type, total


def print_report(report: ValidationReport) -> None:
    print(f"Archivo validado: {report.path}")
    print(f"Tamaño final: {report.size:,} bytes")
    print(f"SHA-256: {report.sha256}")
    print(f"Codificación: {report.encoding}; separador: {report.delimiter!r}")
    print(f"Columnas detectadas: {report.columns}")
    print(
        f"Registros: {report.records:,}; entidades: {report.entities}; "
        f"totales municipales: {report.municipal_records:,}"
    )
    print("Validación completada correctamente.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Descarga y valida el CSV nacional ITER 2020 de INEGI."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="reemplaza el destino sólo después de validar una nueva descarga",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="valida el archivo existente sin usar la red",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEFAULT_DEST,
        metavar="RUTA",
        help="ruta del CSV final (por defecto: datos.csv en la raíz del proyecto)",
    )
    args = parser.parse_args()
    if args.force and args.validate_only:
        parser.error("--force y --validate-only no pueden usarse juntos")
    return args


def run(args: argparse.Namespace) -> None:
    destination = args.dest.expanduser().resolve()
    print(f"URL oficial configurada: {OFFICIAL_URL}")

    if args.validate_only:
        print("Modo de sólo validación; no se usará la red.")
        print_report(validate_csv(destination))
        return

    if destination.exists() and not args.force:
        try:
            report = validate_csv(destination)
        except IterError as exc:
            raise IterError(
                f"El destino ya existe pero no pasó la validación: {exc} "
                "Revíselo o use --force para reemplazarlo de forma segura."
            ) from exc
        print("datos.csv ya existe y es válido; no se descargará de nuevo.")
        print_report(report)
        return

    if destination.exists():
        print("--force activo: el archivo actual sólo se reemplazará si la descarga es válida.")

    destination.parent.mkdir(parents=True, exist_ok=True)
    downloaded_at = datetime.now().astimezone().isoformat(timespec="seconds")
    print(f"Fecha/hora de descarga: {downloaded_at}")
    print(f"Descargando desde: {OFFICIAL_URL}")

    with tempfile.TemporaryDirectory(
        prefix=".iter2020-", dir=str(destination.parent)
    ) as temporary_directory:
        temporary = Path(temporary_directory)
        downloaded = temporary / "descarga.tmp"
        candidate = temporary / EXPECTED_CSV_BASENAME

        content_type, downloaded_size = download_to_temp(OFFICIAL_URL, downloaded)
        print(f"HTTP correcto; Content-Type: {content_type}")
        print(f"Descarga temporal completa: {downloaded_size:,} bytes")

        file_type = classify_download(downloaded, content_type)
        if file_type == "zip":
            print("ZIP detectado; comprobando integridad y CSV nacional.")
            extract_expected_csv(downloaded, candidate)
        else:
            print("CSV directo detectado.")
            shutil.copyfile(downloaded, candidate)

        report = validate_csv(candidate)
        os.replace(candidate, destination)

    final_report = ValidationReport(
        path=destination,
        size=report.size,
        sha256=report.sha256,
        encoding=report.encoding,
        delimiter=report.delimiter,
        columns=report.columns,
        records=report.records,
        municipal_records=report.municipal_records,
        entities=report.entities,
    )
    print("El archivo se instaló mediante escritura atómica.")
    print_report(final_report)


def main() -> int:
    try:
        run(parse_args())
    except (IterError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
