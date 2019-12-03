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
    font = pygame.font.Font("font.ttf", 25)
    text = 'Congratulation! ' + player + ' has won the match!'

    pygame.draw.rect(screen, COLOR_BACKGROUND,(270,0,500,100))
    text_surface = font.render(text, False, BLACK)
    screen.blit(text_surface, (250, 30))
    pygame.display.update()
