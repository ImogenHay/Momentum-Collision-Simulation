### MOMENTUM COLLISION SIMULATION (final version) ###
import pygame
import math
import time


## Mommentum & Kinetic Energy Class ##
class Momentum_Ek(object): #Calculates the momentum and kinetic energy of a particular object using its
                           #mass and velocity

    #Constructor 
    def __init__(self, mass, velocity):

        #Attributes
        self.mass = mass       
        self.velocity = velocity
        
    #String method that will be called on print displaying mass and velocity of object and their units
    def __str__(self):
        report = "Mass: " + str(self.mass) + " kg\n"
        report = report + "Initial Velocity: " + str(self.velocity) + " m/s"               
        return report       

    #Methods  
    def getMomentum(self): #Calculates and outputs the momentum of this object
        momentum = self.mass * self.velocity #uses formula 
        return momentum 
    
    def getKinetic_Energy(self): #Calculates and outputs the kinetic energy of this object
        Ek = 0.5 * self.mass * (self.velocity)**2  #uses formula
        return Ek 



## Collision Class ##     
class Collision(object): #Calculaates the final velocity, final kinetic energy and change in Ek of objects
                         #after elastic or inelastic collision

    #Constructor 
    def __init__(self, m1, v1, m2, v2, p_total, Ek_total):

        #Attributes
        self.m1 = m1       
        self.m2 = m2
        self.v1 = v1
        self.v2 = v2
        self.p_total = p_total
        self.Ek_total = Ek_total
        
    #String method that will be called on print displaying the momentum before the collision and their units
    def __str__(self):
        report = "Total Momentum before Collision: " + str(round(self.p_total,2)) + " kg m/s \n"
        report = report + "Total Kinetic Energy before Collision: " + str(round(self.Ek_total,2)) + " J \n"
        return report       

    #Methods  
    def getInelastic_Velocity(self): #Calculates final velocity of both objects after inelastic collision
        m_total = self.m1 + self.m2 #Calculates total mass
        inelastic_v = self.p_total/m_total #Uses total momentum and total mass to calculate final v,
                                                        
        return inelastic_v 

    def getElastic_Velocity1(self): #Calculates final velocity of first object after elastic collision
        m_total = self.m1 + self.m2 #Calculates total mass
        elastic_v1 = ((self.m1-self.m2)*self.v1 + 2*self.m2*self.v2)/m_total #uses the formula I researched
        elastic_v1 = elastic_v1 
        return elastic_v1  

    def getElastic_Velocity2(self): #Calculates final velocity of second object after elastic collision
        m_total = self.m1 + self.m2 #Calculates total mass
        elastic_v2 = (2*self.m1*self.v1 - (self.m1-self.m2)*self.v2)/m_total #uses formula I researched
        elastic_v2 = elastic_v2 
        return elastic_v2
    
    def getFinal_Ek(self, final_v1, final_v2): #Calculates final kinetic energy of both objects after collision
        object1_Ek = 0.5 * self.m1 * (final_v1)**2
        object2_Ek = 0.5 * self.m2 * (final_v2)**2 #For inelastic collision both objects will have the same Ek
        final_Ek = object1_Ek + object2_Ek #Adds kinetic energies of both objects together to find total final Ek,                                                     
        return final_Ek 

    def getChange_Ek(self,final_Ek): #Calculates change in kinetic enery which requires total kinetic energy after collision 
        change_Ek = round(self.Ek_total - final_Ek, 2) #Round change in kinetic energy to two decimal places
        return change_Ek        



## Graph Class ##
class Graph(object): #Creates a graph of kinetic energy against time 

    #Constructor 
    def __init__(self, x1, x2, Ek_before, Ek_after, maxtime, v1, v2):

        #Attributes
        self.x1 = x1       
        self.x2 = x2
        self.Ek_before = Ek_before
        self.Ek_after = Ek_after
        self.maxtime = maxtime
        self.v1 = v1       
        self.v2 = v2

    #Methods  
    def getTime(self): #Calculates the time taken for the objects to collide
        time_taken = 0
        while self.x2 >= self.x1 and time_taken < self.maxtime: #detects collision and limits time
            self.x1 = self.x1 + self.v1 #each sec the object moves a certain distance (it's velocity)
            self.x2 = self.x2 + self.v2
            time_taken = time_taken + 1 #increase time taken as objects move
        return time_taken
    
    def plotGraph(self,time): #needs time taken to know when Ek changes
        points = []
        for i in range (0,time+1):
            point = [i,self.Ek_before] #[x = time, y = Ek]
            points.append(point)
        for i in range (time+1,self.maxtime+1): #after collision
            point = [i,self.Ek_after] #x = time, y = Ek
            points.append(point)

        pygame.init()

        white = (255,255,255) #defines the colours
        black = (0,0,0)
        blue = (0,0,255)
        title = pygame.font.Font(None, 26) #difines different types of text (Font,size)
        title.set_underline(True) #underlines any text using the title font
        font = pygame.font.Font(None, 18)#set to defult font
        gap = 50 #gap between the axis of the graph and the edges of the pygame window

        if self.Ek_before <= 900: #works out scale of y axis depening on maximum Ek  
            scale = 100 #100 points on GUI represents 100J
            size = 1
            if self.Ek_before <= 90: #bigger scale of there is space
                scale = 10 #100 points on GUI represents 10J
                size = 10
            #<= 900 or 90 because anything greater than that is too big for screen
                
            max_Ek = int(math.ceil(self.Ek_before / scale))*scale #Rounds highest value of Ek up to the nearest 10/100 to determin hight of y axis
            y_axis = max_Ek * size #length of y_axis depends on scale determinded earlier
            x_axis = self.maxtime+gap*2 #total width of pygame window
            graphDisplay = pygame.display.set_mode((x_axis,y_axis+gap*2)) #creates window of set resolution
            graphDisplay.fill(white) #makes background white
            pygame.display.set_caption('How Kinetic Energy Varies with Time:') #titles window 
                                                 #(points of ends of line (x,y),             width)
            pygame.draw.line(graphDisplay, black, (gap,y_axis+50), (self.maxtime+gap,y_axis+gap),2)#colour and position of x axis
            pygame.draw.line(graphDisplay, black, (gap,y_axis+50), (gap,gap),2)#colour and position of y axis

            for i in range(0,11): #Creates points a long x axis, interval of 100 seconds
                position = i*100+gap #Converts value in seconds to position on screen
                pygame.draw.line(graphDisplay, black, (position,y_axis+gap), (position,y_axis+gap+5),1) #draws lines
                graphDisplay.blit((font.render(str(position-gap), True, (black))), (position,y_axis+gap+10)) #shows values
            for i in range(0,int(max_Ek/scale)+1): #Creates points a long x axis, interval of 10 Joules
                position = y_axis-(i*100+gap)+100 #Converts value in joules to position on screen
                pygame.draw.line(graphDisplay, black, (gap,position), (gap-5,position),1) #draws lines
                graphDisplay.blit((font.render(str(i*scale), True, (black))), (gap-20,position)) #shows values

            if points[0][1] == points[len(points)-1][1]: #works out collision type to title graph
                message = "Elastic Collision:"
            else:
                message = "Inelastic Collision:"

            graphDisplay.blit((title.render(message, True, (black))), (500,0)) #Displays title
            graphDisplay.blit((font.render("Time (s)", True, (black))), (500,y_axis+80)) #labels x axis
            text = font.render("Total Kinetic Energy (J)", True, (black)) #label for y axis
            text = pygame.transform.rotate(text, 90) #rotates label by 90 degrees to line up with y axis
            graphDisplay.blit(text,(0,y_axis/2))

            posx = (self.maxtime+gap*2)-gap #positions points plotted to line up with axis 
            posy = (y_axis+gap*2)-gap
            for i in range(0,len(points)-1): #plots points by drawing multiple tiny lines
                pygame.draw.line(graphDisplay,blue,(x_axis-(posx-points[i][0]),posy-points[i][1]*size),(x_axis-(posx-points[i+1][0]),posy-points[i+1][1]*size),2)
            
            pygame.display.update() 

            while True: #allows user to exit program
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
        else: #validation - if maxEk is too big for screen graph won't be displayed
            print("Data too big to create graph")



## Animation Class ##
class Animation(object): #Creates the objects and makes them collide

    #Constructor 
    def __init__(self, v1, v2, x2):

        #Attributes
        self.v1 = v1       
        self.v2 = v2
        self.x2 = x2

    #Methods  
    def createObjects(self): 
        pygame.draw.rect(guiDisplay, green, [60, 234, 50, 25]) #draws object 1 on platform
        pygame.draw.rect(guiDisplay, red, [610, 234, 50, 25]) #draws object 2 on platform
        
    def moveObjects(self,time_taken,final_v1,final_v2):
        distance1 = v1/2 #distance objects move per second = velocity divided by two because scale on GUI is 1:2
        distance2 = v2/2
        for i in range (0,time_taken): #moves objects at the speed they are before they collide
            time.sleep(0.01) #makes animation slow enough for users to view
            pygame.draw.rect(guiDisplay, white, [60, 234, 600, 25]) #makes backround white after each movement so no trail
            pygame.draw.rect(guiDisplay, green, [60+distance1, 234, 50, 25]) #draws object 1 at its new position
            distance1 = distance1 + (v1/2)
            pygame.draw.rect(guiDisplay, red, [610+distance2, 234, 50, 25]) #draws object 2 at its new position
            distance2 = distance2 + (v2/2)            
            pygame.display.update()
        while (60+distance1)>60 and (610+distance2)<610: #moves objects at calculated speed after collision until they reach boundary
            time.sleep(0.01) #makes animation slow enough for users to view
            pygame.draw.rect(guiDisplay, white, [60, 234, 600, 25]) #makes backround white after each movement so no trail
            pygame.draw.rect(guiDisplay, green, [60+distance1, 234, 50, 25]) #draws object 1 at its new position
            distance1 = distance1 + (final_v1/2)
            pygame.draw.rect(guiDisplay, red, [610+distance2, 234, 50, 25]) #draws object 2 at its new position
            distance2 = distance2 + (final_v2/2)
            pygame.display.update()


## FUNCTIONS ##
def Validation(message,value): #Function that validates the user inputs,
                               #function recieves the message to be displayed and the type of data being inputted
    while True:
        try: #Allows user to try to input a value after the displayed message
            userInput = float(input(message)) #Input must be a float because velocity and mass don't need to be whole numbers
        except ValueError: #If the value entered is not a float a ValueError will occur so a statement will be printed and the loop repeated
            print("This is not a number\n")
            continue
        if value == 'm' and userInput <= 0: #If the value being inputted is a mass it needs to be greater than
            print("Mass must be greater than 0\n") #needs to be greater than 0 because mass can't be less than 0
            continue
        if value == 'v1' and userInput < 0: #If the value being inputted is v1 it needs to be greater or equal to 0
            print("Velocity of object 1 must be greater than or equal to 0\n")#So always moving in one direction (velocity is vector)
            continue
        if value == 'v2' and userInput > 0: #If the value being inputted is v2 it needs to be smaller or equal to 0
            print("Velocity of object 2 must be greater than or equal to 0\n") #So moving towards other object so collision occurs
            continue
        else:
            return userInput
            break

def Database(m1,v1,m2,v2,p_total,change_Ek): #Function that reads the current infomation from the database and writes new values to it
    try:
       import csv
       with open("database.csv", 'rt') as text_file: #opens text file
          reader = csv.reader(text_file)
          aList = list(reader) #puts data from database into list
    except FileNotFoundError: #If an error occurs a message is displayed to tell the user how to prevent it then ends the program
       print("Please make sure the CSV file is not open and has not been deleted.")
       quit()
    values = [str(m1),str(v1),str(m2),str(v2),str(p_total),str(change_Ek)] #creates list containing the new values
    aList.append(values) #appends new values to the current list
    try:
        import csv
        with open("database.csv", 'w', newline='') as csv_file: #opens the text file
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(aList) #writes the list to the file
            csv_file.close()
    except PermissionError: #If an error occurs a message is displayed to tell the user how to prevent it then end the program
        print("The data could not be added to the database.")
        print("Please make sure the 'database' file is closed and re-start the program.")
        quit()

def button(x,y,w,h,c,c2,action,perameter=None): #(x,y,width,height,colour,second colour,action,parameter for action)
    mouse = pygame.mouse.get_pos() #gives position of mouse
    click = pygame.mouse.get_pressed() #when mouse clicked
    if x+w > mouse[0] > x and y+h > mouse[1] > y: #if users mouse within area of button
        pygame.draw.rect(guiDisplay, c2,(x,y,w,h))#makes button second colour

        if click[0] == 1: #if user click button
            action(perameter) #runs function of button when clicked       
    else:
        pygame.draw.rect(guiDisplay, c,(x,y,w,h)) #draws button
        

def start(x):       
    Object1 = Momentum_Ek(m1,v1) #Created first object using Momentum_Ek class which calculates momentum and initial kinetic energy 
    p1 = Object1.getMomentum() #p used to represent momentum because it resebles the greek symbol 'rho' which is used to represent it in physics 
    Ek1 = Object1.getKinetic_Energy() #returns kinetic energy of first object before collision

    Object2 = Momentum_Ek(m2,v2)#Created second object using Momentum_Ek class which calculates momentum and initial kinetic energy
    p2 = Object2.getMomentum() #p used to represent momentum because it resebles the greek symbol 'rho' which is used to represent it in physics
    Ek2 = Object2.getKinetic_Energy()#returns kinetic energy of second object before collision

    guiDisplay.blit((big_font.render(str(round(m1,2))+" kg", True, (grey))), (85,378))#Prints values calculated and their units
    guiDisplay.blit((big_font.render(str(round(v1,2))+" m/s", True, (grey))), (100,406))
    guiDisplay.blit((big_font.render(str(round(p1,2))+" kgm/s", True, (grey))), (140,434))
    guiDisplay.blit((big_font.render(str(round(Ek1,2))+" J", True, (grey))), (165,462))
    guiDisplay.blit((big_font.render(str(round(m2,2))+" kg", True, (grey))), (450,378))#Prints values calculated and their units
    guiDisplay.blit((big_font.render(str(round(v2,2))+" m/s", True, (grey))), (465,406))
    guiDisplay.blit((big_font.render(str(round(p2,2))+" kgm/s", True, (grey))), (500,434))
    guiDisplay.blit((big_font.render(str(round(Ek2,2))+" J", True, (grey))), (530,462))

    p_total = p1 + p2 #Total momentum of both objects 
    Ek_total = Ek1 + Ek2 #Total initial kinetic energy of both objects
    collision = Collision(m1, v1, m2, v2, p_total, Ek_total) #Creates object using Collision class that calculates the final velocities + Change_Ek

    if collision_type == 'inelastic': #Prints calculations of inelastic collisions and stores info in database
        final_v1 = collision.getInelastic_Velocity()
        final_v2 = final_v1
        final_Ek = round(collision.getFinal_Ek(final_v1, final_v2), 2)
        change_Ek = collision.getChange_Ek(final_Ek)
        Database(m1,v1,m2,v2,p_total,change_Ek) #Runs database function
        guiDisplay.blit((big_font.render("Inelastic Collision", True, (grey))), (735,125))
    else: #Prints calculation of elastic collisions
        final_v1 = collision.getElastic_Velocity1()
        final_v2 = collision.getElastic_Velocity2()
        final_Ek = round(collision.getFinal_Ek(final_v1, final_v2), 2)
        change_Ek = collision.getChange_Ek(final_Ek)
        guiDisplay.blit((big_font.render("Elastic Collision", True, (grey))), (725,125))

    graph = Graph(x1, x2, Ek_total, final_Ek, maxtime, v1, v2) #Creates graph of kinetic energy against time
    time_taken = graph.getTime() #Finds time taken for objects to collide

    #displays calculations on GUI
    guiDisplay.blit((small_font.render(str(x2)+"m", True, (grey))), (880,210))
    guiDisplay.blit((small_font.render(str(time_taken)+"s", True, (grey))), (850,240))
    guiDisplay.blit((small_font.render(str(final_Ek)+" J", True, (grey))), (850,447.5))
    guiDisplay.blit((small_font.render(str(change_Ek)+" J", True, (grey))), (880,467.5))
    guiDisplay.blit((small_font.render(str(round(p_total,2))+" kgm/s", True, (grey))), (830,370)) #some values still need to be rounded
    guiDisplay.blit((small_font.render(str(round(Ek_total,2))+" J", True, (grey))), (850,390))
    guiDisplay.blit((big_font.render(str(round(final_v1,2))+" m/s", True, (grey))), (240,15))
    guiDisplay.blit((big_font.render(str(round(final_v2,2))+" m/s", True, (grey))), (615,15))

    Animation.moveObjects(time_taken,final_v1,final_v2) #shows simulation of objects colliding
     
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button(720,280,220,55,blue,dark_blue,graph.plotGraph,time_taken) #once calculations have been made and displayed graph button starts working
        guiDisplay.blit((big_font.render("Display Graph", True, (black))), (760,295))
        button(840,10,100,50,blue,dark_blue,start) #reset button that repeats animation of objects
        guiDisplay.blit((big_font.render("Reset", True, (black))), (860,20))      
        pygame.display.update()
        
## MAIN PROGRAM ##
m1 = Validation("Mass of object 1: ","m")
v1 = Validation("Velocity of object 1: ","v1")
m2 = Validation("Mass of object 2: ","m")
v2 = Validation("Velocity of object 2: ","v2") #Runs validation function

collision_type = input("Collision Type(elastic/inelastic): \n") #Determines the type of collision
x1 = 0.0 #initial positon of object 1
x2 = 1000.0 #initial position of object 2
maxtime = 1000 #maximum time of collision to prevent program running forever

pygame.init() #initiates pygame
white = (255,255,255) #defines the colours
black = (0,0,0)
light_blue = (100,149,237)
blue = (61,89,171)
dark_blue = (0,0,139)
green = (0,139,0)
red = (139,0,0)
grey = (51,51,51)

big_font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 22)#difines different types of text (Font,size)
big_font2 = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 22) 
big_font2.set_underline(True) #underlines font
small_font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 13)
small_font2 = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 13) 
small_font2.set_underline(True) #underlines font

guiDisplay = pygame.display.set_mode((950,500)) #creates window of set resolution
guiDisplay.fill(light_blue) #makes background light_blue
pygame.draw.rect(guiDisplay, white, [10, 10, 700, 325])#draws box that will contain animation
pygame.draw.line(guiDisplay, black, (60,260), (660,260),3) #draws platform for objects

pygame.draw.rect(guiDisplay, black, [10, 345, 340, 145], 1) #draws boxes to seperate areas of GUI
pygame.draw.rect(guiDisplay, black, [370, 345, 340, 145], 1) #[xcord,ycord,width,height], thickness
pygame.draw.rect(guiDisplay, black, [720, 345, 220, 67.5], 1)
pygame.draw.rect(guiDisplay, black, [720, 422.5, 220, 67.5], 1)
pygame.draw.rect(guiDisplay, black, [720, 70, 220, 110], 1)
pygame.draw.rect(guiDisplay, black, [720, 190, 220, 80], 1)
Animation = Animation(v1, v2, x2)
Animation.createObjects() #creates objects on GUI that will collide

guiDisplay.blit((big_font2.render("Collision Type", True, (black))), (725,75))#labels display boxes
guiDisplay.blit((small_font.render("Distance between objects:", True, (black))), (725,210))
guiDisplay.blit((small_font.render("Time taken to collide:", True, (black))), (725,240))
guiDisplay.blit((small_font2.render("Before Collision", True, (black))), (725,350))
guiDisplay.blit((small_font.render("Total Momentum:", True, (black))), (725,370))
guiDisplay.blit((small_font.render("Total Kinetic Energy:", True, (black))), (725,390))
guiDisplay.blit((small_font2.render("After Collision", True, (black))), (725,427.5))
guiDisplay.blit((small_font.render("Total Kinetic Energy:", True, (black))), (725,447.5))
guiDisplay.blit((small_font.render("Change in Kinetic Energy:", True, (black))), (725,467.5))
guiDisplay.blit((big_font.render("Object 1 Final Velocity:", True, (black))), (15,15))
guiDisplay.blit((big_font.render("Object 2 Final Velocity:", True, (black))), (390,15))
guiDisplay.blit((big_font2.render("Object 1", True, (black))), (15,350)) 
guiDisplay.blit((big_font2.render("Object 2", True, (black))), (375,350))

messages = ["Mass:", "Velocity:","Momentum:","Kinetic Energy:"]
x = 0
for i in range (0,len(messages)): #used loop for labels that are repeated in multiple boxes
    x = x + 28 #28 is gap between lines of text
    guiDisplay.blit((big_font.render(messages[i], True, (black))), (15,350+x))
    guiDisplay.blit((big_font.render(messages[i], True, (black))), (375,350+x))

pygame.display.set_caption('Momentum Collision Simulation:') #titles window

## MAIN LOOP ##
while True: #finds position of mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
   
    button(720,10,100,50,blue,dark_blue,start)#creates buttons using function
    button(840,10,100,50,blue,dark_blue,start)
    guiDisplay.blit((big_font.render("Start", True, (black))), (745,20)) #labels buttons
    guiDisplay.blit((big_font.render("Reset", True, (black))), (860,20))
    pygame.display.update()
