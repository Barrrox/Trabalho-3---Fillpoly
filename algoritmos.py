from typing import List, Tuple, Dict, Iterator
from geometria import Ponto, Poligono

def preenchimento_scanline(poligono: Poligono) -> Iterator[Tuple[int, int, int]]:
    """
    Gera as linhas horizontais para preencher um polígono.
    Retorna um iterador de tuplas (x_inicio, x_fim, y).
    """
    tabela_arestas: Dict[int, List[Dict]] = {}
    vertices = poligono.vertices
    n = len(vertices)

    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]

        if y1 == y2:
            continue
        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        m_inverso = (x2 - x1) / (y2 - y1)
        
        tabela_arestas.setdefault(int(y1), []).append({
            'y_max': y2, 'x_atual': x1, 'm_inverso': m_inverso
        })

    arestas_ativas = []
    y_min = min(tabela_arestas.keys()) if tabela_arestas else 0
    y_max_global = max(edge['y_max'] for edges in tabela_arestas.values() for edge in edges) if tabela_arestas else 0

    for y in range(int(y_min), int(y_max_global) + 1):
        if y in tabela_arestas:
            arestas_ativas.extend(tabela_arestas[y])
        arestas_ativas = [edge for edge in arestas_ativas if edge['y_max'] > y]
        arestas_ativas.sort(key=lambda edge: edge['x_atual'])

        for i in range(0, len(arestas_ativas), 2):
            if i + 1 < len(arestas_ativas):
                x_inicio = int(round(arestas_ativas[i]['x_atual']))
                x_fim = int(round(arestas_ativas[i + 1]['x_atual']))
                yield (x_inicio, x_fim, y)

        for edge in arestas_ativas:
            edge['x_atual'] += edge['m_inverso']

def calcular_distancia_ponto_segmento(x: float, y: float, p1: Ponto, p2: Ponto) -> float:
    """Calcula a distância euclidiana entre um ponto e um segmento de reta."""
    if p1.x == p2.x and p1.y == p2.y:
        return ((x - p1.x)**2 + (y - p1.y)**2)**0.5

    l2 = (p1.x - p2.x)**2 + (p1.y - p2.y)**2
    t = max(0, min(1, ((x - p1.x) * (p2.x - p1.x) + (y - p1.y) * (p2.y - p1.y)) / l2))
    
    proj_x = p1.x + t * (p2.x - p1.x)
    proj_y = p1.y + t * (p2.y - p1.y)
    
    return ((x - proj_x)**2 + (y - proj_y)**2)**0.5

def contem_ponto(poligono: Poligono, x: float, y: float, tolerancia: float) -> bool:
    """Verifica se um ponto está dentro de um polígono (borda ou interior)."""
    vertices_obj = poligono.vertices_obj
    for i in range(len(vertices_obj)):
        p1 = vertices_obj[i]
        p2 = vertices_obj[(i + 1) % len(vertices_obj)]
        if calcular_distancia_ponto_segmento(x, y, p1, p2) < tolerancia:
            return True

    dentro = False
    n = len(vertices_obj)
    for i in range(n):
        p1 = vertices_obj[i]
        p2 = vertices_obj[(i + 1) % n]
        if ((p1.y > y) != (p2.y > y)):
            x_intersecao = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
            if x <= x_intersecao:
                dentro = not dentro
    return dentro