import pygame
import random
import time


class Sudoku:
    def __init__(self):
        file = open("sudoku.txt", "r")
        data = file.readlines()
        file.close()
        amount = len(data) // 10
        choice = random.randint(0, amount - 1)
        data = data[choice * 10 + 1: (choice + 1) * 10]
        self.data = [[y for y in x.strip("\n")] for x in data]
        for line in self.data:
            print(line)
        for y in range(len(self.data)):
            for x in range(len(self.data[y])):
                if data[y][x] == "0":
                    self.data[y][x] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                else:
                    self.data[y][x] = int(self.data[y][x])
        self.counter = 0

    def do_horizontal_based_eliminiation(self):
        for y in range(len(self.data)):
            in_row = set()
            for x in range(len(self.data[y])):
                if isinstance(self.data[y][x], int):
                    in_row.add(self.data[y][x])
            for x in range(len(self.data[y])):
                if isinstance(self.data[y][x], list):
                    for el in in_row:
                        if el in self.data[y][x]:
                            self.data[y][x].remove(el)

    def do_vertical_based_eliminiation(self):
        for x in range(len(self.data[0])):
            in_column = set()
            for y in range(len(self.data)):
                if isinstance(self.data[y][x], int):
                    in_column.add(self.data[y][x])
            for y in range(len(self.data)):
                if isinstance(self.data[y][x], list):
                    for el in in_column:
                        if el in self.data[y][x]:
                            self.data[y][x].remove(el)

    def do_box_based_elimination(self):
        for yb in range(3):
            for xb in range(3):
                in_box = set()
                for y in range(3):
                    for x in range(3):
                        if isinstance(self.data[yb * 3 + y][xb * 3 + x], int):
                            in_box.add(self.data[yb * 3 + y][xb * 3 + x])
                for y in range(3):
                    for x in range(3):
                        if isinstance(self.data[yb * 3 + y][xb * 3 + x], list):
                            for el in in_box:
                                if el in self.data[yb * 3 + y][xb * 3 + x]:
                                    self.data[yb * 3 + y][xb * 3 + x].remove(el)

    def do_collapse(self):
        for y in range(len(self.data)):
            for x in range(len(self.data[y])):
                if isinstance(self.data[y][x], list) and len(self.data[y][x]) == 1:
                    self.data[y][x] = self.data[y][x][0]

    def do_solve_step(self):
        possibilites = []
        possibilites.append(self.do_horizontal_based_eliminiation)
        possibilites.append(self.do_vertical_based_eliminiation)
        possibilites.append(self.do_box_based_elimination)
        possibilites.append(self.do_collapse)
        possibilites[self.counter % len(possibilites)]()
        self.counter += 1


class GUI:
    def __init__(self):
        pygame.init()
        self.small_square_length = 25
        self.small_line_width = 1
        self.square_length = self.small_square_length * 3 + self.small_line_width * 2
        self.normal_line_width = 4
        self.thick_line_width = 10
        self.large_box_dim = self.square_length * 3 + self.thick_line_width + 2 * self.normal_line_width
        self.total_x = 3 * self.large_box_dim + self.thick_line_width
        self.total_y = self.total_x
        self.screen = pygame.display.set_mode((self.total_x, self.total_y))
        self.running = True
        self.background_colour = (255, 255, 255)
        self.number_colour = (255, 0, 0)
        self.line_colour = (0, 0, 0)
        self.game = Sudoku()

    def run(self):
        while self.running:
            self.get_input()
            self.compute()
            self.render()
            time.sleep(0.5)

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.QUIT:
                    self.running = False
                if event.key == pygame.K_h:
                    self.game.do_horizontal_based_eliminiation()
                if event.key == pygame.K_v:
                    self.game.do_vertical_based_eliminiation()
                if event.key == pygame.K_b:
                    self.game.do_box_based_elimination()
                if event.key == pygame.K_c:
                    self.game.do_collapse()

    def compute(self):
        self.game.do_solve_step()

    def render(self):
        self.screen.fill(self.background_colour)
        self.render_thick_lines()
        self.render_normal_lines()
        self.render_known_numbers()
        self.render_guesses()
        pygame.display.update()

    def render_thick_lines(self):
        for i in range(4):
            pygame.draw.rect(self.screen, self.line_colour, (i * self.large_box_dim, 0, self.thick_line_width, self.total_y))
            pygame.draw.rect(self.screen, self.line_colour, (0, i * self.large_box_dim, self.total_x, self.thick_line_width))

    def render_normal_lines(self):
        for i in range(6):
            large_count = i // 2
            distance = self.large_box_dim * large_count + self.thick_line_width + self.square_length + (i % 2) * (self.normal_line_width + self.square_length)
            pygame.draw.rect(self.screen, self.line_colour, (distance, 0, self.normal_line_width, self.total_y))
            pygame.draw.rect(self.screen, self.line_colour, (0, distance, self.total_x, self.normal_line_width))

    def square_coord_to_pixel(self, square_coord):
        ret = self.thick_line_width
        box_amount = square_coord // 3
        in_box_amount = square_coord % 3
        ret += self.large_box_dim * box_amount
        ret += (self.square_length + self.normal_line_width) * in_box_amount
        return ret

    def render_known_numbers(self):
        font = pygame.font.Font(None, 36)
        numbers = []
        for i in range(1, 10):
            number = font.render(str(i), True, self.number_colour, self.background_colour)
            rescaled = pygame.transform.scale(number, (self.square_length, self.square_length))
            numbers.append(rescaled)
        for y in range(len(self.game.data)):
            for x in range(len(self.game.data[y])):
                to_render = self.game.data[y][x]
                if isinstance(to_render, list):
                    continue
                x_coord = self.square_coord_to_pixel(x)
                y_coord = self.square_coord_to_pixel(y)
                text_pic = numbers[self.game.data[y][x] - 1]
                self.screen.blit(text_pic, (x_coord, y_coord))

    def render_guesses(self):
        font = pygame.font.Font(None, 36)
        numbers = []
        for i in range(1, 10):
            number = font.render(str(i), True, self.number_colour, self.background_colour)
            rescaled = pygame.transform.scale(number, (self.small_square_length, self.small_square_length))
            numbers.append(rescaled)
        for y in range(len(self.game.data)):
            for x in range(len(self.game.data[y])):
                to_render = self.game.data[y][x]
                if isinstance(to_render, int):
                    continue
                for el in self.game.data[y][x]:
                    x_coord = self.square_coord_to_pixel(x) + self.small_square_length * ((el - 1) % 3)
                    y_coord = self.square_coord_to_pixel(y) + self.small_square_length * ((el - 1) // 3)
                    text_pic = numbers[el - 1]
                    self.screen.blit(text_pic, (x_coord, y_coord))


def main():
    gui = GUI()
    gui.run()


if __name__ == '__main__':
    main()
