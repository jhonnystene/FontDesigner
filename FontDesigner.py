#!/usr/bin/env python3

# FontDesigner
# Copyright 2020 Johnny Stene <jhonnystene@protonmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#
# This is just a small app for designing fonts for arcticOS and exporting in the .h format it uses.

import pygame, json

pygame.init()
pygame.display.set_caption("FontDesigner")
screen = pygame.display.set_mode((800, 500))

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_LIGHTRED = (255, 102, 102)
COLOR_GRAY = (204, 204, 204)

FONT_REGULAR = pygame.font.SysFont(None, 24)
FONT_LARGE = pygame.font.SysFont(None, 72)

savedFonts16 = []
savedFonts32 = []
fontChars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,/\'\""

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

def exportChar(character):
    #print(character)
    exported = []
    for y in character:
        current = ""
        for x in y:
            current = current + str(x)
            if(len(current) == 8):
                exported.append(int(current, 2))
                current = ""
    return exported

# Init fonts
for i in range(0, len(fontChars)):
    savedFonts16.append(getBlankCharacter16())
    savedFonts32.append(getBlankCharacter32())

print("Trying to load savedfont.json...")
try:
    with open("savedfont.json") as jsonfile:
        data = json.load(jsonfile)
        savedFonts16 = data["font16"]
        savedFonts32 = data["font32"]
except:
    print("Failed!")

print(exportChar(savedFonts32[0]))

def save(font16, font32):
    print("Trying to save...")
    font = {}
    font["font16"] = font16
    font["font32"] = font32
    with open("savedfont.json", "w") as jsonfile:
        json.dump(font, jsonfile)

def export(font16, font32):
    print("Trying to export...")
    exportString = ""

    # Save 16x16 font
    exportString = exportString + "\nint font16[" + str(len(font16) * len(exportChar(font16[0]))) + "] = {"
    for character in font16:
        exportCharacter = exportChar(character)
        for i in exportCharacter:
            exportString = exportString + str(i) + ","
    exportString = exportString[:-1] + "};"

    # Save 32x32 font
    exportString = exportString + "\nint font32[" + str(len(font32) * len(exportChar(font32[0]))) + "] = {"
    for character in font32:
        exportCharacter = exportChar(character)
        for i in exportCharacter:
            exportString = exportString + str(i) + ","
    exportString = exportString[:-1] + "};"

    with open("exportedfont.h", "w") as outfile:
        outfile.write(exportString)

currentCharacter = 0
running = True
while running:
    screen.fill(COLOR_WHITE)

    if(currentCharacter >= len(fontChars)):
        currentCharacter = 0

    if(currentCharacter < 0):
        currentCharacter = len(fontChars) - 1

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

    # Draw current charater at top left
    charImg = FONT_LARGE.render(fontChars[currentCharacter], True, COLOR_BLACK)
    screen.blit(charImg, (10, 5))

    # Draw save button at top left
    pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(98, 18, 52, 32), 2)
    saveImg = FONT_REGULAR.render("Save", True, COLOR_BLACK)
    screen.blit(saveImg, (105, 25))

    # Draw export button at top left
    pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(155, 18, 62, 32), 2)
    saveImg = FONT_REGULAR.render("Export", True, COLOR_BLACK)
    screen.blit(saveImg, (160, 25))

    # Draw current characters
    draw16 = savedFonts16[currentCharacter]
    draw32 = savedFonts32[currentCharacter]

    for y in range(0, 32):
        for x in range(0, 32):
            if(draw32[y][x] == 1):
                pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(16 + (x * 12), 66 + (y * 12), 12, 12))

    for y in range(0, 16):
        for x in range(0, 16):
            if(draw16[y][x] == 1):
                pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(400 + (x * 24), 66 + (y * 24), 24, 24))


    pygame.display.flip()
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False

        if(event.type == pygame.KEYUP):
            if(event.key == pygame.K_LEFT):
                currentCharacter -= 1
            elif(event.key == pygame.K_RIGHT):
                currentCharacter += 1

        if(event.type == pygame.MOUSEBUTTONDOWN):
            # Are we in the drawing area?
            if(event.pos[0] > 16 and event.pos[0] < 784
                and event.pos[1] > 66 and event.pos[1] < 450):
                    if(event.pos[0] < 400): # We're drawing in the 32x32 area
                        clickedX = int((event.pos[0] - 16) / 12)
                        clickedY = int((event.pos[1] - 66) / 12)
                        if(event.button == 1):
                            print("Filling position " + str(clickedX) + "," + str(clickedY) + " on 32x32 font.")
                            savedFonts32[currentCharacter][clickedY][clickedX] = 1
                        elif(event.button == 3):
                            print("Clearing position " + str(clickedX) + "," + str(clickedY) + " on 32x32 font.")
                            savedFonts32[currentCharacter][clickedY][clickedX] = 0
                    else: # We're drawing in the 16x16 area
                        clickedX = int((event.pos[0] - 400) / 24)
                        clickedY = int((event.pos[1] - 66) / 24)
                        if(event.button == 1):
                            print("Filling position " + str(clickedX) + "," + str(clickedY) + " on 16x16 font.")
                            savedFonts16[currentCharacter][clickedY][clickedX] = 1
                        elif(event.button == 3):
                            print("Clearing position " + str(clickedX) + "," + str(clickedY) + " on 16x16 font.")
                            savedFonts16[currentCharacter][clickedY][clickedX] = 0
            else: # We're in the toolbar areas
                if(event.pos[0] > 98 and event.pos[0] < 150
                    and event.pos[1] > 18 and event.pos[1] < 50):
                    save(savedFonts16, savedFonts32)
                if(event.pos[0] > 155 and event.pos[0] < 217
                    and event.pos[1] > 18 and event.pos[1] < 50):
                    export(savedFonts16, savedFonts32)

        if(event.type == pygame.MOUSEMOTION):
            # Are we in the drawing area?
            if(event.pos[0] > 16 and event.pos[0] < 784
                and event.pos[1] > 66 and event.pos[1] < 450):
                    if(event.pos[0] < 400): # We're drawing in the 32x32 area
                        clickedX = int((event.pos[0] - 16) / 12)
                        clickedY = int((event.pos[1] - 66) / 12)
                        if(event.buttons[0]):
                            print("Filling position " + str(clickedX) + "," + str(clickedY) + " on 32x32 font.")
                            savedFonts32[currentCharacter][clickedY][clickedX] = 1
                        elif(event.buttons[2]):
                            print("Clearing position " + str(clickedX) + "," + str(clickedY) + " on 32x32 font.")
                            savedFonts32[currentCharacter][clickedY][clickedX] = 0
                    else: # We're drawing in the 16x16 area
                        clickedX = int((event.pos[0] - 400) / 24)
                        clickedY = int((event.pos[1] - 66) / 24)
                        if(event.buttons[0]):
                            print("Filling position " + str(clickedX) + "," + str(clickedY) + " on 16x16 font.")
                            savedFonts16[currentCharacter][clickedY][clickedX] = 1
                        elif(event.buttons[2]):
                            print("Clearing position " + str(clickedX) + "," + str(clickedY) + " on 16x16 font.")
                            savedFonts16[currentCharacter][clickedY][clickedX] = 0
