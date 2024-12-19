# slow_bold
stimuli scripts for 2015 slow bold paper

https://pmc.ncbi.nlm.nih.gov/articles/PMC4262662/

The main bash script (run_exp11_mac_p3.sh) provides menu options as a wrapper for running
the psychopy based stimuli scripts (vis-arb-10_p3.py, tap-task4.py).  Options used for
the paper were 4 and probably 9 (but maybe 10, they are similar). They should run using 
the python environment specified in stim_env.yml.

Importantly, after intial run naming menu (for the log file name), the tasks are set up to start
on a keyboard 't' trigger or you will be looking at a fixation cross for a long time.  There was
no built in exit key, you'll have to use the system appropriate force quit (opt-cmd-esc on a mac).

