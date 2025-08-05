from typing import List, Tuple, Optional

class Ponto:
    """Representa um ponto 2D com coordenadas x e y."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def para_tupla(self) -> Tuple[float, float]:
        return (self.x, self.y)

class Poligono:
    """Representa um polígono com vértices, cor e estado de preenchimento."""
    def __init__(self, vertices: List[Tuple[float, float]]):
        # Armazena os vértices internamente como objetos Ponto
        self._vertices_obj = [Ponto(x, y) for x, y in vertices]
        self._cor_rgb = (255, 255, 255)  # Branco padrão
        self._preenchimento_ativado = False
        self._esta_selecionado = False

    @property
    def vertices(self) -> List[Tuple[float, float]]:
        """Retorna uma lista de tuplas (x, y) para os vértices."""
        return [p.para_tupla() for p in self._vertices_obj]

    @property
    def vertices_obj(self) -> List[Ponto]:
        """Retorna a lista de objetos Ponto."""
        return self._vertices_obj

    @property
    def cor_rgb(self) -> Tuple[int, int, int]:
        return self._cor_rgb

    @cor_rgb.setter
    def cor_rgb(self, valor: Tuple[int, int, int]):
        self._cor_rgb = valor

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

class GerenciadorPoligonos:
    """Gerencia a coleção de polígonos na cena."""
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
        """Adiciona um novo polígono à coleção."""
        novo_poligono = Poligono(vertices)
        self._poligonos.append(novo_poligono)
        return novo_poligono

    def remover_poligono_selecionado(self) -> bool:
        """Remove o polígono atualmente selecionado."""
        if self._poligono_selecionado:
            self._poligonos.remove(self._poligono_selecionado)
            self._poligono_selecionado = None
            return True
        return False

    def selecionar_poligono_em(self, x: float, y: float, tolerancia_aresta: float) -> bool:
        """Seleciona o polígono mais acima que contém o ponto (x, y)."""
        from algoritmos import contem_ponto # Importação local para evitar ciclo
        
        poligono_encontrado = None
        for poligono in self._poligonos:
            if contem_ponto(poligono, x, y, tolerancia_aresta):
                poligono_encontrado = poligono # Pega o último (mais acima na pilha de desenho)

        if self._poligono_selecionado:
            self._poligono_selecionado.esta_selecionado = False

        self._poligono_selecionado = poligono_encontrado
        if self._poligono_selecionado:
            self._poligono_selecionado.esta_selecionado = True
            return True
        
        return False