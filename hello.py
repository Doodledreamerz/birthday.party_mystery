import pygame
import sys
import math
import os

pygame.init()
pygame.mixer.init()

if getattr(sys, 'frozen', False):
    # Running as bundled app
    current_folder = sys._MEIPASS
else:
    current_folder = os.path.dirname(os.path.abspath(__file__))

# -----------------------
# SCREEN SETTINGS
# -----------------------
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Birthday Murder Mystery")
clock = pygame.time.Clock()

# -----------------------
# FONT
# -----------------------
font = pygame.font.SysFont("arial", 26)
big_font = pygame.font.SysFont("arial", 40)

def draw_text(text, x, y, font_obj=font, color=(255, 255, 255)):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))

# -----------------------
# CLUES
# -----------------------
clues = []
def add_clue(clue):
    if clue not in clues:
        clues.append(clue)

# -----------------------
# LOAD BACKGROUNDS
# -----------------------
school_bg = pygame.image.load(os.path.join(current_folder,"backgrounds","school_hallway.png"))
school_bg = pygame.transform.scale(school_bg, (1000,650))

classroom_bg = pygame.image.load(os.path.join(current_folder,"backgrounds","classroom_crime_scene.png"))
classroom_bg = pygame.transform.scale(classroom_bg, (1000,650))

courtyard_bg = pygame.image.load(os.path.join(current_folder,"backgrounds","school_courtyard.png"))
courtyard_bg = pygame.transform.scale(courtyard_bg, (1000,650))

party_bg = pygame.image.load(os.path.join(current_folder,"backgrounds","party.png"))
party_bg = pygame.transform.scale(party_bg, (1000,650))

bedroom_bg = pygame.image.load(os.path.join(current_folder,"backgrounds","bedroom_morning.png"))
bedroom_bg = pygame.transform.scale(bedroom_bg, (1000,650))

# -----------------------
# LOAD SPRITES
# -----------------------
jewel = pygame.image.load(os.path.join(current_folder,"images","jewel.png"))
dakshi = pygame.image.load(os.path.join(current_folder,"images","dakshi.png"))
gargi = pygame.image.load(os.path.join(current_folder,"images","gargi.png"))
ishani = pygame.image.load(os.path.join(current_folder,"images","ishani.png"))
manha = pygame.image.load(os.path.join(current_folder,"images","manha.png"))
zaara = pygame.image.load(os.path.join(current_folder,"images","zaara.png"))
ayra = pygame.image.load(os.path.join(current_folder,"images","ayra.png"))
ritisha = pygame.image.load(os.path.join(current_folder,"images","ritisha.png"))
batul = pygame.image.load(os.path.join(current_folder,"images","batul.png"))
ruthvika = pygame.image.load(os.path.join(current_folder,"images","ruthvika.png"))

# -----------------------
# MUSIC
# -----------------------
pygame.mixer.music.load(os.path.join(current_folder,"music","mystery_theme.mp3"))
pygame.mixer.music.play(-1)

# -----------------------
# GAME STATE
# -----------------------
scene = "intro"
party_accuse = None

# -----------------------
# SPRITE BOUNCE FUNCTION
# -----------------------
def draw_sprite_with_bounce(sprite, x, y, tick):
    """Makes the sprite bounce up and down slightly."""
    offset = 5 * math.sin(tick * 0.01)  # bounce amplitude
    screen.blit(sprite, (x, y + offset))

# -----------------------
# CHOICE FUNCTIONS
# -----------------------
def show_choices(options, y_start=450):  # added y_start parameter
    y = y_start
    for i, option in enumerate(options):
        draw_text(f"{i+1}. {option}", 50, y, color=(0,0,0))  # black text
        y += 40

def wait_for_key():
    waiting = True
    key_pressed = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key_pressed = event.key
                waiting = False
        pygame.display.update()
        clock.tick(60)
    return key_pressed

# -----------------------
# TEXT WITH BACKGROUND
# -----------------------
def draw_text(text, x, y, font_obj=font, color=(0,0,0), bg_color=(255,255,255), padding=5):
    """
    Draws text with a colored rectangle behind it.
    - color: text color (default black)
    - bg_color: rectangle color (default white)
    - padding: space around text inside rectangle
    """
    img = font_obj.render(text, True, color)
    rect = img.get_rect()
    rect.topleft = (x - padding, y - padding)  # move rect slightly for padding
    rect.width += 2*padding
    rect.height += 2*padding
    pygame.draw.rect(screen, bg_color, rect)
    screen.blit(img, (x, y))

TEXT_START_Y = 350
CHOICES_START_Y = 500

# -----------------------
# DETECTIVE NOTEBOOK
# -----------------------
# HELPER: draw wrapped text inside notebook
def draw_text_wrapped(text, x, y, max_width=300, font_obj=font, color=(255,255,255), bg_color=(30,30,30), padding=5):
    words = text.split(' ')
    line = ""
    for word in words:
        test_line = line + word + " "
        test_img = font_obj.render(test_line, True, color)
        if test_img.get_width() > max_width:
            # draw current line
            img = font_obj.render(line, True, color)
            rect = img.get_rect()
            rect.topleft = (x - padding, y - padding)
            rect.width += 2*padding
            rect.height += 2*padding
            pygame.draw.rect(screen, bg_color, rect)
            screen.blit(img, (x, y))
            y += font_obj.get_height() + padding  # move down for next line
            line = word + " "
        else:
            line = test_line
    if line:  # draw last line
        img = font_obj.render(line, True, color)
        rect = img.get_rect()
        rect.topleft = (x - padding, y - padding)
        rect.width += 2*padding
        rect.height += 2*padding
        pygame.draw.rect(screen, bg_color, rect)
        screen.blit(img, (x, y))
    return y + font_obj.get_height() + padding  # return updated y

# UPDATED NOTEBOOK FUNCTION
def draw_notebook():
    pygame.draw.rect(screen, (30,30,30), (600,50,350,550))
    draw_text("NOTEBOOK", 620, 60, big_font)
    y = 120
    if clues:
        for c in clues:
            y = draw_text_wrapped(f"- {c}", 620, y, max_width=300, color=(255,255,255), bg_color=(30,30,30), padding=5)
    else:
        draw_text_wrapped("No clues yet.", 620, y, max_width=300, color=(255,255,255), bg_color=(30,30,30), padding=5)
# -----------------------
# SCENES
# -----------------------
def scene_intro():
    screen.blit(bedroom_bg, (0,0))
    draw_text("It's my birthday.", 50, 350, color=(0,0,0))
    draw_text("But someone says Dakshi is dead.", 50, 400, color=(0,0,0))
    show_choices(["Investigate the school"])  # no y_start needed
    key = wait_for_key()
    if key == pygame.K_1:
        return "school_hallway"
    return "intro"

def scene_school_hallway():
    screen.blit(school_bg, (0,0))
    draw_text("The hallway is full of whispers.", 50, 250,color=(0,0,0))
    show_choices([
        "Talk to Zaara",
        "Talk to Ayra",
        "Talk to Ritisha & Batul",
        "Talk to Ruthvika",
        "Talk to Gargi",
        "Talk to Ishani",
        "Go to Classroom"
    ],y_start=350)
    key = wait_for_key()
    if key == pygame.K_1:
        return "zaara"
    elif key == pygame.K_2:
        return "ayra"
    elif key == pygame.K_3:
        return "ritisha_batul"
    elif key == pygame.K_4:
        return "ruthvika"
    elif key == pygame.K_5:
        return "gargi_school"
    elif key == pygame.K_6:
        return "ishani_school"
    elif key == pygame.K_7:
        return "classroom"
    return "school_hallway"

def scene_zaara():
    screen.blit(courtyard_bg, (0,0))
    draw_sprite_with_bounce(zaara, 500, 200, pygame.time.get_ticks())
    draw_text("Zaara: Dakshi borrowed my Furina doll yesterday.",50,400,color=(0,0,0))
    add_clue("Missing Furina doll")
    show_choices(["Return to hallway"])
    key = wait_for_key()
    if key == pygame.K_1:
        return "school_hallway"
    return "zaara"

def scene_ayra():
    screen.blit(courtyard_bg, (0,0))
    draw_sprite_with_bounce(ayra, 450, 200, pygame.time.get_ticks())
    draw_text("Ayra: I saw Gargi carrying a big bag this morning.",50,400,color=(0,0,0))
    add_clue("Gargi carrying bag")
    show_choices(["Return to hallway"])
    key = wait_for_key()
    if key == pygame.K_1:
        return "school_hallway"
    return "ayra"

def scene_ritisha_batul():
    screen.blit(courtyard_bg, (0,0))
    draw_sprite_with_bounce(ritisha, 350, 200, pygame.time.get_ticks())
    draw_sprite_with_bounce(batul, 550, 200, pygame.time.get_ticks())
    draw_text("Ritisha & Batul were debating football vs F1.",50,400,color=(0,0,0))
    add_clue("Ritisha & Batul alibi")
    show_choices(["Return to hallway"])
    key = wait_for_key()
    if key == pygame.K_1:
        return "school_hallway"
    return "ritisha_batul"

def scene_ruthvika():
    screen.blit(classroom_bg, (0,0))
    draw_sprite_with_bounce(ruthvika, 600, 120, pygame.time.get_ticks())
    draw_text("Ruthvika: In string theory, every event branches into infinite universes.",50,400,color=(0,0,0))
    add_clue("Dakshi's bracelet found")
    show_choices(["Return to hallway"])
    key = wait_for_key()
    if key == pygame.K_1:
        return "school_hallway"
    return "ruthvika"

def scene_gargi_school():
    screen.blit(classroom_bg, (0,0))
    draw_sprite_with_bounce(gargi, 700, 200, pygame.time.get_ticks())
    draw_text("Gargi: Happy birthday, Jewel. Weird day for a party, huh?",50,400,color=(0,0,0))
    add_clue("Gargi suspicious behavior")
    show_choices(["Return to hallway"])
    key = wait_for_key()
    if key == pygame.K_1:
        return "school_hallway"
    return "gargi_school"

def scene_ishani_school():
    screen.blit(classroom_bg, (0,0))
    draw_sprite_with_bounce(ishani, 550, 200, pygame.time.get_ticks())
    draw_text("Ishani: Let the teachers handle it.",50,400,color=(0,0,0))
    add_clue("Ishani suspicious")
    show_choices(["Return to hallway"])
    key = wait_for_key()
    if key == pygame.K_1:
        return "school_hallway"
    return "ishani_school"

def scene_classroom():
    screen.blit(classroom_bg, (0,0))
    draw_text("You find Dakshi's phone on the floor.",50,400,color=(0,0,0))
    add_clue("Dakshi's phone message: 'Meet me after school – G'")
    show_choices([
        "Return to hallway",
        "Go to Party"  # <-- new option
    ])
    key = wait_for_key()
    if key == pygame.K_1:
        return "school_hallway"
    elif key == pygame.K_2:  # <-- handle the new option
        return "party"
    return "classroom"

def scene_party():
    screen.blit(party_bg, (0,0))
    
    draw_text("Everyone is here. The birthday party begins...",50,400,color=(0,0,0))
    show_choices([
        "Talk to Gargi",
        "Talk to Ishani",
        "Talk to Manha",
        "Look around",
        "Open detective notebook"
    ])
    key = wait_for_key()
    if key == pygame.K_1:
        return "gargi_party"
    elif key == pygame.K_2:
        return "ishani_party"
    elif key == pygame.K_3:
        return "manha_party"
    elif key == pygame.K_4:
        return "look_around_party"
    elif key == pygame.K_5:
        return "notebook_view"
    return "party"

def scene_notebook():
    scroll_y = 0  # initial scroll offset
    scroll_speed = 20  # pixels per key press
    running = True

    while running:
        screen.blit(party_bg, (0,0))  # background
        pygame.draw.rect(screen, (30,30,30), (600,50,350,550))  # notebook area
        draw_text("NOTEBOOK", 620, 60, big_font)

        # draw clues with scroll offset
        y = 120 + scroll_y
        if clues:
            for c in clues:
                y = draw_text_wrapped(f"- {c}", 620, y, max_width=300, color=(255,255,255), bg_color=(30,30,30), padding=5)
        else:
            draw_text_wrapped("No clues yet.", 620, y, max_width=300, color=(255,255,255), bg_color=(30,30,30), padding=5)

        # draw instructions
        draw_text("Arrow Up/Down to scroll, Esc to close", 620, 620, font, color=(255,255,255))

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    scroll_y += scroll_speed
                elif event.key == pygame.K_DOWN:
                    scroll_y -= scroll_speed

    # once the loop ends (Esc pressed), return to the party
    return "party"

def scene_look_around_party():
    draw_text("You notice a gift box with Jewel’s name. The wrapping has dark stains.",50,500,color=(0,0,0))
    add_clue("Suspicious gift box from Gargi")
    wait_for_key()
    return "party"

def scene_gargi_party():
    screen.blit(party_bg, (0,0))
    draw_sprite_with_bounce(gargi, 700, 200, pygame.time.get_ticks())
    draw_text("Gargi: Did you solve your little mystery?",50,400,color=(0,0,0))
    show_choices([
        "Accuse Gargi",
        "Accuse someone else",
        "Say you don't know yet"
    ])
    key = wait_for_key()
    global party_accuse
    if key == pygame.K_1:
        party_accuse = "gargi"
        return "ending_cliffhanger"
    elif key == pygame.K_2:
        party_accuse = "wrong"
        return "ending_bad"
    elif key == pygame.K_3:
        return "party"
    return "gargi_party"

def scene_ishani_party():
    screen.blit(party_bg, (0,0))
    draw_sprite_with_bounce(ishani, 550, 200, pygame.time.get_ticks())
    draw_text("Ishani: Careful, Jewel. Mysteries can be dangerous.",50,400,color=(0,0,0))
    wait_for_key()
    return "party"

def scene_manha_party():
    screen.blit(party_bg, (0,0))
    draw_sprite_with_bounce(manha, 450, 200, pygame.time.get_ticks())
    draw_text("Manha whispers: Something about this is wrong...",50,400,color=(0,0,0))
    wait_for_key()
    return "party"

# -----------------------
# ENDINGS
# -----------------------
def ending_bad():
    screen.fill((0,0,0))
    draw_text("BAD ENDING", 400, 200, big_font)
    draw_text("You accused the wrong person. Ishani notices and…",50,300)
    draw_text("…the screen fades to black.",50,330)
    draw_text("GAME OVER", 400,400, big_font)
    pygame.display.update()
    pygame.time.wait(5000)
    pygame.quit()
    sys.exit()

def ending_cliffhanger():
    screen.fill((0,0,0))
    draw_text("CLIFFHANGER ENDING", 300, 150, big_font)
    draw_text("Jewel opens the gift...",50,250)
    draw_text("Inside: a blood-stained Furina doll.",50,280)
    draw_text("Everyone watches. The mystery isn't over.",50,310)
    draw_text("HAPPY BIRTHDAY JEWEL.",50,340)
    pygame.display.update()
    pygame.time.wait(7000)
    pygame.quit()
    sys.exit()

# -----------------------
# SCENE MAPPING
# -----------------------
scenes = {
    "intro": scene_intro,
    "school_hallway": scene_school_hallway,
    "zaara": scene_zaara,
    "ayra": scene_ayra,
    "ritisha_batul": scene_ritisha_batul,
    "ruthvika": scene_ruthvika,
    "gargi_school": scene_gargi_school,
    "ishani_school": scene_ishani_school,
    "classroom": scene_classroom,
    "party": scene_party,
    "notebook_view": scene_notebook,
    "look_around_party": scene_look_around_party,
    "gargi_party": scene_gargi_party,
    "ishani_party": scene_ishani_party,
    "manha_party": scene_manha_party,
    "ending_bad": ending_bad,
    "ending_cliffhanger": ending_cliffhanger
}

# -----------------------
# GAME LOOP
# -----------------------
while True:
    screen.fill((0,0,0))
    scene_function = scenes.get(scene)
    if scene_function:
        scene = scene_function()
    pygame.display.update()
    clock.tick(60)

