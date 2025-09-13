# Rota Inteligente: Otimização de Entregas com Algoritmos de IA

**Sabor Express** precisa reduzir atrasos e custos nas entregas em horário de pico. Este projeto implementa uma solução didática que:
- Modela a cidade como **grafo** (bairros = nós; ruas = arestas com pesos de **tempo** e **distância**).
- Calcula **menor caminho** com **A*** (com heurística euclidiana), e demonstra **BFS**/**DFS**.
- **Agrupa** pedidos por proximidade geográfica com **K‑Means** (clustering).
- Gera **rotas heurísticas** por cluster (nearest-neighbor sobre custos A*).
- Compara **baseline** (ordem ingênua) vs. **otimizado**, reportando métricas.

> **Objetivo pedagógico:** cumprir os entregáveis da disciplina de *Artificial Intelligence Fundamentals*: parte teórica (README) + parte prática (código e outputs).

---

## 1) Descrição do problema e objetivos
- **Problema:** múltiplas entregas em uma malha urbana, com rotas definidas manualmente e custos crescentes.
- **Objetivo:** sugerir rotas mais curtas (em tempo), agrupando pedidos próximos e calculando caminhos eficientes entre pontos.

## 2) Abordagem adotada
1. **Representação do Grafo**: nós (bairros) possuem coordenadas (x, y). Arestas contêm `distance` e `time` (tempo = distância/velocidade + ruído de tráfego).
2. **Busca com heurística (A\*)**: custo por **tempo**; heurística = distância euclidiana / velocidade esperada.
3. **BFS/DFS**: para comparação de caminhos em grafo não ponderado (demonstração conceitual).
4. **Clustering (K‑Means)**: cria **zonas de entrega**; cada zona recebe uma rota dedicada.
5. **Roteamento por Heurística**: *nearest neighbor* calculando custo entre paradas com **A\***.
6. **Avaliação**: compara **baseline** vs. **otimizado** em **tempo total** de deslocamento e % de melhoria.

## 3) Algoritmos utilizados
- **A\*** (menor caminho com heurística) – `src/algorithms.py`
- **BFS / DFS** – `src/algorithms.py`
- **K‑Means** (clustering) – `src/clustering.py`
- **Heurística de roteamento** (nearest neighbor + A\*) – `src/routing.py`

## 4) Diagrama do grafo / modelo
Gerado automaticamente em `outputs/graph_astar.png` (grafo e caminho A\* de *Centro* até o último bairro).  
Clusters de entregas em `outputs/clusters.png`.

## 5) Resultados e análise
Após executar `main`, o projeto produz:
- `outputs/results.json` com:
  - custo A* (tempo) em um par origem‑destino,
  - rotas por cluster, custos por cluster e **tempo total otimizado**,
  - **baseline** (ordem ingênua) e **ganho percentual**.
- `outputs/deliveries_clustered.csv` com cada pedido rotulado por cluster.

**Interpretação:** em geral, o pipeline reduz o tempo total ao:
- Diminuir deslocamentos entre pedidos próximos (via clusters);
- Priorizar **caminhos ótimos** entre paradas (A\*).

**Limitações:** dados sintéticos, sem janelas de tempo/capacidade; rota por cluster é heurística simples; não há realimentação de tráfego em tempo real.

**Melhorias sugeridas:**
- Substituir nearest‑neighbor por 2‑opt/3‑opt ou **programação inteira mista (MILP)**;
- Adaptar para múltiplos entregadores (VRP) e **balanceamento de carga**;
- Integrar **dados reais de tráfego**; usar **A\*** dinâmico / **D\***;
- Explorar **DBSCAN** para captar zonas com formatos arbitrários;
- Avaliar com métricas adicionais: distância total, tempo médio por pedido, atraso estimado.

## 6) Como executar

### Requisitos
- Python 3.10+
- Bibliotecas (instale com `pip`):
```
pip install -r requirements.txt
```

### Execução
Crie um script `run.py` (exemplo abaixo) ou use seu próprio *entrypoint*:

```python
from src.main import run
import os

base = os.path.dirname(__file__)
data_dir = os.path.join(base, "data")
out_dir = os.path.join(base, "outputs")
print(run(data_dir, out_dir, k_clusters=3, depot_name="Centro"))
```

Então rode:
```
python run.py
```

Os gráficos e resultados aparecerão em `outputs/`.

## 7) Referências (inspiração)
- **UPS – ORION** (heurísticas + dados de tráfego em tempo real).
- Casos no **Medium** com K‑Means/DBSCAN e **MILP** para logística.
- Artigos em **ResearchGate** com IA + IoT + heurísticas (genéticos, RL).
- **Kardinal.ai** – planejamento dinâmico para *fresh delivery*.

