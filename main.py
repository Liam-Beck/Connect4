"""
Welcome to Connect4 written in Python. I am quite new to programming so please accept that the code 
may not be written well or may confuse you at some points. I also know that there are still
some bugs in the code. I'll try to solve them by time. The idea behind the game is to add a 1(for Player1) 
or a 2(for Player2) to a dictionary which represents all fields in the game. After every move the dictionary 
will be scanned to look for four equal numbers in a row (vertical, horizontal or diagonal) 
If you want to give me feedback or write sth. else please write an email to liam.beck@protonmail.com 
"""
import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

COLOR_SLOT = (200, 200, 200)
COLOR_BACKGROUND= (203, 213, 236)
COLOR_LINE = (150, 0, 0)
COLOR_RESTART = (240, 240, 240)

COLOR_PLAYER_1 = (106,90,205)
COLOR_PLAYER_2 = (255, 255, 140)

screen_size = width, height = (700, 700)
radius = 40

fields = {
  1 : [],
  2 : [],
  3 : [],
  4 : [],
  5 : [],
  6 : [],
  7 : []
}



class Main:
  def __init__(self):
    self.Player1 = True
    self.restart = self.restart_button()
    self.Not_Won = True

  def run(self):
    running = True

    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
          sys.exit()

        #Get Position of mouseclick and start Process()
        if event.type == pygame.MOUSEBUTTONDOWN:
          pos = pygame.mouse.get_pos()

          #If sb. has won process should not be started.
          #Game should stop until "Restart"
          if self.Not_Won:
            self.continues = Process(pos[0], pos[1], self.Player1).get_field()
            self.Not_Won = self.continues
            
          if self.Player1:
            self.Player1 = False
          
          else:
            self.Player1 = True

          if self.restart.collidepoint(pos):
            self.start_again()     
            self.Not_Won = True     
      
      clock.tick(60)

  def draw_field(self):
    y = 40
    for c in range(0,6):
      y += 100
      x = 50

      for i in range(0, 7):
        pygame.draw.circle(screen, COLOR_SLOT, (x, y), radius)
        x += 100  

    x = 100
    y = 190
    for i in range(0,6):
      pygame.draw.line(screen, COLOR_LINE, (x, 100), (x, height - 20))
      pygame.draw.line(screen, COLOR_LINE, (20, y), (width -20, y))

      x += 100
      if not y == 590:
        y += 100
    
  def restart_button(self):
    self.restart = pygame.Rect(20, 30, 80, 40)
    pygame.draw.rect(screen, COLOR_RESTART, self.restart) 
    font = pygame.font.Font("font/font.ttf", 28)
    textsurface = font.render('Restart', False, BLACK)
    screen.blit(textsurface, (25, 35))

    player1_surface_start = font.render('Player 1', False, BLACK)
    screen.blit(player1_surface_start, (600, 30))
    pygame.display.update()
    return self.restart

  def start_again(self):
    self.draw_field()
    pygame.draw.rect(screen, COLOR_BACKGROUND,(250,0,600,100))
    pygame.display.update()

    for i in range(1,8):
      fields[i].clear()


class Process:
  def __init__(self, X_FIELD, Y_FIELD, Player1):
    self.Player1 = Player1
    self.X_FIELD = X_FIELD
    self.Y_FIELD = Y_FIELD
    self.text()
    
  def get_field(self):
    #My idea to take the first cipher does not work if x < 100.
    #So I have to improvise 
    if self.X_FIELD < 100:
      self.X_FIELD = 1
    else:
      self.X_FIELD = int(str(self.X_FIELD)[:1]) +1

    self.Y_FIELD = int(str(self.Y_FIELD)[:1]) 

    # If greater than 5 than x would be out of the field
    if len(fields[self.X_FIELD]) <= 5:

      if self.Player1:
        fields[self.X_FIELD].append(1)
      else:
        fields[self.X_FIELD].append(2)

      self.mark_field()
      return CheckWin().check()

    else:
      return CheckWin().check()

  def mark_field(self):  
    #just paint over slots with a bit of calculation :)
    y = 640 - len(fields[self.X_FIELD]) * 100 + 100
    
    if self.Player1:
      COLOR_MARKED = COLOR_PLAYER_1
      self.Player1 = False
    
    else:
      COLOR_MARKED = COLOR_PLAYER_2

    if self.X_FIELD == 1:
      pygame.draw.circle(screen, COLOR_MARKED, (50, y), radius)
    
    else:
      x = self.X_FIELD * 100 - 50
      pygame.draw.circle(screen, COLOR_MARKED, (x, y), radius)

    pygame.display.update()

  def text(self):
    font = pygame.font.Font("font/font.ttf", 30)
    text_player1 = 'Player 1'
    text_player2 = 'Player 2'

    pygame.draw.rect(screen,COLOR_BACKGROUND,(300,0,500,100))

    if not self.Player1:
      textsurface = font.render(text_player1, False, (0,0,0))
    
    else:
      textsurface = font.render(text_player2, False, (0,0,0))

    screen.blit(textsurface, (600, 30))
    pygame.display.update()


class CheckWin:
  def __init__(self):
    self.Not_Won = True

  def check(self):
    #Check if there is a string with 4 same numbers in a row. 
    #If yes self.Not_Won will be changed to False wich will be returned

    self.get_vertical()
    self.get_horizontal()
    self.get_diagonal()

    return self.Not_Won

  def get_horizontal(self):
    for j in range(len(fields)):
      string = ''
      string2 = ''

      for i in fields.values():

        try:   
          string += str(i[j])

        except IndexError:
          string2 += string
          string = ''
      self.check_win(string, string2)
  
  def get_vertical(self):
    string2 = '' 
    for i in range(1,8):
      string = ''
      #No need if less than four
      if len(fields[i]) >= 4:
        for j in fields[i]:
          string += str(j)
      self.check_win(string, string2)

  def get_diagonal(self):
    #Now it' getting confusing...
    #Top-Down three diagonal lines starting on y-  b axis
    height = 0
    string2 = ''
    for i in range(3):
      start = 3 + height
      string = ''
      for j in range(1, len(fields)):
        if start >= 0:
          try:
            string += str(fields[j][start])
          
          except IndexError:
            string2 = ''
            string2 = string
            string = ''
          start -= 1
          self.check_win(string, string2)
      height += 1

    #Top-Down three diagonal lines starting on x-axis
    until = 8
    height = 0
    for i in range(3):
      start = 5
      string = ''
      for j in range(2+height, until):
        if start >= 0:
          try:
            string += str(fields[j][start])
            print(string)
            
          except IndexError:
            string2 = ''
            string2 = string
            string = ''
            print(string2)
            
          self.check_win(string, string2)
          start -= 1
      height += 1

    #Down-Top four diagonal lines on x-axis
    string2 = ''
    higher = 0
    for i in range(4):
      index = 0
      string = ''
      for j in range(1+higher, len(fields) +1):

        try:
          string += str(fields[j][index])
          index += 1

        except IndexError:
          string2 = ''
          string2 = string
          string = ''
        self.check_win(string, string2) 
      higher += 1

    #Down-Top two diagonal lines on y axis
    height = 0
    for i in range(2):
      index = 1 + height
      string = ''

      for j in range(1, len(fields)+1):
        try:
          string += str(fields[j][index])
          index += 1

        except IndexError:
          string2 = ''
          string = string2
          string = ''
        self.check_win(string, string2)
      height += 1

  def check_win(self, game, game2):
    #Check if there are four equal numbers in a row
    p1 = '1111'
    p2 = '2222'
    if p1 in game or p1 in game2:
      self.print_results('Player1')
      self.Not_Won = False

    if p2 in game or p2 in game2:
      self.print_results('Player 2')
      self.Not_Won = False

  def print_results(self, player):
    font = pygame.font.Font("font/font.ttf", 25)
    text = 'Congratulation! ' + player + ' has won the match!'   
    
    pygame.draw.rect(screen, COLOR_BACKGROUND,(270,0,500,100))
    text_surface = font.render(text, False, BLACK)
    screen.blit(text_surface, (250, 30))
    pygame.display.update()


if __name__ == "__main__":
  pygame.init()
  pygame.font.init()
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode(screen_size)
  screen.fill(COLOR_BACKGROUND)
  pygame.display.set_caption('Connect 4')
  Main().draw_field()
  pygame.display.update()
  Main().run()   