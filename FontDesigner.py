#!/usr/bin/env python3
import pygame

pygame.init()
pygame.display.set_caption("FontDesigner")
screen = pygame.display.set_mode((800, 500))

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_LIGHTRED = (255, 102, 102)
COLOR_GRAY = (204, 204, 204)

savedFonts16 = []
savedFonts32 = []
fontChars = "01235456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,/\'\""

def getBlankCharacter16():
    character = []
    for y in range(0, 16):
        row = []
        for x in range(0, 16):
            row.append(0)
        character.append(row)
    return character

def getBlankCharacter32():
    character = []
    for y in range(0, 32):
        row = []
        for x in range(0, 32):
            row.append(0)
        character.append(row)
    return character

# Init fonts
for i in range(0, len(fontChars)):
    savedFonts16.append(getBlankCharacter16())
    savedFonts32.append(getBlankCharacter32())

running = True
while running:
    screen.fill(COLOR_WHITE)

    # Split up left side (32x32 font)
    pygame.draw.rect(screen, COLOR_LIGHTRED, pygame.Rect(16, 66, 24, 384)) #left
    pygame.draw.rect(screen, COLOR_LIGHTRED, pygame.Rect(376, 66, 24, 384)) #right
    pygame.draw.rect(screen, COLOR_LIGHTRED, pygame.Rect(16, 66, 384, 24)) #top
    pygame.draw.rect(screen, COLOR_LIGHTRED, pygame.Rect(16, 426, 384, 24)) #bottom

    for x in range(0, 32):
        pygame.draw.line(screen, COLOR_GRAY, ((x * 12) + 16, 66), ((x * 12) + 16, 450))

    for y in range(0, 32):
        pygame.draw.line(screen, COLOR_GRAY, (16, (y * 12) + 66), (400,(y * 12) + 66))

    # Split up right side (16x16 font)
    pygame.draw.rect(screen, COLOR_LIGHTRED, pygame.Rect(400, 66, 24, 384)) #left
    pygame.draw.rect(screen, COLOR_LIGHTRED, pygame.Rect(760, 66, 24, 384)) #right
    pygame.draw.rect(screen, COLOR_LIGHTRED, pygame.Rect(400, 66, 384, 24)) #top
    pygame.draw.rect(screen, COLOR_LIGHTRED, pygame.Rect(400, 426, 384, 24)) #bottom

    for x in range(0, 17): # 17 because we need to draw the right line
        pygame.draw.line(screen, COLOR_GRAY, ((x * 24) + 400, 66), ((x * 24) + 400, 450))

    for y in range(0, 16):
        pygame.draw.line(screen, COLOR_GRAY, (400, (y * 24) + 66), (784, (y * 24) + 66))

    # Draw top menu bar
    pygame.draw.line(screen, COLOR_BLACK, (0, 66), (800, 66))

    # Draw bottom info bar
    pygame.draw.line(screen, COLOR_BLACK, (0, 450), (800, 450))

    # Draw separator
    pygame.draw.line(screen, COLOR_BLACK, (400, 66), (400, 450))

    pygame.display.flip()
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
