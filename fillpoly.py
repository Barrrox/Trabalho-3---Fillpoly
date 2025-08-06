def algoritmo_fillpoly(app, poligono):
    """Algoritmo FillPoly com interpolação de cores (Gouraud Shading)."""
    
    vertices = poligono.vertices
    cores = poligono.cor_vertices

    y_min_poligono = int(min(y for (x, y) in vertices))
    y_max_poligono = int(max(y for (x, y) in vertices))
    
    Ns = y_max_poligono - y_min_poligono
    if Ns == 0:
        return # Polígono é uma linha horizontal

    num_vertices = len(vertices)
    # A lista de arestas agora armazenará tuplas: (x, r, g, b)
    lista_arestas = [[] for _ in range(Ns)]

    # --- 1. Construção da lista de arestas com cores interpoladas em Y ---
    for i in range(num_vertices):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % num_vertices]
        c1 = cores[i]
        c2 = cores[(i + 1) % num_vertices]

        y1, y2 = v1[1], v2[1]
        
        if y1 == y2:
            continue

        # Garante que a aresta seja processada de cima para baixo (y1 < y2)
        if y1 > y2:
            v1, v2 = v2, v1
            c1, c2 = c2, c1
        
        x1, y1 = v1
        x2, y2 = v2
        r1, g1, b1 = c1 # Pega cores do vertice inicial
        r2, g2, b2 = c2 # Pega cores do vertice final

        # Calcula a taxa de variação de X em relação a Y
        delta_y = y2 - y1
        Tx = (x2 - x1) / delta_y
        
        # Calcula a taxa de variação de cada componente de cor em relação a Y
        dr_dy = (r2 - r1) / delta_y
        dg_dy = (g2 - g1) / delta_y
        db_dy = (b2 - b1) / delta_y
        
        # Inicializa os valores para a interpolação
        x_atual = x1
        r_atual, g_atual, b_atual = float(r1), float(g1), float(b1)

        y_inicial_abs = y1 - y_min_poligono
        y_final_abs = y2 - y_min_poligono

        for y in range(y_inicial_abs, y_final_abs):
            # Armazena a interseção X e a cor interpolada (R,G,B)
            lista_arestas[y].append((x_atual, r_atual, g_atual, b_atual))
            
            # Incrementa para a próxima scanline
            x_atual += Tx
            r_atual += dr_dy
            g_atual += dg_dy
            b_atual += db_dy

    # --- 2. Preenchimento das scanlines com cores interpoladas em X ---
    for y in range(Ns):
        # Ordena as interseções pelo valor de X
        interseccoes = sorted(lista_arestas[y])

        for i in range(0, len(interseccoes), 2):
            # Pega o par de interseções que define o segmento horizontal
            p_inicial = interseccoes[i]
            p_final = interseccoes[i+1]

            x_inicial, r_inicial, g_inicial, b_inicial = p_inicial
            x_final, r_final, g_final, b_final = p_final

            # Converte para inteiros para o loop de pixels
            xi, xf = int(x_inicial), int(x_final)
            
            if xi >= xf:
                continue

            # Calcula a taxa de variação de cada cor em relação a X
            delta_x = x_final - x_inicial
            dr_dx = (r_final - r_inicial) / delta_x if delta_x != 0 else 0
            dg_dx = (g_final - g_inicial) / delta_x if delta_x != 0 else 0
            db_dx = (b_final - b_inicial) / delta_x if delta_x != 0 else 0

            # Inicializa a cor para o início do segmento horizontal
            cor_pixel_r, cor_pixel_g, cor_pixel_b = r_inicial, g_inicial, b_inicial

            y_tela = y + y_min_poligono

            # Desenha a linha pixel a pixel
            for px in range(xi, xf):
                # Converte a cor float para int e depois para formato hexadecimal
                try:
                    cor_hex = '#%02x%02x%02x' % (int(cor_pixel_r), int(cor_pixel_g), int(cor_pixel_b))
                except ValueError:
                    # Um fallback caso a interpolação saia um pouco dos limites 0-255
                    cor_hex = '#000000'

                # Desenha o pixel
                app._canvas.create_line(px, y_tela, px + 1, y_tela, fill=cor_hex)
                
                # Incrementa para o proximo pixel
                cor_pixel_r += dr_dx
                cor_pixel_g += dg_dx
                cor_pixel_b += db_dx
        