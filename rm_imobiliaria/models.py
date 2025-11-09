
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class PropertyType(Enum):
    APARTAMENTO = "APARTAMENTO"
    CASA = "CASA"
    ESTUDIO = "ESTUDIO"


@dataclass(frozen=True)
class RentalConfig:
    base_apartamento_1q: float = 700.0
    base_casa_1q: float = 900.0
    base_estudio: float = 1200.0

    add_apartamento_2q: float = 200.0
    add_casa_2q: float = 250.0

    add_garagem_apt_casa: float = 300.0

    estudio_pacote_ate2_vagas: float = 250.0
    estudio_vaga_extra_apartir_3: float = 60.0

    contrato_total: float = 2000.0
    contrato_max_parcelas: int = 5

    desconto_apartamento_sem_criancas: float = 0.05  # 5%


@dataclass
class QuoteRequest:
    tipo: PropertyType
    quartos: int | None
    tem_criancas: bool
    garagem_apt_casa: bool = False
    vagas_estudio: int = 0
    parcelas_contrato: int = 1  # 1..5


@dataclass
class MonthBreakdown:
    mes: int
    aluguel: float
    parcela_contrato: float
    total: float


@dataclass
class QuoteResult:
    aluguel_mensal: float
    contrato_total: float
    parcelas_contrato: int
    parcela_media_contrato: float
    cronograma_12_meses: List[MonthBreakdown]


def arred2(x: float) -> float:
    return round(float(x) + 1e-12, 2)
