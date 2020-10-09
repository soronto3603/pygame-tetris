import pygame
from pygame.locals import *
from typing import Type, List
import random

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('A bit Racey')
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
surface = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])

BLUE = (0,0,255)
BLOCK_SIZE = 10

crashed = False
clock = pygame.time.Clock()


BLOCK_PLAN_SIZE = 4
blockPlan = [
  [
    [
      [0, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 1, 1, 1],
      [0, 0, 0, 0],
    ],
    [
      [0, 0, 1, 0],
      [0, 0, 1, 0],
      [0, 1, 1, 0],
      [0, 0, 0, 0],
    ],
    [
      [0, 0, 0, 0],
      [1, 1, 1, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 0],
    ],
    [
      [0, 0, 0, 0],
      [0, 1, 1, 0],
      [0, 1, 0, 0],
      [0, 1, 0, 0],
    ]
  ],
  [
    [
      [0, 0, 0, 0],
      [0, 1, 1, 1],
      [0, 1, 0, 0],
      [0, 0, 0, 0],
    ],
    [
      [0, 1, 0, 0],
      [0, 1, 0, 0],
      [0, 1, 1, 0],
      [0, 0, 0, 0],
    ],
    [
      [0, 0, 0, 0],
      [0, 0, 1, 0],
      [1, 1, 1, 0],
      [0, 0, 0, 0],
    ],
    [
      [0, 0, 0, 0],
      [0, 1, 1, 0],
      [0, 0, 1, 0],
      [0, 0, 1, 0],
    ],
  ],
  [
    [
      [1, 0, 0, 0],
      [1, 0, 0, 0],
      [1, 0, 0, 0],
      [1, 0, 0, 0],
    ],
    [
      [1, 1, 1, 1],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
    ],
  ],
  [
    [
      [0, 0, 0, 0],
      [0, 1, 1, 0],
      [0, 1, 1, 0],
      [0, 0, 0, 0],
    ]
  ]
]

class Block:
  def __repr__(self):
    return f'{self.x}, {self.y}, {self.activation}'

  def __init__(self, x = (SCREEN_WIDTH / BLOCK_SIZE) / 2, y = 0):
    self.x = x
    self.y = y
    self.activation = True
    self.type = random.randint(0, 3)
    self.dir = 0

  def increaseY(self):
    self.y += 1

  def increaseX(self):
    self.x += 1

  def decreaseX(self):
    self.x -= 1

  def changeDirection(self):
    self.dir = (self.dir + 1) % len(blockPlan[self.type])

  def getNextPositions(self):
    return [[self.x + i, self.y + j + 1] for i in range(BLOCK_PLAN_SIZE) for j in range(BLOCK_PLAN_SIZE) if blockPlan[self.type][self.dir][j][i]]

  def getPositions(self):
    return [[self.x + i, self.y + j] for i in range(BLOCK_PLAN_SIZE) for j in range(BLOCK_PLAN_SIZE) if blockPlan[self.type][self.dir][j][i]]

  def turnOff(self):
    self.activation = False

  def turnOn(self):
    self.activation = True


class Tetris:
  blocks: List[Type[Block]] = []

  def __init__(self):
    self.blocks = [Block()]

  def run(self, key = None):
    if key == K_DOWN:
      pass

    blocks = [block for block in self.blocks if block.activation]
    for block in blocks:
      if key == K_UP:
        block.changeDirection()
      elif key == K_LEFT:
        block.decreaseX()
      elif key == K_RIGHT:
        block.increaseX()

      isCollision = False
      for [nextX, nextY] in block.getNextPositions():
        if nextY > (SCREEN_HEIGHT / BLOCK_SIZE) - 1:
          block.turnOff()
          self.blocks.append(Block())
          return

        for targetBlock in filter(lambda b: b != block, self.blocks):
          for [targetX, targetY] in targetBlock.getPositions():
            if nextX == targetX and nextY == targetY:
              block.turnOff()
              self.blocks.append(Block())
              return

      block.increaseY()

tetris = Tetris()
gameDisplay.blit(surface, (0, 0))
loopCounter = 0
while not crashed:
  loopCounter += 1
  pressedKey = None
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit(); #sys.exit() if sys is imported
    if event.type == pygame.KEYDOWN:
      pressedKey = event.key

  tetris.run(pressedKey)
  gameDisplay.fill((0, 0, 0))

  for block in tetris.blocks:
    for i in range(4):
      for j in range(4):
        if blockPlan[block.type][block.dir][i][j]:
          pygame.draw.rect(gameDisplay, BLUE, ((block.x + j) * BLOCK_SIZE, (block.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

  # pygame.display.flip()

  pygame.display.update()

  clock.tick(25)

pygame.quit()
quit()