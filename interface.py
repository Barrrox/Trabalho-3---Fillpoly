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
        self._cor_preenchimento_atual = (255, 255, 255) # Inicializa branco
        self._mostrar_arestas = True
        self._modo_interacao = "desenho"  # ou "selecao"

        # view
        self._configurar_interface_grafica()
        self._configurar_eventos_mouse()
        self.renderizar_cena()

    @staticmethod
    def _s_rgb_para_hex(rgb_tuple: Tuple[int, int, int]) -> str:
        """Função auxiliar estática para converter RGB para o formato hexadecimal que o Tkinter usa"""
        return f"#{rgb_tuple[0]:02x}{rgb_tuple[1]:02x}{rgb_tuple[2]:02x}"

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
            novo_poligono.cor_vertices = [self._cor_preenchimento_atual] * len(self._vertices_temporarios)
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
        """
        Abre uma nova janela para permitir a seleção de cor para cada vértice
        individualmente do polígono selecionado.
        """
        poligono_selecionado = self._gerenciador_poligonos.poligono_selecionado
        
        if not poligono_selecionado:
            messagebox.showinfo("Nenhum Polígono Selecionado", "Por favor, selecione um polígono no modo 'Seleção' primeiro.")
            return

        # Cria uma nova janela (Toplevel) para a edição de cores
        dialogo_cores = tk.Toplevel(self.root)
        dialogo_cores.title("Editor de Cores dos Vértices")
        dialogo_cores.geometry("300x400")
        dialogo_cores.resizable(False, True)
        # Faz com que a janela de diálogo fique em foco
        dialogo_cores.grab_set()

        # Função que será chamada pelo botão para alterar a cor de um vértice específico
        def _mudar_cor_vertice(indice_vertice: int, label_preview: tk.Label):
            # Abre o seletor de cores
            
            cor_escolhida = colorchooser.askcolor(
                color=self._s_rgb_para_hex(poligono_selecionado.cor_vertices[indice_vertice]),
                title=f"Escolha a cor para o Vértice {indice_vertice + 1}"
            )
            
            # A cor_escolhida é uma tupla ((R, G, B), "#RRGGBB")
            if cor_escolhida and cor_escolhida[0]:
                cor_rgb = tuple(int(c) for c in cor_escolhida[0])
                cor_hex = cor_escolhida[1]

                # Atualiza a cor no modelo de dados do polígono
                poligono_selecionado.cor_vertices[indice_vertice] = cor_rgb
                
                # Atualiza a cor da caixa de preview na janela de diálogo
                label_preview.config(bg=cor_hex)
                self.renderizar_cena()

        # Cria uma linha na UI para cada vértice
        for i, vertice in enumerate(poligono_selecionado.vertices):
            frame_vertice = tk.Frame(dialogo_cores, bd=2, relief=tk.GROOVE)
            frame_vertice.pack(fill=tk.X, padx=5, pady=3)

            tk.Label(frame_vertice, text=f"Vértice {i + 1}").pack(side=tk.LEFT, padx=5)

            # Preview da cor atual
            cor_atual_hex = self._s_rgb_para_hex(poligono_selecionado.cor_vertices[i])
            preview = tk.Label(frame_vertice, text="    ", bg=cor_atual_hex, relief=tk.SUNKEN)
            preview.pack(side=tk.LEFT, padx=5)
            
            # Botão para mudar a cor, usando lambda para passar o índice correto
            tk.Button(
                frame_vertice, 
                text="Mudar Cor", 
                command=lambda index=i, p=preview: _mudar_cor_vertice(index, p)
            ).pack(side=tk.RIGHT, padx=5)

    def _aplicar_preenchimento_poligono(self):
        """Ativa o preenchimento para o polígono selecionado"""
        if self._gerenciador_poligonos.poligono_selecionado:
            self._gerenciador_poligonos.poligono_selecionado.preenchimento_ativado = not self._gerenciador_poligonos.poligono_selecionado.preenchimento_ativado
            self.renderizar_cena()
        else:
            messagebox.showinfo("Nenhum Polígono Selecionado", "Por favor, selecione um polígono no modo 'Seleção' primeiro.")

    def _remover_poligono_selecionado(self):
        """Remove o polígono atualmente selecionado"""
        if self._gerenciador_poligonos.remover_poligono_selecionado():
            self.renderizar_cena()
