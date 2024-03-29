import os
import sys
import pygame

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
STEP = 50
cols = 10
rows = 10
wr = WIDTH / cols
hr = HEIGHT / rows


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


FPS = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

        player_rect = pygame.Rect(pos_x, pos_y, wr - 3, hr - 3)
        x_, y_ = int(player_rect.centerx / wr), int(player_rect.centery / hr)
        x0, y0 = int(player_rect.left / wr), int(player_rect.top / hr)
        x1, y1 = int(player_rect.right / wr), int(player_rect.bottom / hr)

    def collide(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if pygame.sprite.spritecollideany(self, wall_group):
            self.rect.x -= x
            self.rect.y -= y
            return False
        print('ok')
        self.rect.x -= x
        self.rect.y -= y
        return True

    def move(self):
        if self.left_pressed and self.player_rect.x < self.x_ * wr + 2:
            if tile_images[self.x_][self.y0].walls[3] or tile_images[self.x_][self.y1].walls[3]:
                player.x = self.x_ * wr + 2
                self.left_pressed = False
            if self.y != self.y_ * hr + 2 and tile_images[self.x0][self.y0].walls[2]:
                self.x = self.x_ * wr + 2
                self.left_pressed = False

        if self.right_pressed and self.player_rect.x > self.x_ * wr + 2:
            if tile_images[self.x_][self.y0].walls[1] or tile_images[self.x_][self.y1].walls[1]:
                self.x = self.x_ * wr + 2
                self.right_pressed = False
            if self.y != self.y_ * hr + 2 and tile_images[self.x0 + 1][self.y0].walls[2]:
                self.x = self.x_ * wr + 2
                self.right_pressed = False

        if self.up_pressed and self.player_rect.y < self.y_ * hr + 2:
            if tile_images[self.x0][self.y_].walls[0] or tile_images[self.x1][self.y_].walls[0]:
                self.y = self.y_ * hr + 2
                self.up_pressed = False
            if self.x != self.x_ * wr + 2 and tile_images[self.x0][self.y0].walls[3]:
                self.y = self.y_ * hr + 2
                self.up_pressed = False

        if self.down_pressed and self.player_rect.y > self.y_ * hr + 2:
            if tile_images[self.x0][self.y_].walls[2] or tile_images[self.x1][self.y_].walls[2]:
                self.y = self.y_ * hr + 2
                self.down_pressed = False
            if self.x != self.x_ * wr + 2 and tile_images[self.x0][self.y0 + 1].walls[3]:
                self.y = self.y_ * hr + 2
                self.down_pressed = False


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y).add(wall_group)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Цель игры состоит в том, чтобы провести персонажа по",
                  "игровому миру, который представлен сеткой из плиток.",
                  "Игрок может перемещать персонажа, используя клавиши",
                  'со стрелками',
                  'Игра включает в себя различные препятствия',
                  'врагов, которые игрок должен преодолеть',
                  "Игрок может собирать предметы или бонусы,"
                  "которые могут помочь ему в путешествии."]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


start_screen()
running = True
player, level_x, level_y = generate_level(load_level('levelex.txt'))
camera = Camera()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.up_pressed = True
                if player.collide(0, -STEP):
                    player.rect.y -= STEP
            if event.key == pygame.K_DOWN:
                player.down_pressed = True
                if player.collide(0, STEP):
                    player.rect.y += STEP
            if event.key == pygame.K_LEFT:
                player.left_pressed = True
                if player.collide(-STEP, 0):
                    player.rect.x -= STEP
            if event.key == pygame.K_RIGHT:
                player.right_pressed = True
                if player.collide(STEP, 0):
                    player.rect.x += STEP

    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill(pygame.Color("black"))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
