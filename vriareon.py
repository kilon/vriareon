#! /usr/bin/env python

""" VRIAREON version 0.01 . Copyright 2009 by Kilon. All rules of GPL licence apply.
MIDI app that using MIDI CC transmits multi point envelops to hardware synthesizers""" 

import sys, pygame
from pygame.locals import *
from pygame.gfxdraw import *

pygame.init()

screen = pygame.display.set_mode((1000,500))
print "Display mode has been set"
pygame.display.set_caption('Vriareon 0.01 Copyright by Kilon ', 'Vriareon 0.01')
print "Pygame version : ", pygame.version.ver
class menv:
    def __init__(self):
        
        """ Definition of all variables used by the class. """
       
        # self.menv contains the multienvelope information.
        # multienvelope is a collection of 8 multipoint / multisegment envelopes.
        # This dictionary is the collection of 9 keys. 
        # 'selected' : Which of the 8 envelopes is selected for editing 
        # 1-8 : the 8 envelopes with each envelope containing the following keys
        # -------------------------------------------------------------------------
        # 
        # 'data'          : this the list  containg the values of the envelope as they are sent via MIDI
        #                   made by x and y axis. X axis is time in milliseconds . Y axis is the value of 
        #                   the parameter (0-127)
        #
        # 'enabled'       : is the envelope enabled (true / false)
        # 'mode'          : The mode of envelope playback. 
        #          'oneshot' envelope is played once. If a note is presssed before it ends, it is retriggered
        #          'freerun' envelope is triggered once and wont be retriggered till it ends
        #          'loop', the envelope ,while the note is keep being pressed, loops the section between 'ae' 
        #                  and 'rs'
        # 'duration'       : the duration of envelope in milliseconds
        # 'midi'           : the type of midi protocol used for the envelope. 'cc' or 'nrpn' .
        # 'midi_channel'   : Midi channel. 
        # 'start_key'      : along with 'end_key' , defines the range of keys assigned to the envelope
        # 'start_velocity' : along with 'end_velocity' , defines the range of velocity assigned 
        # 'ae'             : Attack end. The final point that defines the end of Attack section
        # 'rs'             : Release start. The first point of Release section.  
        
     
        self.menv = {'selected':1,
                     1: {'data':[[0,0],[100,100],[150,27],[300,127],[870,0]], 
                         'enabled':True , 
                         'mode':"oneshot",
                         'duration':1000,
                         'midi':"cc",
                         'midi_channel':1,
                         'start_key':"C0",
                         'end_key':"C5",
                         'start_velocity':0,
                         'end_velocity':127,
                         'ae':2, 
                         'rs':3},
                         
                     2:{'data':[[0,0],[100,100],[150,27],[300,127],[870,0]], 
                         'enabled':False , 
                         'mode':"oneshot",
                         'duration':1000,
                         'midi':"cc",
                         'midi_channel':1,
                         'start_key':"C0",
                         'end_key':"C5",
                         'start_velocity':0,
                         'end_velocity':127,
                         'ae':2, 
                         'rs':3},
                         
                     3:{'data':[[0,0],[100,100],[150,27],[300,127],[870,0]], 
                         'enabled':False , 
                         'mode':"oneshot",
                         'duration':1000,
                         'midi':"cc",
                         'midi_channel':1,
                         'start_key':"C0",
                         'end_key':"C5",
                         'start_velocity':0,
                         'end_velocity':127,
                         'ae':2, 
                         'rs':3},
                         
                     4:{'data':[[0,0],[100,100],[150,27],[300,127],[870,0]], 
                         'enabled':False , 
                         'mode':"oneshot",
                         'duration':1000,
                         'midi':"cc",
                         'midi_channel':1,
                         'start_key':"C0",
                         'end_key':"C5",
                         'start_velocity':0,
                         'end_velocity':127,
                         'ae':2, 
                         'rs':3},
                         
                     5:{'data':[[0,0],[100,100],[150,27],[300,127],[870,0]], 
                         'enabled':False , 
                         'mode':"oneshot",
                         'duration':1000,
                         'midi':"cc",
                         'midi_channel':1,
                         'start_key':"C0",
                         'end_key':"C5",
                         'start_velocity':0,
                         'end_velocity':127,
                         'ae':2, 
                         'rs':3},
                         
                     6:{'data':[[0,0],[100,100],[150,27],[300,127],[870,0]], 
                         'enabled':False , 
                         'mode':"oneshot",
                         'duration':1000,
                         'midi':"cc",
                         'midi_channel':1,
                         'start_key':"C0",
                         'end_key':"C5",
                         'start_velocity':0,
                         'end_velocity':127,
                         'ae':2, 
                         'rs':3},
                         
                     7:{'data':[[0,0],[100,100],[150,27],[300,127],[870,0]], 
                         'enabled':False , 
                         'mode':"oneshot",
                         'duration':1000,
                         'midi':"cc",
                         'midi_channel':1,
                         'start_key':"C0",
                         'end_key':"C5",
                         'start_velocity':0,
                         'end_velocity':127,
                         'ae':2, 
                         'rs':3},
                         
                     8:{'data':[[0,0],[100,100],[150,27],[300,127],[870,0]], 
                         'enabled':False , 
                         'mode':"oneshot",
                         'duration':1000,
                         'midi':"cc",
                         'midi_channel':1,
                         'start_key':"C0",
                         'end_key':"C5",
                         'start_velocity':0,
                         'end_velocity':127,
                         'ae':2, 
                         'rs':3}}
        
        # the color of the line drawn for the multienvelope
        self.linecolor=pygame.Color(255, 0, 0) 
        
        # background color
        self.backcolor=pygame.Color(0, 0, 50)  
        
        # the middlebar is the bar that defines the center of the box and the focus point, 
        # this is its color
        self.middlebar_color=pygame.Color(50,0,50)
                 
        # this is the multipoint envelope as it appears on the screen taking into account zoom 
        # and pan factor, as well as zoom compensation . X and Y are the screen coordinates
        self.drawn=[]
        
        # first is whether there is a point drag, second on which point there is a drag 
        self.mousedrag=[0,0] 
        
        # indicates whether it entered or not in zoom / pan mode of the box
        self.zoomNpan=0 
        
        # used by zoom n pan to compare how the mouse moved 
        # and decide whether a pan or a zoom will be performed
        self.StoredPos=[0,0] 
        
        # should the programm stop ? 0 = No
        self.stop=0 
        
        # the box which inside the multienvelope is drawn
        self.box = (30,100,870,128) 
        
        # the zoom applied to the multi envelope box. The zoom can be applied only on the x axis.
        self.zoom=1 
        
        # the pan applied from the user to focus in a specific area.
        # The middle bar is always the center of focus. Only for the x axis.
        self.pan=0  
        
        # the middle of the box inside which the multipoint envelop is drawn and 
        # where the middle bar is located.
        self.box_middle=int(round((self.box[2]/2)+self.box[0])) 
        
        # this a pan applied from the program to comp(ensate) for the move of the points 
        # because of zoom in/zoom out and keep the area of focus centered even if zoom is applied.
        # Zoom is applied by multipling x coordinates of the multienvelope's points by the zoom factor,
        # thus all points are moved forward because of the multiplication as well as spread apart.
        # This is a pan to bring all points back after the zoom in order for the area of focus to be 
        # retained in the the center of the box , on the middle bar. This is always zero of course 
        # if there is no zoom and thus is seperate from menv.pan which does not depend on the zoom.
        self.comp=0
        
        #background image containing all background gui elements 
        self.backgr=pygame.image.load("test3.jpg") 
        
        # the rect of the background image which takes the whole window.
        self.backgr_rect=self.backgr.get_rect()
        
        self.countloops=0
        self.average_loop=0
        self.loops=0   

# Draws the  multipoint envelope 
    def drawenv(self): 
        env=self.menv[self.menv['selected']]['data']
        numberofpoints=len(env)
        self.drawn=[]
        screen.fill(self.backcolor)
                
        for x in range(0,numberofpoints-1):
            
            # this the formula that computes the menv.drawn which is the envelop as it is drawn
            # on the screen. It takes for the x cordinates , the x data of the point, the pan,
            # the zoom factor and zoom compensation. Y because is not affected by zoom or pan 
            # is alot easier to compute. It also computes the next point for drawing a straight 
            # line as well as the circle handlers for each point which handle the move of points. 
            ax=int(round(((env[x][0]+self.pan+self.box[0])*self.zoom)+self.comp))
            ay=(self.box[3]+self.box[1])- env[x][1]
            bx=int(round(((env[x+1][0]+self.pan+self.box[0])*self.zoom)+self.comp))
            by=(self.box[3]+self.box[1])-env[x+1][1]
            pos1=(ax,ay)
            pos2=(bx,by)
            
            self.drawn.insert(x, list(pos1)) # insert the values 
                
            if x==numberofpoints-2:
                self.drawn.insert(x+1, list(pos2)) # add also the last point as well
            
            pygame.draw.aaline(screen, self.linecolor, pos1, pos2 , 1)
            #pygame.draw.aaline(screen, self.linecolor, (pos1[0],pos1[1]-1), (pos2[0],pos2[1]-1 ), 1)
                
            if x < len(env)-2:
                # use the code bellow if gfxdraw does not work properly
                # pygame.draw.circle(screen, (0,0,200),pos2, 10,1 )
                aacircle(screen, pos2[0], pos2[1],10, (0,0,200))
            
        # this draws the box    
        pygame.draw.rect(screen,pygame.Color(0,100,0), self.box,1)
        
        # this draws the middle bar
        pygame.draw.aaline(screen,self.middlebar_color,[round(self.box_middle),self.box[1]],[round(self.box_middle),(self.box[1]+self.box[3])],1)           
                
        # update only what is inside the box.
        pygame.display.update(self.box)
        
# gui is responsible for the gui functionality, including handling mouse and keyboard events 
    def gui(self, event):
        env=self.menv[self.menv['selected']]['data']    
        start_time=pygame.time.get_ticks()
        
        # after a maximise from minimise or when the window regain focus , redraw the entire window         
        if event.type== pygame.ACTIVEEVENT and event.state==2 and event.gain==1:
            draw_screen()
    
        mpos = pygame.mouse.get_pos()
        pos = list(mpos)
        
        # it is 1 when a point is moved/inserted/deleted , only when 0 zoom in/out and pan can be applied 
        eventaction=0
        
        # terminate the loop when esc key is pressed or user exits
        if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)  : self.stop=1
    
        for y in range(0,len(self.drawn)-1) :
            
            xpoint=self.drawn[y][0]
            ypoint=self.drawn[y][1]
            
            # detect drag giving +-10 pixels fallout
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (pos[0]==xpoint or (pos[0] < xpoint+10 and pos[0]> xpoint-10)) and (pos[1]==ypoint or (pos[1] < ypoint+10 and pos[1]> ypoint-10)) : 
                self.mousedrag=[1,y] # check whether user clicks on a circle control of points, then enter drag mode
                eventaction=1
                
            # delete point with right click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and (pos[0]==xpoint or (pos[0] < xpoint+10 and pos[0]> xpoint-10)) and (pos[1]==ypoint or (pos[1] < ypoint+10 and pos[1]> ypoint-10)) : 
                eventaction=1
                if len(env)>3:
                  
                    self.menv[self.menv['selected']]['data'].pop(y)
                    self.drawenv()
          
        # define which point is being draged and drag it            
        if event.type == pygame.MOUSEMOTION and self.mousedrag[0]==1: # move point between 2 neighbor points
            mdp=self.mousedrag[1]
            eventaction=1    
            
                       
            # check that the point is draged between the space of its two neighbor points 
            # This is because of the nature of the envelope. It meaningless for the next point to occupy a 
            # smaller x coordinate than the previous point. That would mean that the parameter controlled by
            # the envelope will have to go back in time as , x axis represents time. Of course that can not 
            # happen so I limit the move so that a point cannot move before the previous point and after 
            # the next one . I check also that is limited inside the  box
            # Warning the x2,y2 of box  is relative to the first x1,y1 (see pygame documentation)
            # that is why i add x1+x2 to find the absolute x end of the box 
            # and y1+y2 to find the absolute y end of the box 
            
            if pos[0] < self.drawn[mdp+1][0] and pos[0] > self.drawn[mdp-1][0]:
        
                if pos[0] > self.box[0] and pos[0] < self.box[2]+self.box[0] and pos[1] > self.box[1] and pos[1] < self.box[3]+self.box[1] : 
                    
                    self.menv[self.menv['selected']]['data'][mdp][0]=int(round((((pos[0]-self.comp )/self.zoom))-self.box[0]-self.pan))
                    self.menv[self.menv['selected']]['data'][mdp][1]=((self.box[3]+self.box[1])-pos[1])
                 
                    self.drawenv()
                                    
        # detect whether drag has finished
        if event.type == pygame.MOUSEBUTTONUP and event.button ==1 and self.mousedrag[0]==1 :
        
            self.mousedrag[0]=0
            eventaction=1
        
        # detect point insertion with left click with a 5 pixel radius falout   
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and self.mousedrag[0]==0:
                    
                yscan=0
                xscan=0
                PosHit=[0,0]
                circlecolor=(0,0,200)
                
                linewashit=0
                
                # basically I scan in y and x axis up to 5 pixels to see if the user clicked near or  
                # on the line of the multipoint envelop, by detecting the coloration of the line.
                # If he did I add one more point to the envelope and redraw it. 
                for yscan in range(-5,5):
                
                    for xscan in range(-5,5):
                        
                        if pos[0]+xscan >= self.box[0] and pos[0]+xscan <= (self.box[0]+self.box[2]) and pos[1]+yscan >=self.box[1] and pos[1] <= (self.box[1]+self.box[3]) :
                    
                            pixelcol=screen.get_at((pos[0]+xscan,pos[1]+yscan))
                            
                            if pixelcol != circlecolor and pixelcol !=self.backcolor and pixelcol != self.middlebar_color:
                            
                                linewashit=1
                                eventaction=1
                                PosHit=[(pos[0]+xscan),(pos[1]+yscan)]
                            
                if linewashit == 1 :
                  
                    for x in range (0,len(env)):
                                
                                if PosHit[0] < self.drawn[x][0]-10 and PosHit[0]> self.drawn[x-1][0]+10   :
                                
                                    insPoint=[int(round((((pos[0]-self.comp )/self.zoom))-self.box[0]-self.pan)) , (self.box[3]-(PosHit[1]-self.box[1]))]
                                    self.menv[self.menv['selected']]['data'].insert(x, insPoint)
                                    self.drawenv()
    
                                    break
    
        # Detect and enter ZoomNpan mode
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and eventaction==0 and ((screen.get_at((pos[0] ,pos[1])))==self.backcolor or (screen.get_at((pos[0] ,pos[1])))==self.middlebar_color ) and pos[0]>self.box[0] and pos[0]<self.box[0]+self.box[2] and pos[1] > self.box[1] and pos[1] < self.box[1]+self.box[3]:
            self.StoredPos=pos
            self.zoomNpan=1
            numberofpoints=len(env)
            
            # this stores the location of the first point of the multipoint envelope on the screen
            first_point = int(round(((env[0][0]+self.pan+self.box[0])*self.zoom)+self.comp)) 
            
            # this stores the location of the last point of the multipoint envelope on the screen
            last_point = int(round(((env[numberofpoints-1][0]+self.pan+self.box[0])*self.zoom)+self.comp))
            
            # make sure that the pan is not infinite. The pan is limited in the range between first and last
            # point of multi point envelope.Pan beyond that range is meaningless. 
            if  self.StoredPos[0]> first_point  and  self.StoredPos[0]< last_point  : 
                self.pan = self.pan+(round((self.box_middle -self.StoredPos[0])/self.zoom))
                
            # if you try to pan beyond the first point then the pan will be limited to the first point
            elif self.StoredPos[0]< first_point  : 
                self.pan= self.pan + (round((self.box_middle -first_point)/self.zoom))
                
            # the same as above but for the last point this time
            elif self.StoredPos[0] > last_point : 
                self.pan= self.pan + (round((self.box_middle -last_point)/self.zoom))
               
            self.drawenv()
            
        # zoom out and zoom in
        if event.type == pygame.MOUSEMOTION and self.zoomNpan == 1 :
            
            if self.StoredPos[1]+10<pos[1] and self.zoom > 1 : # zoom out
                
                self.zoom=self.zoom-0.1
                
                self.comp=1
                
                # the zoom compensation is computed by calculating how far a point has moved from the 
                # middle bar which is the center of focus, taking zoom factor always in consideration.
                # zoom compensation has always a negative value because it is responsible for moving
                # the points back to the focus center (middle bar ) after a zoom . It wont matter if 
                # it is a zoom in or zoom out as in both cases , the points are always multiplied by 
                # zoom factor. Of course in zoom in the compensation increases , and in zoom out decreases
                # until it reaches zero at zoom zero (technically zoom = 1 ). 
                
                if self.comp > 0 :
                    self.comp=-((self.box_middle*self.zoom)-self.box_middle)
                    
                elif self.comp < 0 :
                    self.comp=((self.box_middle*self.zoom)-self.box_middle)
                    
            if self.StoredPos[1]-10>pos[1] and self.zoom < 5.9 : # zoom in 
                self.zoom=self.zoom+0.1
                self.comp=1
                
                if self.comp > 0 :
                    self.comp=-((self.box_middle*self.zoom)-self.box_middle)
                
                elif self.comp < 0 : 
                    self.comp=((self.box_middle*self._zoom)-self.box_middle)
                
            self.drawenv()
        
        # right click resets pan and zoom                                     
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and eventaction==0 and ((screen.get_at((pos[0] ,pos[1])))==self.backcolor or (screen.get_at((pos[0] ,pos[1])))==self.middlebar_color ) and pos[0]>self.box[0] and pos[0]<self.box[0]+self.box[2] and pos[1] > self.box[1] and pos[1] < self.box[1]+self.box[3]:
            self.pan=0
            self.zoom=1
            self.comp=0
            self.drawenv()
            
        # once left mouse button is released exit ZoomNpan mode    
        if event.type == pygame.MOUSEBUTTONUP and self.zoomNpan==1:
            self.zoomNpan=0   
                   
        if eventaction==1 : 
            eventaction=0 
        end_time=pygame.time.get_ticks()
        loop_duration=end_time-start_time
        if loop_duration > 1 :
            print "Loop duration : " , loop_duration 
            self.countloops=self.countloops+1
            self.loops=self.loops+loop_duration
            self.average_loop= self.loops/self.countloops
            print "average loop :",self.average_loop
                     

multienv=menv()

# draws the entire window's GUI    
def draw_screen():
    screen.fill(multienv.backcolor)
    screen.blit(multienv.backgr,multienv.backgr_rect)

    pygame.display.flip()

    multienv.drawenv()
draw_screen()

# main loop
while multienv.stop== 0 :
    for event in pygame.event.get():
        multienv.gui(event)
        
    # use this to limit the CPU load of the while loop, 
    # the less the wait the faster the loop runs and thus the more cpu it consumes   
    pygame.time.wait(10) 
