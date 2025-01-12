add_library('sound')
import csv
import os
import copy
PATH=os.getcwd()

class Game:
    def __init__(self):
       self.w = 1350
       self.h = 750
       self.screen_stage = "menu"
       self.file = None
       self.amp = None
       self.score = {}
       self.hited = {k: 0 for k in self.score.keys()}
       self.lines = {n: (n + 0.5) * self.h / 4 for n in range(4)}
       self.lines_for_draw = {n: (n + 1) * self.h / 4 for n in range(4)}
       self.points = {'start': self.w * 0.1, 'end': self.w * 0.9}
       self.w_ = self.points['end'] - self.points['start']
       self.pressed = {k: False for k in self.lines.keys()}
       self.result = {'s': 0, 'level': 'C'}
       self.prev_time = 0
       self.img = loadImage(PATH+"\\song_selection_images\\Blank_Space.jpeg")
       self.song_paused = True
       self.score_imported = False
       self.t = 0
       self.i = 1
       
    def display(self):    
        if self.screen_stage == "menu":
            # code for menu graphics
            background(15) #dark grey
            textSize(55)
            fill(255,255,255)
            text("WELCOME TO",515,100)
           
            self.logo = loadImage(PATH+"\\song_selection_images\\logo.png")
            image(self.logo,550,112)
                       
            textSize(40)
            if 390<mouseX<650 and 570<mouseY<700:
                fill(0,255,0) # text becomes green when hovered over
            else :
                fill(255,255,255) # text stays white otherwise
            text("Start Game", 400, 670)
           
            textSize(40)
            if 750<mouseX<1050 and 570<mouseY<700:
                fill(0,0,255) # text becomes blue when hovered over
            else :
                fill(255,255,255) # text stays white otherwise
            text("Leaderboard", 770, 670)
           
            textSize(20)
            fill(160,32,240) # purple
            text("Hit the spacebar at any point of the game to return to this page", (game.w/2)-280, game.h-15)
           
       
        elif self.screen_stage == "songs":
           
            background(15) # grey
            textSize(45)
            fill(255,255,255)
            text("Click on the song title of your choice:",290,80)
           
            textSize(25)
            fill(255,255,0)
            text("Use the up and down arrow keys to scroll through the song menu",300,150)
           
            global song_choice
            song_choice = {1: "Blank_Space", 2: "Payphone", 3: "New_World_Sanity", 4: "Shingeki_No_Kyojin", 5: "Snow_Halation", 6:"Strayer"}
            self.img = loadImage(PATH+"\\song_selection_images\\{0}.jpeg".format(song_choice[self.i])) # song album picture
            #textAlign(CENTER)
            if 470<mouseX<1000 and 675<mouseY<self.h-10:
                fill(160,32,240)
            else:
                fill(255,255,255)
            text(song_choice[self.i], (game.w/2)-140, game.h-30) # song title
            image(self.img,(self.w/2)-(self.img.width/2),(self.h/2)-(self.img.height/2))
           
       
        elif self.screen_stage == "play":
            game.draw()
           
        elif self.screen_stage == "leaderboard":
            size(self.w,self.h)
            background(15)
           
            textSize(45)
            fill(255,0,0)
            text("Player:", (self.w*5/18), 100)
            text("Score:", (self.w*11/18), 100)
           
            player_name = []
            player_score = []
            with open(PATH+"\\leaderboard.csv","r") as f:
                f.readline()
                for line in f:
                    xline = line.strip(" ").split(",")
                    player_name.append(xline[0])
                    player_score.append(xline[1])
                f.close()
            textSize(40)
            fill(255,255,255)
           
            NUM_PLAYERS = len(player_name)    
                 
            for p in range(NUM_PLAYERS): #player_name
                text(player_name[p], (self.w*5/18)+10, self.h/4+(p*50))
               
            for s in range(NUM_PLAYERS): #player_score
                text(player_score[s], (self.w*11/18)+10, self.h/4+(s*50))
           

       


    def draw(self):
        #self.file = SoundFile(this, '{0}.mp3'.format(song_choice[self.i]))

        if self.song_paused == True:
            #self.file.pause()
            print("@")
        else:
            if self.score_imported == False:
                with open(PATH+"\\{0}_additional.csv".format(song_choice[self.i]),"r") as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        v_list = []
                        k = float(row[0])+self.t
                        value = int(row[1])
                        v_list.append(value)
                        self.score[k] = v_list
                f.close()
                self.file.loop()
                self.score_imported = True
        if keyCode == LEFT:
            self.song_paused = False

       
        #background(0)
        background(15)
        for n in range(4):
            y = (n + 1) * self.h / 4
            stroke(255)
            line(0, y, self.w, y)

        stroke(255)
        line(self.points['end'], 0, self.points['end'], self.h)

        for l in self.lines:
            y = self.lines[l]
            x = self.points['end']
            if self.pressed[l]:
                fill(153)
            else:
                fill(255)
            ellipse(x, y, 30, 30)

        m = millis()
        m = float(m) / 1000

        app_dur = 4
        for start_inst, line_has_circle in self.score.items():
            if m > start_inst:
                continue
            if start_inst - m < app_dur:
                for l in line_has_circle:

                    cir_y = self.lines[l]
                    cir_x = -(start_inst - m) / app_dur * self.w_ + self.points['end']
                    if cir_x > 0:
                        fill(255)
                        ellipse(cir_x, cir_y, 20, 20)
                    if self.pressed[l]:
                        if abs(cir_x - self.points['end']) < 20:
                            self.result['s'] += 100
                            self.hited[start_inst] = 1
                        duration = 10
                        seq = [v for k, v in self.hited.items() if m > k > m - duration]
                        if len(seq) == 0:
                            self.result['level'] = 'C'
                        else:
                            average = float(sum(seq)) / len(seq)
                            if average > 0.9:
                                self.result['level'] = 'S'
                            elif average > 0.8:
                                self.result['level'] = 'A'
                            elif average > 0.6:
                                self.result['level'] = 'B'
                            elif average > 0.5:
                                self.result['level'] = 'C'
                            else:
                                self.result['level'] = 'D'

        textSize(32)
        fill(255)
        text("score:" + str(self.result['s']), self.w/2, self.h/2)
        fill(255)
        text("current level:" + str(self.result['level']), self.w / 2, self.h * 3 / 4)
       
        fill(255)
        text("Y", self.w*0.95, self.h*1/8)
        text("H", self.w*0.95, self.h*3/8)
        text("N", self.w*0.95, self.h*5/8)    
       
        textSize(25)
        fill(0,255,0)
        text("Press the left arrow key to start", 75, self.h-75)

        vol = self.amp.analyze()

        if m != self.prev_time:
            self.prev_time = m

    def keyPressed(self):
        key_2_line = {'y': 0, 'h': 1, 'n': 2}
        m = millis()
        m = float(m) / 1000
        print("key pressed", m, key)
        for k_, line_ in key_2_line.items():
            if key == k_:
                self.pressed[line_] = True
        if self.screen_stage == "songs":
            if keyCode == UP:
                if self.i == 1:
                    self.i = 6
                else:
                    self.i -=1
            if keyCode == DOWN:
                if self.i == 6:
                    self.i = 1
                else:
                    self.i +=1
        if keyCode == 32: # ascii code for spacebar
            self.screen_stage = "menu"
        if keyCode == LEFT:
            if self.screen_stage == "play":
                self.t = millis()
                self.t = float(self.t)/1000
               


    def keyReleased(self):
        key_2_line = {'y': 0, 'h': 1, 'n': 2}
        for k_, line_ in key_2_line.items():
            if key == k_:
                self.pressed[line_] = False
        if self.screen_stage == "songs":
            if keyCode == UP:
                pass
            if keyCode == DOWN:
                pass


    def mouseClicked(self):
        if self.screen_stage == "menu":
            if 390<mouseX<650 and 570<mouseY<700: # "start game" button
                self.screen_stage = "songs"
            elif 750<mouseX<1050 and 570<mouseY<700: # "leaderboard" button
                self.screen_stage = "leaderboard"
        elif self.screen_stage == "songs":
            if 470<mouseX<1000 and 675<mouseY<self.h-10:
                self.screen_stage = "play"
                self.file = SoundFile(this, PATH+"\\song_selection_songs\\{0}.mp3".format(song_choice[self.i]))
                self.amp = Amplitude(this)
                self.amp.input(self.file)



game = Game()

def setup():
    size(game.w,game.h)
    background(255)

def draw():
    game.display()

def keyReleased():
    game.keyReleased()

def keyPressed():
    game.keyPressed()

def mouseClicked():
    game.mouseClicked()

def display():
    game.display()
