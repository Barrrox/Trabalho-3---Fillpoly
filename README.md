# Projeto FillPoly com Sombreamento de Gouraud

Trabalho da disciplina de Computação Gráfica - Ciência da Computação, Unioeste, Campus Cascavel (2025).

**Autores:** Gabriel Merline, Leonardo Royer, Matheus Barros, Monique Barros

## Visão Geral do Projeto

Esta é uma aplicação gráfica interativa desenvolvida em Python com a biblioteca `tkinter`. O objetivo do projeto é demonstrar a implementação e o funcionamento do algoritmo de preenchimento de polígonos **Scanline**, com a adição de **sombreamento de Gouraud** para permitir a interpolação de cores suaves entre os vértices.

## Como Executar

Para executar o projeto, basta baixar a pasta do projeto e ter o Python 3 instalado.

```bash
# Navegue até a pasta do projeto
cd /caminho/para/o/projeto

# Execute o arquivo main.py
python main.py
```

A biblioteca tkinter é usada para apresentar a interface do projeto e é uma biblioteca nativa do python, porém algumas versões do Ubuntu não instalam ele por padrão com o python. Caso precise você pode instalá-lo com o comando:

```bash
sudo apt-get install python3-tk
```



## Funcionalidades Principais

  - **Desenho de Polígonos**: Crie polígonos clicando com o botão esquerdo para adicionar vértices e com o botão direito para fechar a forma.
  - **Modos de Interação**: Clicando no botão **Modo Desenho/Seleção** Alterne entre o modo de "Desenho" para criar novas formas e "Seleção" para manipular polígonos existentes.
  - **Preenchimento com Sombreamento de Gouraud**: Aplique um preenchimento suave que interpola as cores definidas nos vértices.
  - **Editor de Cores por Vértice**: Para qualquer polígono selecionado, é possível abrir um diálogo para definir uma cor RGB específica para cada um de seus vértices.
  - **Manipulação de Cena**: Funções para limpar todo o canvas, remover um polígono selecionado e alternar a visibilidade das arestas.

## Tutorial rápido

Passo a passo para desenhar e preencher um poligono:

1. Execute o arquivo `main.py`
2. No espaço de desenho, clique com o botão esquedo para adicionar pontos, formando arestas. Para fechar o polígono, clique com o botão direito.
3. Clique no botão `Modo Desenho/Seleção` para trocar para o modo de seleção
4. Clique dentro do poligono desejado para selecioná-lo.
5. Clique no botão `Definir Cor` e escolha as cores de cada vértice do poligono. Feche a janela de escolha de cor.
6. Clique no botão `Aplicar Preenchimento` e veja o resultado.

## Estrutura do Projeto

O código está organizado de forma modular para separar as responsabilidades:

  - `main.py`: Ponto de entrada da aplicação. Inicializa o `tkinter` e a classe principal `App`.
  - `interface.py`: Contém a classe `App`, a qual contém a lógica da interface gráfica (View e Controller), gerenciamento de eventos de mouse e teclado, e a estrutura dos botões.
  - `geometria.py`: Define as classes do modelo de dados (`Poligono`, `GerenciadorPoligonos`), que armazenam o estado da cena (vértices, cores, seleção).
  - `fillpoly.py`: Contém a implementação do algoritmo de preenchimento `scanline` com a lógica de interpolação de cores (Gouraud).


## Detalhes da Implementação

### Algoritmo de Preenchimento (Scanline)

O `fillpoly.py` implementa o algoritmo **FillPoly**. O processo consiste em:

1.  Construir uma tabela de arestas (`lista_arestas`) que armazena, para cada linha de varredura (`scanline`) horizontal, as informações das arestas do polígono que a cruzam.
2.  Para cada `scanline`, as interseções são ordenadas pelo seu valor X.
3.  Aplicando a **regra par-ímpar**, os pixels entre cada par de interseções são preenchidos.

### Sombreamento de Gouraud

O sombreamento suave é obtido através de uma interpolação linear dupla:

1.  **Interpolação em Y**: Ao percorrer as arestas para construir a tabela, as cores RGB são interpoladas verticalmente.
2.  **Interpolação em X**: Ao preencher uma `scanline`, as cores das interseções (obtidas na etapa anterior) são interpoladas horizontalmente para colorir cada pixel no segmento.

## Limitações e Possíveis Melhorias Futuras

  - **Polígonos Não Convexos**: A implementação atual do `fillpoly.py` não lida corretamente com todos os casos de vértices em polígonos côncavos, o que pode gerar artefatos visuais no preenchimento de algumas formas.
  - **Eficiência de Renderização**: A função `renderizar_cena` é chamada a cada interação, limpando e redesenhando toda a cena do zero. Isso é ineficiente e pode ser otimizado com técnicas de **cache**, como armazenar o preenchimento de cada polígono em uma imagem separada (*off-screen buffer*) ou gerenciar os objetos do canvas com *tags* para atualizações seletivas.
