# Pysnake: Jogo da Cobrinha

Este projeto, **Pysnake**, foi desenvolvido como um exercício para treinar lógica de programação utilizando Python. Ele recria o clássico jogo da cobrinha, onde o jogador controla o movimento da cobra para comer frutas e evitar colisões consigo mesma ou com as bordas.

---

## Tecnologias Utilizadas

- **Linguagem**: Python 3
- **Bibliotecas**: `curses` para manipulação da interface no terminal
- **Base**: Pequeno curso de lógica de programação na plataforma **Asimov**

---

## Funcionalidades

- Movimentação da cobra com as setas do teclado.
- Geração aleatória de frutas.
- Sistema de pontuação baseado nas frutas coletadas.
- Opção de seleção de dificuldade, ajustando a velocidade do jogo.
- Detecção de colisões com as bordas ou com o corpo da cobra.
- Exibição de mensagem ao final com a pontuação alcançada.

---

## Como Funciona

1. O jogador controla a cobra utilizando as setas do teclado.
2. O objetivo é comer o máximo de frutas possível, sem colidir com as bordas ou consigo mesma.
3. Cada fruta coletada aumenta o tamanho da cobra e incrementa a pontuação.
4. A dificuldade selecionada no início define a velocidade da cobra.

---

## Como Jogar

### Pré-requisitos
- Ter Python 3 instalado no sistema.

### Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/vinicq/Pysnake-cobrinha.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd pysnake
   ```
3. Execute o jogo:
   ```bash
   python pysnake.py
   ```

### Controles
- Use as **setas do teclado** para mover a cobra.

---

## Estrutura do Código

1. **game_loop**: Função principal que controla o jogo.
2. **get_new_fruit**: Gera coordenadas aleatórias para a fruta.
3. **move_snake**: Atualiza a posição da cobra com base na direção escolhida.
4. **snake_hit_border** e **snake_hit_itself**: Detectam colisões que encerram o jogo.
5. **select_difficulty**: Permite ao jogador escolher a dificuldade do jogo.

---

## Sobre o Desenvolvedor

- **Nome**: Vinicius Queiroz
- **E-mail**: [vinicq@gmail.com](mailto:vinicq@gmail.com)

---

## Licença

Este projeto foi desenvolvido para fins de estudo e prática de lógica de programação. Sinta-se livre para utilizá-lo, modificá-lo e distribuí-lo.

---