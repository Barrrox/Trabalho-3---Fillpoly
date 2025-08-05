def algoritmo_fillpoly(app, poligono):
        """algoritmo FillPoly"""
        
        #inicialização
        vertices = poligono.vertices

        # Encontra os valores minimos e maximos de y do poligono
        y_min_poligono = min(y for (x,y) in vertices)
        y_max_poligono  = max(y for (x,y) in vertices)
        
        # Ns = Numero de scanlines - 1
        Ns = y_max_poligono - y_min_poligono 

        num_vertices = len(vertices)
        lista_arestas = [[] for _ in range(Ns)] # Cria a Lista de Arestas com Ns elementos

        # Construção da lista de arestas

        # Iterando para cada aresta
        for i in range(num_vertices):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % num_vertices]
            

            # Caso o segmento seja uma linha horizontal, pula
            if y1 == y2:
                continue

            # Caso o ponto 1 esteja abaixo do 2, inverte 
            if y1 > y2:
                x1, y1, x2, y2 = x2, y2, x1, y1

            # Tx = m inverso    
            Tx = (x2 - x1) / (y2 - y1) 
            x = x1 # salva para poder incrementar x depois
                
            # Pega o valor absoluto do inicio e fim da aresta
            y_inicial = y1 - y_min_poligono
            y_final = y2 - y_min_poligono

            # Itera sobre a aresta, incrementando x e 
            # capturando as intersecções das scanlines com a aresta
            for y in range(y_inicial, y_final):
                lista_arestas[y].append(x)                
                x += Tx

        # Para cada scanline
        for y in range(Ns):

            # Ordena as intersecções da aresta y
            interseccoes = sorted(lista_arestas[y])

            # Para cada par de valores x na linha
            for i in range(0, len(interseccoes), 2): 

                # Par (x_inicial, x_final)
                x_inicial = interseccoes[i]
                x_final = interseccoes[i+1]

                # Calcula o valor absoluto da scanline na janela
                y_tela = y + y_min_poligono

                # Desenha a linha
                app._canvas.create_line(
                    x_inicial, y_tela, x_final, y_tela,
                    fill="#%02x%02x%02x" % poligono.cor_rgb,
                    width=1
                    )