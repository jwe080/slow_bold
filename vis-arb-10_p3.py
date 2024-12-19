#!/usr/bin/python


from psychopy import visual,core,event,gui,logging
import psychopy_visionscience as psyvi
import sys,os,glob
from datetime import datetime
from numpy import mod,exp
from argparse import ArgumentParser
from random import choice
from random import shuffle

#sys.path.append('NI_USB-6501-master')

#import ni_usb_6501 as ni


# get input parameters
parser = ArgumentParser(description="To make sure I don't mess up experiments, use the command line")

parser.add_argument("-t", "--fixtime", type=float, help="fixation time at start and end in s",default=3)
parser.add_argument("-b", "--btime", type=float, help="block duration (s)",default=15)
parser.add_argument("-l", "--blocks", type=float, help="length of scan in (s)",default=150)
parser.add_argument("-s", "--sk", type=float, help="sigmoid k value",default=1/30.)
parser.add_argument("-o", "--offset", type=float, help="sigmoid offset value ",default=150/2.)
parser.add_argument("-c", "--CL", type=float, help="Contrast level, 0 makes the program do a continous sigmoid, non-zero is a block design ",default=0.7)
parser.add_argument("-f", "--freq", type=float, help="Flicker frequency (Hz)",default=4.)
parser.add_argument("-r", "--frate", type=float, help="Frame rate (Hz)",default=60.)
parser.add_argument("-n", "--loc_num", type=float, help="number of localizer blocks (Hz)",default=0.)
parser.add_argument("-q", "--seq", help="sequence",default='[1,0.05,0.1]')
parser.add_argument("-m", "--hemi", help="",default=0)
parser.add_argument("-a", "--cont",type=float, help="",default=0)
parser.add_argument("-k", "--rest",type=float, help="",default=0)


args = parser.parse_args()

# blocks and reps
fix_time = args.fixtime  # in seconds
btime = args.btime   # length of blocks
blocks = args.blocks   #length of scan in s
loc_num = args.loc_num
## parameters for sigmoid
sk = args.sk #1/2., 1/13.,1/30,1/60.
offset = args.offset
## parameters for block > 0 is block, 0 is sigmoid
CL = args.CL
frate = args.frate  # Hz
freq = args.freq
seq = args.seq[1:-1].split(",")*4
#shuffle(seq)
print(seq)
hemi = args.hemi
cont = args.cont
rest = args.rest

# check on the parallel port
pexist=0
#try:
#   dev = ni.get_adapter()
#   dev.set_io_mode(0b00000000, 0b00000000, 0b11111111)
#   pexist = 1
#except:
#   pexist = 0
#   pass

theDate = datetime.now()

def sigmoid(x,x0,k,a,c):

   y = a/(1 + exp(-k*(x-x0))) + c

   return y

# annoyingly ask the user something about the experiment
expInfo = {"subject":"phtm",'run':42}
dlg = gui.DlgFromDict(expInfo, title='simple JND Exp', fixed=['dateStr'])
if dlg.OK:
   logFn = "arb-s-" + expInfo['subject'] + "-r-" + str(expInfo['run']) + "-" + theDate.strftime("%d%b%y") + ".log"
   print(logFn)
else:
    core.quit()#the user hit cancel so exit

# setup the log file
logging.console.setLevel(logging.CRITICAL)
lastLog=logging.LogFile(logFn,filemode='w', level=logging.INFO)

Timer = core.Clock()
logging.setDefaultClock(Timer)

logging.info("CL - " + str(CL) + " - sk - " + str(sk) + " - " + str(freq) + "--Hz --" + theDate.strftime("%a %d %b %y %R"))


#  --- setup window and stim ---
#win = visual.Window((1280,800.0),allowGUI=True,winType='pyglet',
win = visual.Window((1600,1200.0),allowGUI=True,winType='pyglet',
		monitor='testMonitor', units ='norm', screen=1,fullscr=True)

# setup stim
if int(hemi)==1:
   a = 20
   b = 155.5
else:
   a = 0
   b = 360


chkbd= psyvi.RadialStim(win,tex='sqrXsqr', mask=None,
    pos=(0,0), size=(3,3),
    radialCycles=12, angularCycles=12,
    radialPhase=0, angularPhase=0,
    color=(1,1,1),contrast=1,
    visibleWedge=(a,b) )


instruct = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='Press ''t'' to start',
           alignHoriz = 'center',alignVert='center',
           color='BlanchedAlmond')

fixation = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='+',
           alignHoriz = 'center',alignVert='center',
           color='BlanchedAlmond')

clock = core.Clock()

win.setRecordFrameIntervals(True)
win._refreshThreshold=1/frate+0.002

# draw some stuff and wait
fixation.draw()
win.flip()
event.waitKeys(keyList='t')
if pexist: dev.write_port(2,222)
Timer.reset()
logging.data("Scan triggered start of experiment")
logging.flush()

fixation.draw()
win.flip()
logging.info("Start Fixation started")
core.wait(fix_time)
logging.info("Start Fixation ended")
logging.flush()

chkbd.setAutoDraw(True)
fixation.setColor('BurlyWood')
fixation.setText('+')
fixation.setAutoDraw(True)


# stim will be shown based on the frame number...
# calculate number of frames needed
# blocks*timeperblock/timeperframe

# add in localizer before run?
loc_frames = loc_num*2*btime*frate
print(loc_frames)
nflicker = round(frate/freq)
if loc_num:
   print("localizer")
   for ff in range(int(loc_frames)):
   
      bb = ff/frate
   
      if mod(int(bb/btime),2):
         #print "level 1"
         cl = 0
      else:
         cl = 0.8
         #print "level 2"

      if mod(ff,nflicker) < nflicker/2:
         chkbd.setContrast(cl)
         if (cl > 0) & (pexist > 0): dev.write_port(2,1)
         logging.data("Colour: 1")
         win.flip()
      else:
         chkbd.setContrast(-cl)
         if (cl > 0) & (pexist > 0): dev.write_port(2,2)
         logging.data("Colour: 2")
         win.flip()
   
      if mod(ff,nflicker*freq) == 0:
         logging.data("Loc: " + str(ff/(nflicker*freq)))
         logging.data("Contrast: " + str(cl) )   
         if ( mod(ff,nflicker*freq*btime) == 0) & (pexist > 0):
            dev.write_port(2,int(10+cl*200))

#print rest
if rest:
   for ff in range(int(rest*frate)):
      win.flip()
      if ff ==0:
         logging.data("Resting")
 
nframes = blocks*frate

print(len(seq))
for ff in range(int(nframes)):
   bb = ff/frate

   # decides the contrast level/type of stim
   # > 0 is block stim
   # == 0 is continuous stim
   if CL:
      # now the type of blocks > 0 is constant contrast, < 0 is a sequence of contrasts
      # this could really be replaced by a single condition with a sequence of the same
      # level of contrast... but what can you do, the program was written iteratively 
      if CL > 0:
         if mod(int(bb/btime),2):
            #print "level 1"
            cl = 0
         else:
            cl = CL
            #print "level 2"
      else:
         if mod(int(bb/btime),2):
            cl = 0
            #print "level 1"
         else:
           cl = float(seq[mod(int(bb/btime/2.),len(seq))])
           #if mod(int(bb/btime)) == 1: cl = float(choice(seq))
           #cl = sigmoid(bb,offset,sk,0.05,0)   
            #print "level 2"
   else:
      cl = sigmoid(bb,offset,sk,cont,0)
   logging.flush()

   if mod(ff,nflicker) < nflicker/2:
      chkbd.setContrast(cl)
      if (cl > 0) & (pexist > 0): dev.write_port(2,1)
      logging.data("Colour: 1")
      win.flip()
   else:
      chkbd.setContrast(-cl)
      if (cl > 0) & (pexist>0): dev.write_port(2,2)
      logging.data("Colour: 2")
      win.flip()

   if mod(ff,nflicker*freq) == 0:
      logging.data("Trial: " + str(ff/(nflicker*freq)))
      logging.data("Contrast: " + str(cl) )   
      if (mod(ff,nflicker*freq*btime) == 0 ) & (pexist > 0):
         dev.write_port(2,int(10+cl*200))

   # get the key pressed
   #kp = event.waitKeys(keyList='al')


   #logging.data("Correct key pressed: " + str(corr) )
   logging.flush()

   #key=event.getKeys('q')
   #if key==True: core.quit()

# end loc
if loc_num:
   print("localizer")
   for ff in range(int(loc_frames)):
   
      bb = ff/frate
   
      if mod(int(bb/btime),2):
         #print "level 1"
         cl = 0
      else:
         cl = 0.8
         #print "level 2"

      if mod(ff,nflicker) < nflicker/2:
         chkbd.setContrast(cl)
         if (cl > 0 ) & ( pexist > 0): dev.write_port(2,1)
         logging.data("Colour: 1")
         win.flip()
      else:
         chkbd.setContrast(-cl)
         if (cl > 0) & (pexist > 0): dev.write_port(2,2)
         logging.data("Colour: 2")
         win.flip()
   
      if mod(ff,nflicker*freq) == 0:
         logging.data("Loc: " + str(ff/(nflicker*freq)))
         logging.data("Contrast: " + str(cl) )   
         if ( mod(ff,nflicker*freq*btime) == 0 ) & ( pexist > 0 ):
            dev.write_port(2,int(10+cl*200))

chkbd.setAutoDraw(False)

fixation.setColor('white')
fixation.draw()
win.flip()
logging.info("End Fixation started")
core.wait(fix_time)
logging.info("End Fixation ended")
logging.flush()

core.quit()
