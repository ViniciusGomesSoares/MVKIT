from dataclasses import dataclass
from typing import List
from datetime import datetime, timedelta

@dataclass
class TipoEntrega:
    id: str
    nome: str
    descricao: str
    icone: str
    tempo_min: int
    tempo_max: int
    valor_base: float
    
    def calcular_taxa(self, distancia_km: float, valor_pedido: float) -> float:
        raise NotImplementedError
    
    def tempo_entrega(self) -> str:
        return f"{self.tempo_min}-{self.tempo_max} min"
    
    def horario_chegada(self) -> str:
        agora = datetime.now()
        minimo = agora + timedelta(minutes=self.tempo_min)
        maximo = agora + timedelta(minutes=self.tempo_max)
        return f"{minimo.strftime('%H:%M')} - {maximo.strftime('%H:%M')}"

class EntregaPadrao(TipoEntrega):
    def __init__(self):
        super().__init__(
            id="padrao",
            nome="Entrega Padrão",
            descricao="Entrega no endereço cadastrado",
            icone="fa-truck",
            tempo_min=30,
            tempo_max=45,
            valor_base=5.90
        )
    
    def calcular_taxa(self, distancia_km: float, valor_pedido: float) -> float:
        return 0.0 if valor_pedido > 30 else max(3.90, self.valor_base - (distancia_km * 0.2))

class EntregaExpressa(TipoEntrega):
    def __init__(self):
        super().__init__(
            id="expressa",
            nome="Entrega Expressa",
            descricao="Entrega mais rápida",
            icone="fa-bolt",
            tempo_min=15,
            tempo_max=25,
            valor_base=9.90
        )
    
    def calcular_taxa(self, distancia_km: float, valor_pedido: float) -> float:
        return self.valor_base - min(2.0, distancia_km * 0.3)

class RetiradaLocal(TipoEntrega):
    def __init__(self):
        super().__init__(
            id="retirada",
            nome="Retirar no Local",
            descricao="Você busca seu pedido",
            icone="fa-store",
            tempo_min=20,
            tempo_max=30,
            valor_base=0.0
        )
    
    def calcular_taxa(self, distancia_km: float, valor_pedido: float) -> float:
        return 0.0

class ServicoEntregas:
    def __init__(self):
        self.tipos = [
            EntregaPadrao(),
            EntregaExpressa(),
            RetiradaLocal()
        ]
    
    def calcular_taxas(self, cep: str, valor_pedido: float, distancia_km: float) -> List[dict]:
        opcoes = []
        for tipo in self.tipos:
            taxa = tipo.calcular_taxa(distancia_km, valor_pedido)
            opcoes.append({
                "id": tipo.id,
                "nome": tipo.nome,
                "descricao": tipo.descricao,
                "icone": tipo.icone,
                "tempo": tipo.tempo_entrega(),
                "taxa": taxa,
                "taxa_formatada": f"Grátis" if taxa <= 0 else f"R$ {taxa:.2f}".replace(".", ","),
                "chegada_estimada": tipo.horario_chegada()
            })
        return sorted(opcoes, key=lambda x: x["tempo"])