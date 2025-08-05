import tkinter as tk
from tkinter import colorchooser, messagebox
from typing import List, Tuple, Optional, Dict
from geometria import GerenciadorPoligonos, Poligono
from fillpoly import algoritmo_fillpoly


class App:
    """classe principal da aplicação gráfica"""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Teste FillPOLYNHU :P - CG 2025")
        
        # modelo
        self._gerenciador_poligonos = GerenciadorPoligonos()
        self._vertices_temporarios: List[Tuple[float, float]] = []
        self._cor_preenchimento_atual = (255, 255, 255)
        self._mostrar_arestas = True
        self._modo_interacao = "desenho"  # ou "selecao"

        # view
        self._configurar_interface_grafica()
        self._configurar_eventos_mouse()
        self.renderizar_cena()

    def _configurar_interface_grafica(self):
        """configura os componentes visuais da aplicação"""
        # toolbar
        self._frame_toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self._frame_toolbar.pack(side=tk.TOP, fill=tk.X)

        # canvas
        self._canvas = tk.Canvas(self.root, width=800, height=600, bg="black")
        self._canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # controles
        self._criar_botoes_toolbar()
        self._criar_labels_status()

    def _criar_botoes_toolbar(self):
        """cria os botões da barra de ferramentas"""
        botoes = [
            ("Modo Desenho/Seleção", self._alternar_modo_interacao),
            ("Limpar Cena", self._limpar_cena),
            ("Remover Polígono", self._remover_poligono_selecionado),
            ("Definir Cor", self._exibir_dialogo_cor),
            ("Aplicar Preenchimento", self._aplicar_preenchimento_poligono),
        ]
        
        for texto, comando in botoes:
            tk.Button(self._frame_toolbar, text=texto, command=comando).pack(side=tk.LEFT)

        # checkbutton para arestas
        self._var_mostrar_arestas = tk.BooleanVar(value=True)
        tk.Checkbutton(
            self._frame_toolbar, 
            text="Exibir Arestas", 
            variable=self._var_mostrar_arestas,
            command=self.renderizar_cena
        ).pack(side=tk.LEFT)

    def _criar_labels_status(self):
        """cria os labels informativos"""
        self._label_status = tk.Label(self.root, text="Modo Desenho: Clique para adicionar vértices")
        self._label_status.pack()
        
        self._label_coordenadas = tk.Label(self.root, text="Coordenadas: (0, 0)")
        self._label_coordenadas.pack()

    def _configurar_eventos_mouse(self):
        """configura os handlers de eventos de mouse"""
        self._canvas.bind("<Button-1>", self._tratar_clique_esquerdo)
        self._canvas.bind("<Button-3>", self._tratar_clique_direito)
        self._canvas.bind("<Motion>", self._atualizar_coordenadas_ponteiro)

    def renderizar_cena(self):
        """renderiza todos os elementos gráficos na cena"""
        self._limpar_viewport()
        self._renderizar_poligonos()
        self._renderizar_poligono_em_construcao()

    def _limpar_viewport(self):
        """limpa o canvas de desenho"""
        self._canvas.delete("all")

    def _renderizar_poligonos(self):
        """renderiza todos os polígonos da cena"""
        for poligono in self._gerenciador_poligonos.poligonos:
            if poligono.preenchimento_ativado:
                algoritmo_fillpoly(self, poligono)
                
            cor_aresta = "red" if poligono.esta_selecionado else "yellow"
            if self._var_mostrar_arestas.get():
                self._canvas.create_polygon(
                    poligono.vertices, 
                    outline=cor_aresta, 
                    fill="", 
                    width=2
                )

    def _renderizar_poligono_em_construcao(self):
        """renderiza o polígono que está sendo construído"""
        if len(self._vertices_temporarios) > 1:
            self._canvas.create_line(
                self._vertices_temporarios, 
                fill="yellow", 
                width=1
            )

    # métodos de interação
    def _tratar_clique_esquerdo(self, event):
        """Handler para clique esquerdo do mouse"""
        if self._modo_interacao == "desenho":
            self._vertices_temporarios.append((event.x, event.y))
        else:
            self._gerenciador_poligonos.selecionar_poligono_por_posicao(event.x, event.y)
        self.renderizar_cena()

    def _tratar_clique_direito(self, event):
        """Handler para o clique direito do mouse"""
        if self._modo_interacao == "desenho" and len(self._vertices_temporarios) >= 3:
            novo_poligono = self._gerenciador_poligonos.adicionar_poligono(self._vertices_temporarios)
            novo_poligono.cor_rgb = self._cor_preenchimento_atual
            self._vertices_temporarios = []
            self.renderizar_cena()
        else:
            messagebox.showerror("Erro", "São necessários pelo menos 3 vértices para formar um polígono")

    def _atualizar_coordenadas_ponteiro(self, event):
        """Atualiza a posição do cursor na interface"""
        self._label_coordenadas.config(text=f"Coordenadas: ({event.x}, {event.y})")

    # métodos de controle
    def _alternar_modo_interacao(self):
        """Alterna entre os modos de desenho e seleção"""
        self._modo_interacao = "selecao" if self._modo_interacao == "desenho" else "desenho"
        status = "Modo Seleção: Clique para selecionar polígonos" if self._modo_interacao == "selecao" else "Modo Desenho: Clique para adicionar vértices"
        self._label_status.config(text=status)
        self._vertices_temporarios = []
        self.renderizar_cena()

    def _limpar_cena(self):
        """Remove todos os polígonos da cena"""
        self._gerenciador_poligonos = GerenciadorPoligonos()
        self._vertices_temporarios = []
        self.renderizar_cena()

    def _exibir_dialogo_cor(self):
        """Exibe o seletor de cores e aplica ao polígono selecionado"""
        cor = colorchooser.askcolor()[0]
        if cor and self._gerenciador_poligonos.poligono_selecionado:
            self._gerenciador_poligonos.poligono_selecionado.cor_rgb = tuple(int(c) for c in cor)
            self.renderizar_cena()

    def _aplicar_preenchimento_poligono(self):
        """Ativa o preenchimento para o polígono selecionado"""
        if self._gerenciador_poligonos.poligono_selecionado:
            self._gerenciador_poligonos.poligono_selecionado.preenchimento_ativado = True
            self.renderizar_cena()

    def _remover_poligono_selecionado(self):
        """Remove o polígono atualmente selecionado"""
        if self._gerenciador_poligonos.remover_poligono_selecionado():
            self.renderizar_cena()

