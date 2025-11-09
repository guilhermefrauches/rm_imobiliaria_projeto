
from __future__ import annotations
import csv
from typing import Iterable
from .models import QuoteResult


class CsvExporter:
    @staticmethod
    def salvar_cronograma_12_meses(result: QuoteResult, caminho_csv: str) -> None:
        with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Mes", "Aluguel", "ParcelaContrato", "TotalMes"])
            for item in result.cronograma_12_meses:
                writer.writerow([item.mes, f"{item.aluguel:.2f}", f"{item.parcela_contrato:.2f}", f"{item.total:.2f}"])
