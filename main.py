
from __future__ import annotations
from rm_imobiliaria.models import PropertyType, QuoteRequest
from rm_imobiliaria.calculators import QuoteCalculator
from rm_imobiliaria.exporters import CsvExporter


def ask_int(msg: str, valid: set[int] | None = None) -> int:
    while True:
        try:
            v = int(input(msg).strip())
            if valid and v not in valid:
                print(f"Valor inválido. Opções: {sorted(valid)}")
                continue
            return v
        except ValueError:
            print("Digite um número válido.")

def ask_bool(msg: str) -> bool:
    while True:
        v = input(msg + " [s/n]: ").strip().lower()
        if v in ("s", "sim", "y"):
            return True
        if v in ("n", "nao", "não", "no"):
            return False
        print("Responda com s ou n.")

def escolher_tipo() -> PropertyType:
    print("Tipo de imóvel: 1) APARTAMENTO  2) CASA  3) ESTUDIO")
    op = ask_int("Escolha 1-3: ", valid={1,2,3})
    return {1: PropertyType.APARTAMENTO, 2: PropertyType.CASA, 3: PropertyType.ESTUDIO}[op]

def montar_requisicao() -> QuoteRequest:
    tipo = escolher_tipo()
    tem_criancas = ask_bool("Há crianças na família?")

    quartos = None
    garagem_apt_casa = False
    vagas_estudio = 0

    if tipo in (PropertyType.APARTAMENTO, PropertyType.CASA):
        quartos = ask_int("Quantidade de quartos [1 ou 2]: ", valid={1,2})
        garagem_apt_casa = ask_bool("Incluir 1 vaga de garagem? (+R$ 300,00)")
    else:
        vagas_estudio = ask_int("Quantidade de vagas de estacionamento (0..10): ", valid=set(range(0,11)))

    parcelas_contrato = ask_int("Parcelas do contrato (1 a 5): ", valid={1,2,3,4,5})

    return QuoteRequest(
        tipo=tipo,
        quartos=quartos,
        tem_criancas=tem_criancas,
        garagem_apt_casa=garagem_apt_casa,
        vagas_estudio=vagas_estudio,
        parcelas_contrato=parcelas_contrato,
    )

def imprimir_resultado(result) -> None:
    print("\n=== ORÇAMENTO R.M IMOBILIÁRIA ===")
    print(f"Aluguel mensal: R$ {result.aluguel_mensal:.2f}")
    print(f"Contrato: R$ {result.contrato_total:.2f} em {result.parcelas_contrato}x  (média: R$ {result.parcela_media_contrato:.2f})")
    print("\nCronograma 12 meses:")
    print("Mes | Aluguel  | ParcelaContrato | TotalMes")
    for it in result.cronograma_12_meses:
        print(f"{it.mes:>3} | {it.aluguel:>7.2f} | {it.parcela_contrato:>15.2f} | {it.total:>8.2f}")

def salvar_csv(result) -> None:
    salvar = input("\nSalvar CSV com as 12 parcelas? [s/n]: ").strip().lower()
    if salvar in ("s", "sim", "y"):
        caminho = input("Caminho do arquivo CSV (ex.: orcamento.csv): ").strip() or "orcamento.csv"
        CsvExporter.salvar_cronograma_12_meses(result, caminho)
        print(f"CSV salvo em: {caminho}")

def main():
    calc = QuoteCalculator()
    req = montar_requisicao()
    result = calc.gerar_orcamento(req)
    imprimir_resultado(result)
    salvar_csv(result)

if __name__ == "__main__":
    main()