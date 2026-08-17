import os

try:
    default_pygame_support_prompt = os.environ['PYGAME_HIDE_SUPPORT_PROMPT']
except KeyError:
    pass
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = default_pygame_support_prompt
except NameError:
    os.environ.pop('PYGAME_HIDE_SUPPORT_PROMPT')

import random
import sys

def find_real_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

def max_at_value(value: float, max_value: float):
    if value > max_value:
        return max_value
    return value

SCREEN_WIDTH: int = 512
SCREEN_HEIGHT: int = 512

width_scaling = SCREEN_WIDTH / 128
height_scaling = SCREEN_HEIGHT / 128

version = 0.3

pygame.init()
pygame.display.set_caption(f'Meteor Shooter {version}')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.SysFont('Arial', 36)

ship = {
    'image': pygame.image.load(find_real_path('assets/ship.png'))
}

ship['width'] = ship['image'].get_width() * width_scaling
ship['height'] = ship['image'].get_height() * height_scaling
ship['image'] = pygame.transform.scale(ship['image'],
                                       (ship['width'],
                                        ship['height']))
ship['x'] = SCREEN_WIDTH // 2 - ship['width'] // 2
ship['y'] = SCREEN_HEIGHT - ship['height']
ship['mask'] = pygame.mask.from_surface(ship['image'].convert_alpha())
ship['speed_x'] = 0

asteroid = {
    'image': pygame.image.load(find_real_path('assets/asteroid.png')),
}
asteroid['width'] = asteroid['image'].get_width() * width_scaling
asteroid['height'] = asteroid['image'].get_height() * height_scaling
asteroid['x'] = random.randint(0, int(SCREEN_WIDTH - asteroid['width']))
asteroid['y'] = -asteroid['height']
asteroid['image'] = pygame.transform.scale(asteroid['image'],
                                           (asteroid['width'],
                                            asteroid['height']))
asteroid['mask'] = pygame.mask.from_surface(asteroid['image'].convert_alpha())

lasers = {
    'image': pygame.image.load(find_real_path('assets/laser.bmp')),
    'entities': []
}
lasers['image'] = pygame.transform.scale(lasers['image'],
                                         (lasers['image'].get_width() * width_scaling,
                                          lasers['image'].get_height() * height_scaling))
lasers['width'] = lasers['image'].get_width()
lasers['height'] = lasers['image'].get_height()
lasers['mask'] = pygame.mask.from_surface(lasers['image'].convert_alpha())

score = 0
meteors_shot = 0
score_multiplier = 1
ASTEROID_BASE_SPEED = 0.5
ASTEROID_SPEED_ACCELERATION = 0.05
max_value = 6.5
over_max_value = False
asteroid['speed_y'] = max_at_value((ASTEROID_BASE_SPEED + meteors_shot / 10 * ASTEROID_SPEED_ACCELERATION) * height_scaling, max_value)

FPS = 50
game_over = False
running = True
game_over_cause = 'error'
a = None
while running:
    if not game_over:
        # game over detection
        if ship['mask'].overlap(asteroid['mask'],
                                (asteroid['x'] - ship['x'],
                                 asteroid['y'] - ship['y'])) is not None:
            game_over = True
            game_over_cause = 'Collided with the meteor'
        elif asteroid['y'] > SCREEN_HEIGHT:
            game_over = True
            game_over_cause = 'Meteor went off-screen'
        
        # destroy asteroids
        for i in range(len(lasers['entities'])):
            if asteroid['mask'].overlap(lasers['mask'],
                                        (lasers['entities'][i]['x'] - asteroid['x'],
                                         lasers['entities'][i]['y'] - asteroid['y'])):
                score += score_multiplier * 1
                meteors_shot += 1
                if meteors_shot == 40:
                    score_multiplier = 5 / 4
                elif meteors_shot == 65:
                    score_multiplier = 3 / 2
                elif meteors_shot == 100:
                    score_multiplier = 2
                
                if not over_max_value:
                    asteroid['speed_y'] = max_at_value((ASTEROID_BASE_SPEED + meteors_shot * ASTEROID_SPEED_ACCELERATION) * height_scaling, max_value)
                if asteroid['speed_y'] == max_value:
                    over_max_value = True
                lasers['entities'][i]['destroyed'] = True
                asteroid['x'] = random.randint(0,
                                               int(SCREEN_WIDTH - asteroid['width']))
                asteroid['y'] = -asteroid['height']
        
        # move lasers
        for i in range(len(lasers['entities'])):
            lasers['entities'][i]['y'] -= 4
            if lasers['entities'][i]['y'] < -lasers['height']:
                lasers['entities'][i]['destroyed'] = True
        # destroy lasers
        destroyed_lasers_exist = True
        while destroyed_lasers_exist and len(lasers['entities']) > 0:
            for i in range(len(lasers['entities'])):
                if lasers['entities'][i]['destroyed']:
                    lasers['entities'].pop(i)
                    break
                elif i == len(lasers['entities']) - 1:
                    destroyed_lasers_exist = False
    
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                lasers['entities'].append({
                    'x': ship['x'] + (ship['width'] // 2) - (lasers['width'] // 2),
                    'y': SCREEN_HEIGHT - ship['height'] - lasers['height'],
                    'destroyed': False
                })
            if event.key == pygame.K_r and game_over:
                score = 0
                meteors_shot = 0
                score_multiplier = 1
                ASTEROID_BASE_SPEED = 0.5
                ASTEROID_SPEED_ACCELERATION = 0.05
                max_value = 6.5
                over_max_value = False
                ship['x'] = SCREEN_WIDTH // 2 - ship['width'] // 2
                asteroid['x'] = random.randint(0,
                                               int(SCREEN_WIDTH - asteroid['width']))
                asteroid['y'] = -asteroid['height']
                asteroid['speed_y'] = max_at_value((ASTEROID_BASE_SPEED + meteors_shot / 10 * ASTEROID_SPEED_ACCELERATION) * height_scaling, max_value)
                game_over_cause = 'error'
                game_over = False
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            if keys[pygame.K_LEFT]:
                ship['speed_x'] -= 1
            if keys[pygame.K_RIGHT]:
                ship['speed_x'] += 1
        else:
            if ship['speed_x'] > 0:
                if ship['speed_x'] - 1 > 0:
                    ship['speed_x'] -= 1
                else:
                    ship['speed_x'] = 0
            else:
                if ship['speed_x'] + 1 < 0:
                    ship['speed_x'] += 1
                else:
                    ship['speed_x'] = 0
        
        # move ship
        if ship['x'] + ship['speed_x'] < 0:
            ship['x'] = 0
            ship['speed_x'] = 0
        elif ship['x'] + ship['speed_x'] > SCREEN_WIDTH - ship['width']:
            ship['x'] = SCREEN_WIDTH - ship['width']
            ship['speed_x'] = 0
        else:
            ship['x'] += ship['speed_x']
        
        # move asteroid
        asteroid['y'] += asteroid['speed_y']
    
    # render the scene
    screen.fill((0, 0, 0))
    for i in lasers['entities']:
        screen.blit(lasers['image'], (i['x'], i['y']))
    screen.blit(ship['image'], (ship['x'], ship['y']))
    screen.blit(asteroid['image'], (asteroid['x'], asteroid['y']))
    if score % 1 == 0:
        score_to_display = int(score)
    elif score % 0.1 == 0:
        score_to_display = round(score, 1)
    else:
        score_to_display = round(score, 2)
    score_text = font.render(f'Score: {score_to_display}',
                             True,
                             (255, 255, 255))
    screen.blit(score_text, (0, 0))
    
    if game_over:
        game_over_text = font.render('Game Over!', True, (255, 255, 255))
        screen.blit(game_over_text,
                    (int(SCREEN_WIDTH / 2 - game_over_text.get_width() / 2),
                     int(SCREEN_HEIGHT / 2 - game_over_text.get_height() * 2)))
        game_over_cause_text = font.render(game_over_cause,
                                           True,
                                           (255, 255, 255))
        screen.blit(game_over_cause_text,
                    (SCREEN_WIDTH // 2 - game_over_cause_text.get_width() // 2,
                     SCREEN_HEIGHT // 2 - game_over_cause_text.get_height()))
        retry_text = font.render('Press R to retry', True, (255, 255, 255))
        screen.blit(retry_text,
                    (SCREEN_WIDTH // 2 - retry_text.get_width() // 2,
                     SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

pygame.quit()
