from time import perf_counter

def algoritmo_fillpoly(app, poligono):
    """Algoritmo FillPoly com interpolação de cores (Gouraud Shading)."""

    # inicio = perf_counter() # Para calcular tempo de execução
    
    # ADquire os vertices e cores do poligono
    vertices = poligono.vertices
    cores = poligono.cor_vertices

    # Obtem o y_min e y_max do poligono na janela de animação
    y_min_poligono = int(min(y for (_, y) in vertices))
    y_max_poligono = int(max(y for (_, y) in vertices))
    
    Ns = y_max_poligono - y_min_poligono
    if Ns == 0:
        return # Polígono é uma linha horizontal

    num_vertices = len(vertices)

    # A lista de arestas armazenará tuplas no formato (x, r, g, b)
    # Cada elemento lista_arestas[i][j] é uma intersecção de uma scanline
    # com um aresta ou vértice do poligono
    lista_arestas = [[] for _ in range(Ns)]

    # 1. Construção da lista de arestas com cores interpoladas em Y
    for i in range(num_vertices):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % num_vertices]
        c1 = cores[i]
        c2 = cores[(i + 1) % num_vertices]

        y1, y2 = v1[1], v2[1]
        
        if y1 == y2: # Se é uma aresta horizontal
            continue

        # Garante que a aresta seja processada de cima para baixo (y1 < y2)
        if y1 > y2:
            v1, v2 = v2, v1
            c1, c2 = c2, c1
        
        x1, y1 = v1 # Pega as coordenas do vertice inicial
        x2, y2 = v2 # Pega as coordenas do vertice final
        r1, g1, b1 = c1 # Pega cores do vertice inicial
        r2, g2, b2 = c2 # Pega cores do vertice final

        # Calcula a taxa de variação de X em relação a Y
        delta_y = y2 - y1
        Tx = (x2 - x1) / delta_y
        
        # Calcula a taxa de variação de cada componente de cor em relação a Y
        dred_dy = (r2 - r1) / delta_y # Delta Red / Delta Y
        dgreen_dy = (g2 - g1) / delta_y # Delta Vermelho / Delta Y
        dblue_dy = (b2 - b1) / delta_y
        
        # Inicializa os valores para a interpolação
        x_atual = x1
        red_atual, green_atual, blue_atual = float(r1), float(g1), float(b1)

        y_inicial_abs = y1 - y_min_poligono
        y_final_abs = y2 - y_min_poligono

        for y in range(y_inicial_abs, y_final_abs):

            # Armazena a interseção X e a cor interpolada (R,G,B)
            lista_arestas[y].append((int(x_atual), int(red_atual), int(green_atual), int(blue_atual)))
            
            # Incrementa para a próxima scanline
            x_atual += Tx
            red_atual += dred_dy
            green_atual += dgreen_dy
            blue_atual += dblue_dy

    # 2. Preenchimento das scanlines com cores interpoladas em X
    for y in range(Ns):
        # Ordena as interseções pelo valor de X
        interseccoes = sorted(lista_arestas[y])
        
        for i in range(0, len(interseccoes), 2):
            # Pega o par de interseções que define o segmento horizontal
            ponto_inicial = interseccoes[i]
            ponto_final = interseccoes[i+1]

            x_inicial, red_inicial, green_inicial, blue_inicial = ponto_inicial
            x_final, red_final, green_final, blue_final = ponto_final

            # Converte para inteiros para o loop de pixels
            xi, xf = int(x_inicial), int(x_final)
            
            if xi >= xf:
                continue

            # Calcula a taxa de variação de cada cor em relação a X
            delta_x = x_final - x_inicial
            dred_dx = (red_final - red_inicial) / delta_x if delta_x != 0 else 0
            dgreen_dx = (green_final - green_inicial) / delta_x if delta_x != 0 else 0
            dblue_dx = (blue_final - blue_inicial) / delta_x if delta_x != 0 else 0

            # Inicializa a cor para o início do segmento horizontal
            cor_pixel_r, cor_pixel_g, cor_pixel_b = red_inicial, green_inicial, blue_inicial

            # Calcula o valro absoluto de y para pintar
            y_tela = y + y_min_poligono

            # Desenha a linha pixel a pixel
            for px in range(xi, xf):
                
                # Converte a cor float para int e depois para formato hexadecimal
                cor_hex = '#%02x%02x%02x' % (int(cor_pixel_r), int(cor_pixel_g), int(cor_pixel_b))

                # Usa o metodo create_line para criar uma linha de tamanho 1 por 1, ou seja, um pixel
                app._canvas.create_line(px, y_tela, px + 1, y_tela, fill=cor_hex)
                
                # Incrementa para o proximo pixel
                cor_pixel_r += dred_dx
                cor_pixel_g += dgreen_dx
                cor_pixel_b += dblue_dx
        
    # print(f"Preenchimento realizado em {perf_counter() - inicio}s")
        