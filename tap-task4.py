#!/usr/bin/python


from psychopy import visual,core,event,gui,logging
import psychopy_visionscience as psyvi
import os,glob,sys
from datetime import datetime
from numpy import mod,exp
from argparse import ArgumentParser

#sys.path.append('NI_USB-6501-master')

#import ni_usb_6501 as ni

parser = ArgumentParser(description="To make sure I don't mess up experiments, use the command line")


parser.add_argument("-t", "--fixtime", type=float, help="fixation time at start and end in s",default=3)
parser.add_argument("-b", "--btime", type=float, help="block duration (s)",default=15)
parser.add_argument("-l", "--blocks", type=float, help="length of scan in (s)",default=150)
parser.add_argument("-s", "--sk", type=float, help="sigmoid k value",default=1/30.)
parser.add_argument("-o", "--offset", type=float, help="sigmoid offset value ",default=150/2.)
parser.add_argument("-c", "--CL", type=float, help="Contrast level, 0 makes the program do a continous sigmoid, non-zero is a block design ",default=0.7)
parser.add_argument("-f", "--freq", help="Flicker frequency (Hz)",default='[1,0,2,0]')
parser.add_argument("-r", "--frate", type=float, help="Frame rate (Hz)",default=60.)
parser.add_argument("-n", "--loc_num", type=float, help="number of localizer blocks (Hz)",default=0.)
parser.add_argument("-q", "--seq", help="sequence",default='[1,2,1,3]')


# check on the parallel port
pexist=0
#try:
#   dev = ni.get_adapter()
#   dev.set_io_mode(0b00000000, 0b00000000, 0b11111111)
#   pexist = 1
#except:
#   pexist = 0
#   pass
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
freq = args.freq[1:-1].split(",")
seq = args.seq[1:-1].split(",")

print(freq)
print(args.freq)

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
		monitor='testMonitor', units ='norm', screen=1, fullscr=True)

# setup stim
chkbd= psyvi.RadialStim(win,tex='sqrXsqr', mask=None,
    pos=(0,0), size=(3,3),
    radialCycles=12, angularCycles=12,
    radialPhase=0, angularPhase=0,
    color=(1,1,1),contrast=1)


instruct = visual.TextStim(win, 
           units='norm',
           pos=(0, 0), text='Press ''t'' to start',
           alignHoriz = 'center',alignVert='center',
           color='BlanchedAlmond')

response = visual.TextStim(win, 
           units='norm',
           pos=(0, -0.05), text='Press ''s'' to start',
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

fixation.setColor('BurlyWood')
fixation.setText('+')


# stim will be shown based on the frame number...
# calculate number of frames needed
# blocks*timeperblock/timeperframe

# add in localizer before run?
chkbd.setAutoDraw(True)
fixation.setAutoDraw(True)
ltime =15
lfreq = 4
loc_frames = loc_num*2*ltime*frate
print(loc_frames)
nflicker = round(frate/lfreq)
print(nflicker)
if loc_num:
   print("localizer")
   for ff in range(int(loc_frames)):
   
      bb = ff/frate
   
      if mod(int(bb/ltime),2):
         print("level 1")
         cl = 0
      else:
         cl = 0.2
         print("level 2")

      if mod(ff,nflicker) < nflicker/2:
         chkbd.setContrast(cl)
         if ( cl > 0 ) & (pexist > 0): dev.write_port(2,1)
         logging.data("Colour: 1")
         win.flip()
      else:
         chkbd.setContrast(-cl)
         if ( cl > 0 ) & ( pexist > 0 ): dev.write_port(2,2)
         logging.data("Colour: 2")
         win.flip()
   
      if mod(ff,nflicker*lfreq) == 0:
         logging.data("Loc: " + str(ff/(nflicker*lfreq)))
         logging.data("Contrast: " + str(cl) )   
         if (mod(ff,nflicker*lfreq*ltime) == 0) & (pexist> 0):
            dev.write_port(2,int(10+cl*200))

nframes = blocks*btime*frate
#nframes = blocks*frate

# for a given sequence of numbers show the numbers at a particular rate
#seq = [1,2,3,4]
nseq = len(seq)
rdur = 0
chkbd.setAutoDraw(False)
fixation.setAutoDraw(False)
#response.setAutoDraw(True)

nflick=0
val=""
instruct.setAutoDraw(True)
for ff in range(int(nframes)):
   bb = ff/frate

   flick = int(freq[int(bb/btime)])

   if flick:
      nflick = frate/float(flick)
      if mod(ff,nflick) < nflick - nflick*0.2:
         val = seq[mod(int(ff/nflick),nseq)]
         instruct.setText(val)
         if pexist>0: dev.write_port(2,int(val))

         if mod(ff,nflick) == 0:
            logging.data("Trial: " + str(ff/(nflick)))
            logging.data("val: " + str(val) )   
            if pexist>0: dev.write_port(2,int(val))
      else:
         instruct.setText(' ')
         instruct.setColor('white')
   else:
      instruct.setText('+')
      instruct.setColor('white')


   keyp  = event.getKeys()
   if keyp:
      logging.data("resp: " + keyp[0] )
      logging.data("respval: " + val )
      if keyp[0] != 't':
         #response.setText('.')
         if (keyp[0] == val) & (flick > 0):
            instruct.setColor('green')
         else:
            instruct.setColor('red')
      print(keyp)
      rdur = ff + nflick*0.2
   #else:
      #if ff > rdur: response.setText('')   
   # get the key pressed
   #kp = event.waitKeys(keyList='al')

   win.flip()

   #logging.data("Correct key pressed: " + str(corr) )
   logging.flush()

instruct.setAutoDraw(False)
chkbd.setAutoDraw(True)
fixation.setAutoDraw(True)

# end loc
if loc_num:
   print("localizer")
   for ff in range(int(loc_frames)):
   
      bb = ff/frate
   
      if mod(int(bb/ltime),2):
         print("level 1")
         cl = 0
      else:
         cl = 0.2
         print("level 2")

      if mod(ff,nflicker) < nflicker/2:
         chkbd.setContrast(cl)
         if ( cl > 0) & (pexist > 0) : dev.write_port(2,1)
         logging.data("Colour: 1")
         win.flip()
      else:
         chkbd.setContrast(-cl)
         if ( cl > 0 )  & (pexist >0 ): dev.write_port(2,2)
         logging.data("Colour: 2")
         win.flip()
   
      if mod(ff,nflicker*lfreq) == 0:
         logging.data("Loc: " + str(ff/(nflicker*lfreq)))
         logging.data("Contrast: " + str(cl) )   
         if (mod(ff,nflicker*lfreq*ltime) == 0 ) & (pexist>0):
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
