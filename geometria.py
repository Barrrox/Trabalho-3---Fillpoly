
from typing import List, Tuple, Optional


class Ponto:
    """representa um ponto 2D com coordenadas x e y"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def para_tupla(self) -> Tuple[float, float]:
        return (self.x, self.y)

class Poligono:
    """representa um polígono com vértices, cor e estado de preenchimento"""
    def __init__(self, vertices: List[Tuple[float, float]]):
        self._vertices = [Ponto(x, y) for x, y in vertices]
        self._cor_rgb = (255, 255, 255)  # Branco padrão
        self._cor_vertices = [(255,255,255) for vertice in vertices]
        self._preenchimento_ativado = False
        self._esta_selecionado = False

    @property
    def vertices(self) -> List[Tuple[float, float]]:
        return [p.para_tupla() for p in self._vertices]

    @property
    def cor_rgb(self) -> Tuple[int, int, int]:
        return self._cor_rgb

    @cor_rgb.setter
    def cor_rgb(self, valor: Tuple[int, int, int]):
        self._cor_rgb = valor

    @property
    def cor_vertices(self) -> List[Tuple[int, int, int]]:
        return self._cor_vertices
    
    @cor_vertices.setter
    def cor_vertices(self, lista_valores: List[Tuple[int, int, int]]):
        self._cor_vertices = lista_valores

    @property
    def preenchimento_ativado(self) -> bool:
        return self._preenchimento_ativado

    @preenchimento_ativado.setter
    def preenchimento_ativado(self, valor: bool):
        self._preenchimento_ativado = valor

    @property
    def esta_selecionado(self) -> bool:
        return self._esta_selecionado

    @esta_selecionado.setter
    def esta_selecionado(self, valor: bool):
        self._esta_selecionado = valor

    def contem_ponto(self, x: float, y: float, tolerancia: float = 2.0) -> bool:
        """implementação do algoritmo ray-casting com tratamento de arestas mas não é tão necessário"""
        # verificação de proximidade com arestas (Perguntar p prof!)
        for i in range(len(self._vertices)):
            p1 = self._vertices[i]
            p2 = self._vertices[(i + 1) % len(self._vertices)]
            if self._calcular_distancia_ponto_segmento(x, y, p1, p2) < tolerancia: #verificar a lógica da função com o adair!!
                return True

        # algoritmo ray-casting só p garantir o preenchimento correto mas o resultado não é tão diferente
        dentro = False
        n = len(self._vertices)
        
        for i in range(n):
            p1 = self._vertices[i]
            p2 = self._vertices[(i + 1) % n]
            
            if ((p1.y > y) != (p2.y > y)):
                x_intersecao = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                if x <= x_intersecao:
                    dentro = not dentro
                    
        return dentro

    def _calcular_distancia_ponto_segmento(self, x: float, y: float, p1: Ponto, p2: Ponto) -> float:
        """calcula distância euclidiana entre ponto e segmento de reta(Pode tá errado)"""
        # Se os Pontos são iguais
        if p1.x == p2.x and p1.y == p2.y:
            return ((x - p1.x)**2 + (y - p1.y)**2)**0.5

        l2 = (p1.x - p2.x)**2 + (p1.y - p2.y)**2
        t = max(0, min(1, ((x - p1.x) * (p2.x - p1.x) + (y - p1.y) * (p2.y - p1.y)) / l2))
        
        proj_x = p1.x + t * (p2.x - p1.x)
        proj_y = p1.y + t * (p2.y - p1.y)
        
        return ((x - proj_x)**2 + (y - proj_y)**2)**0.5

class GerenciadorPoligonos:
    """gerencia a coleção de polígonos"""
    def __init__(self):
        self._poligonos: List[Poligono] = []
        self._poligono_selecionado: Optional[Poligono] = None

    @property
    def poligonos(self) -> List[Poligono]:
        return self._poligonos

    @property
    def poligono_selecionado(self) -> Optional[Poligono]:
        return self._poligono_selecionado

    def adicionar_poligono(self, vertices: List[Tuple[float, float]]) -> Poligono:
        """adiciona um novo polígono"""
        novo_poligono = Poligono(vertices)
        self._poligonos.append(novo_poligono)
        return novo_poligono

    def selecionar_poligono_por_posicao(self, x: float, y: float) -> bool:
        """seleciona o polígono contendo as coordenadas especificadas"""
        for poligono in reversed(self._poligonos):
            if poligono.contem_ponto(x, y):
                if self._poligono_selecionado:
                    self._poligono_selecionado.esta_selecionado = False
                self._poligono_selecionado = poligono
                poligono.esta_selecionado = True
                return True
        return False

    def remover_poligono_selecionado(self) -> bool:
        """remove o polígono atualmente selecionado"""
        if self._poligono_selecionado:
            self._poligonos.remove(self._poligono_selecionado)
            self._poligono_selecionado = None
            return True
        return False