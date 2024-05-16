import calendar

import pygame
from time import time
import datetime

try:
    char_list = eval(open("charlist", "r").read())
except FileNotFoundError:
    char_list = []
    name = 0
    i = 0
    print("(input -1 if you dont have an nth character)")
    while name != "-1":
        name = input(f"Please input character number {i}'s name: ")
        char_list.append(name)
        i += 1

    open("charlist", "w").write(str(char_list))

pygame.display.init()
pygame.font.init()
Font = pygame.font.SysFont("Consolas", 40)
Font_Small = pygame.font.SysFont("Consolas", 18)


# Button class
class Button:
    def __init__(self, position, size, icon, colours=((200, 0, 0), (0, 200, 0))):
        # position = [x, y]
        # size = [width, height]
        # icon = <file name>
        # colours = (
        # background : (r, g, b),
        # highlight : (r, g, b),
        # selected : (r, g, b))
        self.Rect = pygame.rect.Rect(position, size)
        self.icon = pygame.image.load(icon)
        self.iconRect = pygame.rect.Rect([a + b / 2 - c / 2 for a, b, c in zip(position, size, self.icon.get_size())],
                                         self.icon.get_size())
        self.colours = colours
        self.on = False

    def Draw(self, display):
        mouse = pygame.mouse.get_pos()

        if self.Rect.collidepoint(mouse):
            drawRect = self.Rect.inflate(-5, -5)
            color = 0.7
        else:
            drawRect = self.Rect
            color = 1

        if self.on:
            pygame.draw.rect(display, [a * color for a in self.colours[1]], drawRect, 0, 15)
        else:
            pygame.draw.rect(display, [a * color for a in self.colours[0]], drawRect, 0, 15)
        display.blit(self.icon, self.iconRect)

    def Clicked(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.Rect.collidepoint(mouse) and sum(click) > 0:
            self.on = not self.on
            return True
        else:
            return False


# TextBox class
class TextBox:
    def __init__(self, pos, size, suggestions):
        self.pos = pos
        self.size = size
        self.selected = False
        self.suggestions = suggestions
        self.scroll = 0
        self.text = ""

    def Update(self, mouse, click, key):
        if 0 < mouse[0] - self.pos[0] < self.size[0] and 0 < mouse[1] - self.pos[1] < self.size[1] and click:
            self.selected = True
        elif not (0 < mouse[0] - self.pos[0] < self.size[0] and 0 < mouse[1] - self.pos[1] < self.size[1]) and click:
            self.selected = False

        if self.selected:
            if key not in [None, "Backspace", "Ctrl Backspace", "Return", "Up", "Down", "Tab"]:
                self.text += key
                self.scroll = 0
            elif key == "Backspace":
                self.text = self.text[:-1]
                self.scroll = 0
            elif key == "Ctrl Backspace":
                self.text = ""
                self.scroll = 0
            elif key == "Return":
                txt = self.text
                self.text = ""
                return txt

    def Draw(self):
        pygame.draw.rect(screen, [60] * 3, (*self.pos, *self.size), 0, 15)

        if self.text != "":
            renderedText = Font.render(self.text, True, [150] * 3)
        else:
            renderedText = Font.render("Amount Sampled", True, [80] * 3)

        screen.blit(renderedText, (self.pos[0] + 15, self.pos[1] + 5))

        if time() // 0.5 % 2 == 0 and self.selected:
            pygame.draw.line(screen, [200] * 3, (self.pos[0] + len(self.text) * 22 + 15, self.pos[1] + 5),
                             (self.pos[0] + len(self.text) * 22 + 15, self.pos[1] + self.size[1] - 5), 3)


# Screen declaration
screen = pygame.display.set_mode((800, 600))


# Simple lists
skills = ["Choppin", "Mining", "Catching", "Fishing"]
types = ["Wood", "Ore", "Bug", "Fish"]

# Declare buttons
Char_Butts = []
for i in range(len(char_list)):
    # Change in left by 4 == change in right by -1
    Char_Butts.append(Button((32 + i * 75, 30), (60, 60), "CharIcon.png"))
Skill_Butts = []
for i in range(4):
    # Change in left by 4 == change in right by -1 TODO
    Skill_Butts.append(Button((32 + i * 60, 130), (50, 50), f"Skill_Icons\\{skills[i]}_Skill_Icon.png"))
Icon_Butts = []
for skill in range(4):
    Icon_Butts.append([])
    for icon in range(24):
        icon = 23 - icon
        try:
            Icon_Butts[skill].append(Button((32 + icon % 4 * 60, 210 + icon // 4 * 60), (50, 50),
                                            f"{types[skill]}\\{types[skill]} ({icon + 1}).png"))
        except FileNotFoundError:
            pass

try:
    World_Butts = []
    for world in range(5):
        # Change in left by 4 == change in right by -1 TODO
        World_Butts.append(Button((280 + world * 100, 130), (90, 50), f"World\\Wb{world + 1}.png"))
except FileNotFoundError:
    pass


# Pre-enable buttons
Char_Butts[0].on = True
Skill_Butts[0].on = True
Icon_Butts[0][-1].on = True
Icon_Butts[1][-1].on = True
Icon_Butts[2][-1].on = True
Icon_Butts[3][-1].on = True

# Pre-enable some other things
selection_Butts = [*Skill_Butts, *World_Butts]
Box = TextBox((300, 210), (470, 50), False)
Ctrl = False
Mouse = [0, 0]
Key = None
Click = False

char = 0
item = 0
skill_selected = 0

suffix = {
    'k': 1000,
    'm': 1000000,
    'b': 1000000000
}

# Main Loop
while True:
    # Event handling
    for event in pygame.event.get():
        # Mouse event handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            Mouse = pygame.mouse.get_pos()
            Click = True

            # Check for all buttons clicked
            char = -1
            for i, Butt in enumerate(Char_Butts):
                if Butt.Clicked():
                    char = i
                    break
            if char != -1:
                for i, Butt in enumerate(Char_Butts):
                    if i != char:
                        Butt.on = False
            skill = -1
            for i, Butt in enumerate(selection_Butts):
                if Butt.Clicked():
                    skill = i
                    break
            if skill != -1:
                for i, Butt in enumerate(selection_Butts):
                    if i != skill:
                        Butt.on = False

            item = -1
            for i, Butt in enumerate(Icon_Butts[skill_selected]):
                if Butt.Clicked():
                    item = i
                    break
            if item != -1:
                for i, Butt in enumerate(Icon_Butts[skill_selected]):
                    if i != item:
                        Butt.on = False
        elif event.type == pygame.MOUSEBUTTONUP:
            Click = False

        # Key event handling
        elif event.type == pygame.KEYDOWN:
            if event.key not in [pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_UP, pygame.K_DOWN, pygame.K_TAB]:
                Key = event.unicode
            else:
                Key = (pygame.key.name(event.key)).title()

            if event.key == pygame.K_BACKSPACE:
                if Ctrl:
                    Key = "Ctrl Backspace"
                else:
                    Key = "Backspace"
            elif event.key == pygame.K_LCTRL:
                Ctrl = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                Ctrl = False

    # Background sections to divide screen
    pygame.draw.rect(screen, (100, 100, 100), (0, 0, 800, 600), 0, 15)
    pygame.draw.rect(screen, (80, 80, 80), (20, 20, 760, 80), 0, 15)
    pygame.draw.rect(screen, (80, 80, 80), (20, 120, 760, 70), 0, 15)
    pygame.draw.rect(screen, (80, 80, 80), (20, 200, 252, 370), 0, 15)
    pygame.draw.rect(screen, (80, 80, 80), (290, 200, 490, 370), 0, 15)

    # Draw all the buttons in their respective spots
    for Butt in Char_Butts:
        Butt.Draw(screen)
    for Butt in World_Butts:
        Butt.Draw(screen)
    for i, Butt in enumerate(Skill_Butts):
        Butt.Draw(screen)
        if Butt.on:
            skill_selected = i
    for i, Butt in enumerate(Icon_Butts[skill_selected]):
        Butt.Draw(screen)

    # Draw textbox for sample inputs
    text = Box.Update(Mouse, Click, Key)
    Box.Draw()
    Key = None

    date = datetime.date.today()

    # Get skill, char, and item
    skill, char, item = -1, -1, -1
    for i, Butt in enumerate(Char_Butts):
        if Butt.on:
            char = i
            break
    for i, Butt in enumerate(selection_Butts):
        if Butt.on:
            skill = i
            break
    for i, Butt in enumerate(Icon_Butts[skill_selected]):
        if Butt.on:
            item = i
            break

    # Write value to file

    if text is not None:
        char_file = open(char_list[int(char)], "a")
        try:
            if not text[-1].isnumeric():
                value = float(text[0:-1]) * suffix[text[-1]]
            else:
                value = float(text)
            day_int = date.day + date.month * 30 + date.year * 365
            char_file.write(
                f"\n[{day_int}, 'Resource',  ('T{(len(Icon_Butts[skill]) - item)}', '{'WOBF'[skill]}'), {value}]")
        except ValueError:
            pass
        char_file.close()

    # Display previous samples for same mat

    icon_matches = 0
    skill_matches = 0

    try:
        char_file = open(char_list[int(char)], "r")
        for line in reversed(char_file.readlines()):
            try:
                line = eval(line)
            except SyntaxError:
                pass
            day = line[0] % 365 % 30 // 1
            month = line[0] % 365 // 30
            year = line[0] // 365
            day_str = "" + calendar.month_abbr[month] + " " + str(day) + ", " + str(year)

            adj = -1
            amount = int(line[3])
            while amount > 1000:
                amount /= 1000
                adj += 1
            if int(line[2][0][1::]) == (len(Icon_Butts[skill]) - item) and line[2][1] == 'WOBF'[skill] and icon_matches < 10:
                render = Font_Small.render(day_str + "|" + str(amount) + list(suffix.keys())[adj], True, [120] * 3)
                icon = pygame.image.load(f"{types[skill]}\\{types[skill]} ({int(line[2][0][1::])}).png")
                screen.blit(render, (300, 280 + icon_matches * 30))
                screen.blit(icon, (500, 270 + icon_matches * 30))

                icon_matches += 1
            if line[2][1] == 'WOBF'[skill] and skill_matches < 10:
                render = Font_Small.render(day_str + "|" + str(amount) + list(suffix.keys())[adj], True, [120] * 3)
                icon = pygame.image.load(f"{types[skill]}\\{types[skill]} ({int(line[2][0][1::])}).png")
                screen.blit(render, (540, 280 + skill_matches * 30))
                screen.blit(icon, (740, 270 + skill_matches * 30))

                skill_matches += 1

        char_file.close()
    except FileNotFoundError or NameError:
        pass

    # Clear screen
    pygame.display.flip()
    screen.fill((0, 0, 0))
    pass

# TODO Add previous samples below TextBox for 1 wood 1 char and all woods 1 char
