import tkinter as tk
from tkinter import colorchooser, messagebox
from typing import List, Tuple

from geometria import GerenciadorPoligonos
from algoritmos import preenchimento_scanline

class AplicacaoRenderizacao:
    """Classe principal da aplicação gráfica."""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Editor de Polígonos - CG 2025")
        
        self._gerenciador_poligonos = GerenciadorPoligonos()
        self._vertices_temporarios: List[Tuple[float, float]] = []
        self._modo_interacao = "desenho"

        self._configurar_interface_grafica()
        self._configurar_eventos_mouse()
        self.renderizar_cena()

    def _configurar_interface_grafica(self):
        """Configura os componentes visuais da aplicação."""
        self._frame_toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self._frame_toolbar.pack(side=tk.TOP, fill=tk.X)
        self._canvas = tk.Canvas(self.root, width=800, height=600, bg="black")
        self._canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self._criar_botoes_toolbar()
        self._criar_labels_status()

    def _criar_botoes_toolbar(self):
        botoes = [
            ("Alternar Modo", self._alternar_modo_interacao),
            ("Definir Cor", self._exibir_dialogo_cor),
            ("Preencher", self._aplicar_preenchimento_poligono),
            ("Remover Polígono", self._remover_poligono_selecionado),
            ("Limpar Tudo", self._limpar_cena),
        ]
        for texto, comando in botoes:
            tk.Button(self._frame_toolbar, text=texto, command=comando).pack(side=tk.LEFT, padx=2, pady=2)

        self._var_mostrar_arestas = tk.BooleanVar(value=True)
        tk.Checkbutton(
            self._frame_toolbar, text="Exibir Arestas", variable=self._var_mostrar_arestas, command=self.renderizar_cena
        ).pack(side=tk.LEFT, padx=5)

    def _criar_labels_status(self):
        frame_status = tk.Frame(self.root)
        frame_status.pack(side=tk.BOTTOM, fill=tk.X)
        self._label_status = tk.Label(frame_status, text="Modo: Desenho")
        self._label_status.pack(side=tk.LEFT, padx=5)
        self._label_coordenadas = tk.Label(frame_status, text="Coordenadas: (0, 0)")
        self._label_coordenadas.pack(side=tk.RIGHT, padx=5)

    def _configurar_eventos_mouse(self):
        self._canvas.bind("<Button-1>", self._tratar_clique_esquerdo)
        self._canvas.bind("<Button-3>", self._tratar_clique_direito)
        self._canvas.bind("<Motion>", self._atualizar_coordenadas_ponteiro)

    def renderizar_cena(self):
        self._canvas.delete("all")
        for poligono in self._gerenciador_poligonos.poligonos:
            cor_rgb_hex = "#%02x%02x%02x" % poligono.cor_rgb
            if poligono.preenchimento_ativado:
                for x_inicio, x_fim, y in preenchimento_scanline(poligono):
                    self._canvas.create_line(x_inicio, y, x_fim, y, fill=cor_rgb_hex, width=1)
            
            if self._var_mostrar_arestas.get():
                cor_aresta = "red" if poligono.esta_selecionado else "yellow"
                self._canvas.create_polygon(poligono.vertices, outline=cor_aresta, fill="", width=2)
        
        if len(self._vertices_temporarios) > 1:
            self._canvas.create_line(self._vertices_temporarios, fill="cyan", width=1, dash=(4, 4))

    def _tratar_clique_esquerdo(self, event):
        if self._modo_interacao == "desenho":
            self._vertices_temporarios.append((event.x, event.y))
        else: # modo "selecao"
            self._gerenciador_poligonos.selecionar_poligono_em(event.x, event.y, tolerancia_aresta=3.0)
        self.renderizar_cena()

    def _tratar_clique_direito(self, event):
        if self._modo_interacao == "desenho" and len(self._vertices_temporarios) >= 3:
            self._gerenciador_poligonos.adicionar_poligono(self._vertices_temporarios)
            self._vertices_temporarios = []
            self.renderizar_cena()
        elif self._modo_interacao == "desenho":
            messagebox.showwarning("Aviso", "São necessários pelo menos 3 vértices para formar um polígono.")

    def _atualizar_coordenadas_ponteiro(self, event):
        self._label_coordenadas.config(text=f"Coordenadas: ({event.x}, {event.y})")

    def _alternar_modo_interacao(self):
        self._modo_interacao = "selecao" if self._modo_interacao == "desenho" else "desenho"
        status = "Seleção" if self._modo_interacao == "selecao" else "Desenho"
        self._label_status.config(text=f"Modo: {status}")
        self._vertices_temporarios = []
        self.renderizar_cena()

    def _limpar_cena(self):
        self._gerenciador_poligonos = GerenciadorPoligonos()
        self._vertices_temporarios = []
        self.renderizar_cena()

    def _exibir_dialogo_cor(self):
        poligono_selecionado = self._gerenciador_poligonos.poligono_selecionado
        if not poligono_selecionado:
            messagebox.showinfo("Aviso", "Selecione um polígono primeiro.")
            return
        
        cor_tupla_int = colorchooser.askcolor(title="Escolha uma cor")[0]
        if cor_tupla_int:
            poligono_selecionado.cor_rgb = cor_tupla_int
            self.renderizar_cena()

    def _aplicar_preenchimento_poligono(self):
        poligono_selecionado = self._gerenciador_poligonos.poligono_selecionado
        if poligono_selecionado:
            poligono_selecionado.preenchimento_ativado = not poligono_selecionado.preenchimento_ativado
            self.renderizar_cena()
        else:
            messagebox.showinfo("Aviso", "Selecione um polígono para preencher.")

    def _remover_poligono_selecionado(self):
        if self._gerenciador_poligonos.remover_poligono_selecionado():
            self.renderizar_cena()
        else:
            messagebox.showinfo("Aviso", "Nenhum polígono selecionado para remover.")