# Editor de Polígonos com Preenchimento Scanline

![Status](https://img.shields.io/badge/status-conclu%C3%ADdo-brightgreen)

Trabalho prático desenvolvido para a disciplina de Computação Gráfica, focado na criação de uma aplicação gráfica interativa para desenhar, manipular e preencher polígonos usando o algoritmo Scanline.

## 📜 Descrição

Esta aplicação permite que o usuário crie polígonos complexos de forma interativa em um canvas. O sistema possui modos distintos para desenho e seleção, permitindo a manipulação das formas criadas, como alterar a cor, aplicar preenchimento ou remover polígonos da cena.

O principal algoritmo de computação gráfica implementado é o **Preenchimento Scanline**, que converte a representação vetorial de um polígono em uma representação raster (pixels) para o preenchimento de sua área interna.

## ✨ Funcionalidades

- **Criação de Polígonos**: Desenhe polígonos complexos adicionando vértices com cliques do mouse.
- **Modo Dual**: Alterne facilmente entre o "Modo Desenho" para criar novas formas e o "Modo Seleção" para manipulá-las.
- **Seleção Inteligente**: Selecione polígonos clicando perto de suas arestas ou em seu interior. O polígono selecionado é destacado em vermelho.
- **Preenchimento com Scanline**: Aplique um preenchimento sólido ao polígono selecionado, demonstrando a implementação do algoritmo Scanline.
- **Seleção de Cor**: Altere a cor de preenchimento de qualquer polígono selecionado através de um seletor de cores nativo.
- **Manipulação de Cena**: Remova polígonos individualmente ou limpe toda a área de desenho.
- **Controle de Visualização**: Oculta ou exiba as arestas dos polígonos para focar apenas no preenchimento.
- **Interface Informativa**: Feedback em tempo real sobre o modo atual e as coordenadas do cursor.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3
- **Interface Gráfica**: Tkinter (biblioteca padrão do Python)
- **Dependências Externas**: Nenhuma. O projeto usa apenas as bibliotecas padrão do Python.

## 📂 Estrutura de Arquivos

O projeto foi organizado de forma modular para separar responsabilidades, seguindo um padrão semelhante ao Model-View-Controller.

-   `main.py`: Ponto de entrada da aplicação. Responsável por iniciar a janela principal e o loop de eventos.
-   `gui.py`: Contém a classe `AplicacaoRenderizacao`, que gerencia toda a interface gráfica, os widgets do Tkinter e os eventos de usuário (View/Controller).
-   `geometria.py`: Define as classes de dados do sistema, como `Ponto`, `Poligono` e o `GerenciadorPoligonos` (Model).
-   `algoritmos.py`: Isola as funções de lógica computacional mais complexas, como `preenchimento_scanline` e `contem_ponto`.

## 🚀 Como Executar

1.  Certifique-se de ter o **Python 3** instalado em sua máquina. A biblioteca Tkinter geralmente já vem inclusa na instalação padrão.
2.  Clone este repositório ou baixe todos os arquivos (`main.py`, `gui.py`, `geometria.py`, `algoritmos.py`) para um mesmo diretório.
3.  Abra um terminal ou prompt de comando e navegue até o diretório onde os arquivos foram salvos.
4.  Execute o seguinte comando:
    ```bash
    python main.py
    ```
5.  A janela da aplicação deverá abrir, e você poderá começar a usar.

## 🖱️ Como Usar

### Modo Desenho
-   **Clique com o botão esquerdo** para adicionar um vértice do polígono no canvas.
-   Após adicionar pelo menos 3 vértices, **clique com o botão direito** para finalizar e fechar o polígono.

### Modo Seleção
-   Clique no botão **"Alternar Modo"** para entrar no modo de seleção.
-   **Clique com o botão esquerdo** sobre um polígono para selecioná-lo. Sua borda ficará vermelha.

### Ações com um Polígono Selecionado
-   **Definir Cor**: Abre um seletor de cores. A cor escolhida será aplicada ao polígono selecionado.
-   **Preencher**: Ativa ou desativa o preenchimento Scanline para o polígono selecionado.
-   **Remover Polígono**: Exclui o polígono selecionado da cena.

## 🧠 Algoritmos Implementados

-   **Preenchimento de Polígonos (Scanline)**: O coração do trabalho. O algoritmo constrói uma Tabela de Arestas (Edge Table) e, para cada linha de varredura, mantém uma Tabela de Arestas Ativas (Active Edge Table) para determinar os pares de interseções `x` entre os quais a linha deve ser desenhada.
-   **Detecção de Ponto em Polígono**: Para a seleção, foram utilizadas duas técnicas combinadas:
    1.  **Distância Ponto-Segmento**: Verifica se o clique do mouse está próximo o suficiente de uma das arestas do polígono.
    2.  **Ray-Casting**: Traça um raio a partir do ponto do clique e conta quantas arestas ele cruza para determinar se o ponto está dentro ou fora da área do polígono.

## 👨‍💻 Autor

**[Seu Nome Completo Aqui]**

