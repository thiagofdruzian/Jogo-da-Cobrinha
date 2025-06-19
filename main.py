import os
import random
import time
import threading
import sys

try:
    import msvcrt  # Windows
except ImportError:
    import termios
    import tty
    import select


class SnakeGame:
    def __init__(self, width=20, height=20, delay=0.1):
        self.width = width
        self.height = height
        self.delay = delay
        self.score = 0
        self.snake = [(width // 2, height // 2)]
        self.direction = None
        self.food = self.place_food()
        self.game_over = False

    def place_food(self):
        while True:
            pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if pos not in self.snake:
                return pos

    def draw(self):
        os.system("cls" if os.name == "nt" else "clear")
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if (x, y) == self.snake[0]:
                    row += "O"
                elif (x, y) in self.snake:
                    row += "o"
                elif (x, y) == self.food:
                    row += "*"
                else:
                    row += " "
            print(f"|{row}|")
        print("-" * (self.width + 2))
        print(f"Pontuação: {self.score}")
        print("Controles: W A S D | Sair: X")

    def change_direction(self, new_dir):
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if self.direction != opposites.get(new_dir):
            self.direction = new_dir

    def move(self):
        if not self.direction:
            return

        x, y = self.snake[0]
        if self.direction == "UP":
            y -= 1
        elif self.direction == "DOWN":
            y += 1
        elif self.direction == "LEFT":
            x -= 1
        elif self.direction == "RIGHT":
            x += 1

        new_head = (x, y)

        if (
            x < 0 or x >= self.width or
            y < 0 or y >= self.height or
            new_head in self.snake
        ):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.food = self.place_food()
        else:
            self.snake.pop()

    def run(self):
        def key_listener():
            while not self.game_over:
                key = get_key()
                if key in ("w", "W"):
                    self.change_direction("UP")
                elif key in ("s", "S"):
                    self.change_direction("DOWN")
                elif key in ("a", "A"):
                    self.change_direction("LEFT")
                elif key in ("d", "D"):
                    self.change_direction("RIGHT")
                elif key in ("x", "X"):
                    self.game_over = True

        threading.Thread(target=key_listener, daemon=True).start()

        while not self.game_over:
            self.draw()
            self.move()
            time.sleep(self.delay)

        self.draw()
        print("\nFim de jogo! Pontuação final:", self.score)


def get_key():
    if os.name == "nt":
        return msvcrt.getch().decode("utf-8")
    else:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            if select.select([fd], [], [], 0.1)[0]:
                return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ""


def escolher_dificuldade():
    print("Escolha a dificuldade:")
    print("1 - Fácil")
    print("2 - Médio")
    print("3 - Difícil")

    while True:
        op = input("Opção: ").strip()
        if op == "1":
            return 0.2
        elif op == "2":
            return 0.1
        elif op == "3":
            return 0.05
        else:
            print("Opção inválida.")


def main():
    while True:
        delay = escolher_dificuldade()
        jogo = SnakeGame(delay=delay)
        jogo.run()

        resp = input("\nDeseja jogar novamente? (s/n): ").strip().lower()
        if resp != "s":
            print("Até a próxima!")
            break


if __name__ == "__main__":
    main()
