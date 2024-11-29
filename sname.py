import curses
import random
import time


def game_loop(window, game_speed):
    """
    Função principal do jogo que controla o loop da cobra.

    Parâmetros:
    - window: Objeto curses para desenhar o jogo na janela do terminal.
    - game_speed: Tempo em milissegundos entre atualizações, controlando a velocidade.

    Fluxo:
    1. Configura a posição inicial da cobra e da fruta.
    2. Executa o loop do jogo:
    - Desenha a cobra, fruta e bordas.
    - Captura entrada do usuário para movimentar a cobra.
    - Verifica colisões (bordas, corpo da cobra e fruta).
    - Atualiza a pontuação e o estado do jogo.
    3. Finaliza ao detectar colisão, exibindo a pontuação final.

    Retorno:
    - Não retorna valores; controla a lógica e a exibição do jogo.
    """
    curses.curs_set(0)
    snake = [
        [12, 15],
        [11, 15],
        [10, 15],
        [9, 15],
        [8, 15],
        [7, 15],
        [6, 15],
    ]
    fruit = get_new_fruit(window=window)
    current_direction = curses.KEY_DOWN
    snake_ate_fruit = False
    score = 0

    # Loop do jogo
    while True:
        # Desenhar elementos
        draw_screen(window=window)
        draw_snake(snake=snake, window=window)
        draw_actor(actor=fruit, window=window, char=curses.ACS_DIAMOND)
        # Pegar input do usuário
        direction = get_new_direction(window=window, timeout=game_speed)
        if direction is None:
            direction = current_direction
        elif direction_is_opposite(direction=direction, current_direction=current_direction):
            direction = current_direction
        move_snake(snake=snake, direction=direction, snake_ate_fruit=snake_ate_fruit)
        # Checar final de jogo
        if snake_hit_border(snake=snake, window=window):
            break
        if snake_hit_itself(snake=snake):
            break
        # Checar colisão
        if snake_hit_fruit(snake=snake, fruit=fruit):
            score += 1
            snake_ate_fruit = True
            fruit = get_new_fruit(window=window)
        else:
            snake_ate_fruit = False
        # Atualizar direção atual
        current_direction = direction

    # Mensagem ao final do jogo
    finish_game(score=score, window=window)
def finish_game(score, window):
    """
    Função que exibe a mensagem de término do jogo.

    Parâmetros:
    - score: Inteiro representando a quantidade de frutas coletadas pelo jogador.
    - window: Objeto curses para desenhar a mensagem de finalização na janela do terminal.

    Fluxo:
    1. Calcula a posição central da mensagem na janela com base no tamanho da tela.
    2. Exibe a mensagem de "Você perdeu!" com o número de frutas coletadas.
    3. Aguarda 2 segundos antes de finalizar.

    Retorno:
    - Não retorna valores; apenas exibe a mensagem e pausa o programa brevemente.
    """
    height, width = window.getmaxyx()
    s = f'Você perdeu! Coletou {score} frutas!'
    x = int((width - len(s)) / 2)
    y = int(height / 2)
    window.addstr(y, x, s)
    window.refresh()
    time.sleep(2)
def get_new_fruit(window):
    """
    Função que gera uma nova posição para a fruta na tela.

    Parâmetros:
    - window: Objeto curses que representa a janela do terminal, usado para determinar os limites da tela.

    Fluxo:
    1. Obtém as dimensões da janela (altura e largura).
    2. Gera coordenadas aleatórias para a fruta dentro dos limites da tela.

    Retorno:
    - Uma lista contendo as coordenadas [y, x] da nova posição da fruta.
    """
    height, width = window.getmaxyx()
    return [random.randint(1, height-2), random.randint(1, width-2)]
def get_new_direction(window, timeout):
    """
    Função que captura a direção de movimento da cobra com base na entrada do usuário.

    Parâmetros:
    - window: Objeto curses que representa a janela do terminal, usado para capturar a entrada do teclado.
    - timeout: Tempo limite (em milissegundos) para aguardar a entrada do usuário antes de continuar a execução.

    Fluxo:
    1. Define o tempo limite para capturar a entrada do teclado.
    2. Lê a tecla pressionada pelo usuário.
    3. Verifica se a tecla corresponde a uma direção válida (setas do teclado).
    4. Retorna a direção capturada ou `None` se nenhuma direção válida for pressionada.

    Retorno:
    - O código da tecla correspondente à nova direção (KEY_UP, KEY_LEFT, KEY_DOWN, KEY_RIGHT) ou `None` se nenhuma direção válida for capturada.
    """
    window.timeout(timeout)
    direction = window.getch()
    if direction in [curses.KEY_UP, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_RIGHT]:
        return direction
    return None
def direction_is_opposite(direction, current_direction):
    """
    Função que verifica se a nova direção escolhida é oposta à direção atual.

    Parâmetros:
    - direction: Código da tecla representando a nova direção (KEY_UP, KEY_LEFT, KEY_DOWN, KEY_RIGHT).
    - current_direction: Código da tecla representando a direção atual.

    Fluxo:
    1. Verifica se a nova direção é oposta à direção atual:
    - UP é oposta a DOWN.
    - LEFT é oposta a RIGHT.
    - DOWN é oposta a UP.
    - RIGHT é oposta a LEFT.
    2. Retorna `True` se as direções forem opostas; caso contrário, retorna `False`.

    Retorno:
    - Booleano (`True` ou `False`) indicando se a nova direção é oposta à atual.
    """
    match direction:
        case curses.KEY_UP:
            return current_direction == curses.KEY_DOWN
        case curses.KEY_LEFT:
            return current_direction == curses.KEY_RIGHT
        case curses.KEY_DOWN:
            return current_direction == curses.KEY_UP
        case curses.KEY_RIGHT:
            return current_direction == curses.KEY_LEFT
def move_snake(snake, direction, snake_ate_fruit):
    """
    Função que movimenta a cobra na direção especificada.

    Parâmetros:
    - snake: Lista de coordenadas representando o corpo da cobra. O primeiro elemento é a cabeça.
    - direction: Código da tecla representando a direção do movimento (KEY_UP, KEY_LEFT, KEY_DOWN, KEY_RIGHT).
    - snake_ate_fruit: Booleano indicando se a cobra comeu uma fruta. 

    Fluxo:
    1. Cria uma nova cabeça da cobra, copiando a posição atual da cabeça.
    2. Move a nova cabeça na direção especificada.
    3. Insere a nova cabeça na frente da lista que representa a cobra.
    4. Remove o último segmento da cobra se ela não comeu uma fruta.

    Retorno:
    - Não retorna valores. A lista `snake` é modificada diretamente.
    """
    head = snake[0].copy()
    snake.insert(0, head)
    move_actor(actor=head, direction=direction)
    if not snake_ate_fruit:
        snake.pop()
def move_actor(actor, direction):
    """
    Função que move um ator (objeto com coordenadas) em uma direção especificada.

    Parâmetros:
    - actor: Lista representando as coordenadas [y, x] do ator.
    - direction: Código da tecla representando a direção do movimento (KEY_UP, KEY_LEFT, KEY_DOWN, KEY_RIGHT).

    Fluxo:
    1. Verifica a direção especificada:
    - KEY_UP: Decrementa a coordenada `y` para mover para cima.
    - KEY_LEFT: Decrementa a coordenada `x` para mover para a esquerda.
    - KEY_DOWN: Incrementa a coordenada `y` para mover para baixo.
    - KEY_RIGHT: Incrementa a coordenada `x` para mover para a direita.
    2. Atualiza as coordenadas do ator diretamente.

    Retorno:
    - Não retorna valores. As coordenadas do `actor` são modificadas diretamente.
    """
    match direction:
        case curses.KEY_UP:
            actor[0] -= 1
        case curses.KEY_LEFT:
            actor[1] -= 1
        case curses.KEY_DOWN:
            actor[0] += 1
        case curses.KEY_RIGHT:
            actor[1] += 1
def snake_hit_border(snake, window):
    """
    Função que verifica se a cobra colidiu com as bordas da janela.

    Parâmetros:
    - snake: Lista de coordenadas representando o corpo da cobra. O primeiro elemento é a cabeça.
    - window: Objeto curses que representa a janela do terminal, usado para determinar os limites da tela.

    Fluxo:
    1. Obtém a posição da cabeça da cobra (primeiro elemento da lista `snake`).
    2. Chama a função `actor_hit_border` para verificar se a cabeça da cobra colidiu com as bordas da janela.

    Retorno:
    - Booleano (`True` ou `False`) indicando se a cobra colidiu com as bordas.
    """
    head = snake[0]
    return actor_hit_border(actor=head, window=window)
def actor_hit_border(actor, window):
    """
    Função que verifica se um ator (objeto com coordenadas) colidiu com as bordas da janela.

    Parâmetros:
    - actor: Lista representando as coordenadas [y, x] do ator.
    - window: Objeto curses que representa a janela do terminal, usado para determinar os limites da tela.

    Fluxo:
    1. Obtém as dimensões da janela (`height` e `width`) usando `window.getmaxyx()`.
    2. Verifica:
    - Eixo vertical (`y`): Se o ator está fora dos limites superior (0) ou inferior (`height - 1`).
    - Eixo horizontal (`x`): Se o ator está fora dos limites esquerdo (0) ou direito (`width - 1`).
    3. Retorna `True` se o ator colidiu com qualquer borda; caso contrário, retorna `False`.

    Retorno:
    - Booleano (`True` ou `False`) indicando se o ator colidiu com as bordas.
    """
    height, width = window.getmaxyx()
    # EIXO VERTICAL
    if (actor[0] <= 0) or (actor[0] >= (height - 1)):
        return True
    # EIXO HORIZONTAL
    if (actor[1] <= 0) or (actor[1] >= (width - 1)):
        return True
    return False
def snake_hit_itself(snake):
    """
    Função que verifica se a cobra colidiu com o próprio corpo.

    Parâmetros:
    - snake: Lista de coordenadas representando o corpo da cobra. O primeiro elemento é a cabeça.

    Fluxo:
    1. Obtém a posição da cabeça da cobra (primeiro elemento da lista `snake`).
    2. Obtém o restante do corpo da cobra (todos os elementos após o primeiro).
    3. Verifica se a cabeça da cobra está presente no restante do corpo.

    Retorno:
    - Booleano (`True` ou `False`) indicando se a cobra colidiu com o próprio corpo.
    """
    head = snake[0]
    body = snake[1:]
    return head in body
def snake_hit_fruit(snake, fruit):
    """
    Função que verifica se a cobra colidiu com a fruta.

    Parâmetros:
    - snake: Lista de coordenadas representando o corpo da cobra. O primeiro elemento é a cabeça.
    - fruit: Lista representando as coordenadas [y, x] da fruta.

    Fluxo:
    1. Verifica se as coordenadas da fruta estão presentes na lista `snake`, indicando que a cobra comeu a fruta.

    Retorno:
    - Booleano (`True` ou `False`) indicando se a cobra colidiu com a fruta.
    """
    return fruit in snake
def draw_screen(window):
    """
    Função que desenha a tela do jogo.

    Parâmetros:
    - window: Objeto curses que representa a janela do terminal.

    Fluxo:
    1. Limpa a tela usando `window.clear()`.
    2. Adiciona uma borda ao redor da janela usando `window.border(0)`.

    Retorno:
    - Não retorna valores; a tela é desenhada diretamente no objeto `window`.
    """
    window.clear()
    window.border(0)
def draw_snake(snake, window):
    """
    Função que desenha a cobra na tela.

    Parâmetros:
    - snake: Lista de coordenadas representando o corpo da cobra. O primeiro elemento é a cabeça.
    - window: Objeto curses que representa a janela do terminal.

    Fluxo:
    1. Obtém a posição da cabeça da cobra (primeiro elemento da lista `snake`).
    2. Desenha a cabeça da cobra na tela usando o caractere "✴".
    3. Obtém as posições do corpo da cobra (restante da lista `snake`).
    4. Desenha cada parte do corpo da cobra na tela usando o caractere "✳".

    Retorno:
    - Não retorna valores; a cobra é desenhada diretamente no objeto `window`.
    """
    head = snake[0]
    body = snake[1:]
    draw_actor(actor=head, window=window, char="✴")
    for body_part in body:
        draw_actor(actor=body_part, window=window, char="✳")
def draw_actor(actor, window, char):
    """
    Função que desenha um ator (objeto com coordenadas) na tela.

    Parâmetros:
    - actor: Lista representando as coordenadas [y, x] do ator.
    - window: Objeto curses que representa a janela do terminal.
    - char: Caractere usado para representar o ator na tela.

    Fluxo:
    1. Utiliza `window.addch()` para desenhar o caractere na posição especificada pelas coordenadas do ator.

    Retorno:
    - Não retorna valores; o ator é desenhado diretamente no objeto `window`.
    """
    window.addch(actor[0], actor[1], char)
def select_difficulty():
    """
    Função que permite ao jogador selecionar a dificuldade do jogo.

    Fluxo:
    1. Define um dicionário `difficulty` que mapeia opções de dificuldade (1 a 5) para valores de velocidade (`game_speed`) em milissegundos.
    2. Entra em um loop solicitando ao jogador que escolha um nível de dificuldade.
    3. Verifica se a entrada do jogador está entre as opções válidas no dicionário:
    - Se válida, retorna o valor correspondente à velocidade (`game_speed`).
    - Se inválida, exibe uma mensagem de erro e solicita novamente.

    Retorno:
    - Inteiro representando o tempo em milissegundos entre as atualizações da tela (a velocidade do jogo).
    """
    difficulty = {
        '1': 1000,
        '2': 500,
        '3': 150,
        '4': 90,
        '5': 35,
    }
    while True:
        answer = input('Selecione a dificuldade de 1 a 5:')
        game_speed = difficulty.get(answer)
        if game_speed is not None:
            return game_speed
        print('Escolha a dificuldade de 1 a 5!')


if __name__ == '__main__':
    curses.wrapper(game_loop, game_speed=select_difficulty())
