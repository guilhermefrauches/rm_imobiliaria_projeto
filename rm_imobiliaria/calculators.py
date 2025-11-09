
from __future__ import annotations
from typing import List
from .models import PropertyType, RentalConfig, QuoteRequest, QuoteResult, MonthBreakdown, arred2


class QuoteCalculator:
    def __init__(self, config: RentalConfig | None = None) -> None:
        self.config = config or RentalConfig()

    def _aluguel_base(self, req: QuoteRequest) -> float:
        c = self.config
        if req.tipo == PropertyType.APARTAMENTO:
            base = c.base_apartamento_1q
            if req.quartos == 2:
                base += c.add_apartamento_2q
            if req.garagem_apt_casa:
                base += c.add_garagem_apt_casa
            if not req.tem_criancas:
                base *= (1.0 - c.desconto_apartamento_sem_criancas)
            return arred2(base)

        if req.tipo == PropertyType.CASA:
            base = c.base_casa_1q
            if req.quartos == 2:
                base += c.add_casa_2q
            if req.garagem_apt_casa:
                base += c.add_garagem_apt_casa
            return arred2(base)


        base = c.base_estudio
        vagas = max(0, int(req.vagas_estudio or 0))
        if vagas >= 1:
            if vagas <= 2:
                base += c.estudio_pacote_ate2_vagas
            else:
                base += c.estudio_pacote_ate2_vagas + c.estudio_vaga_extra_apartir_3 * (vagas - 2)
        return arred2(base)

    def _parcelas_contrato(self, n: int) -> list[float]:
        n = max(1, min(n, self.config.contrato_max_parcelas))
        total = self.config.contrato_total
        base = arred2(total / n)
        parcelas = [base] * n
        soma = arred2(sum(parcelas))
        ajuste = arred2(total - soma)
        parcelas[-1] = arred2(parcelas[-1] + ajuste)
        return parcelas

    def gerar_orcamento(self, req: QuoteRequest) -> QuoteResult:
        aluguel = self._aluguel_base(req)
        parcelas = self._parcelas_contrato(req.parcelas_contrato)

        cronograma: list[MonthBreakdown] = []
        for mes in range(1, 13):
            parcela = parcelas[mes - 1] if mes <= len(parcelas) else 0.0
            total_mes = arred2(aluguel + parcela)
            cronograma.append(MonthBreakdown(mes, aluguel, parcela, total_mes))

        return QuoteResult(
            aluguel_mensal=aluguel,
            contrato_total=self.config.contrato_total,
            parcelas_contrato=len(parcelas),
            parcela_media_contrato=arred2(sum(parcelas) / len(parcelas)),
            cronograma_12_meses=cronograma,
        )
