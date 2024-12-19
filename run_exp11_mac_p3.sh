#!/bin/bash

#echo " -- This would be a Menu --
#1)  cont
#2)  20 s block 100% contrast
#3)  block 50% contrast
#4)  block 30% contrast
#5)  block 10% contrast
#6)  Sigmoid -1/13 
#7)  Sigmoid -1/60
#8)  Sigmoid -1/40 
#9)  Sigmoid 1/40 
#"

menu_arr=( "intentionally blank "
"contrast localization"
"long block full contrast"
"long block full contrast"
"long block 20% contrast "
"long block 5% contrast "
"long block 2.5% contrast"
"long block 3/4 shift @ 20% contrast"
"long block 1/3 shift @ 20% contrast"
"long block ramp -1/40"
"long block ramp -1/60"
"tap 1"
"tap 2"
"long block ramp -1/40 5%"
"long block ramp -1/60 5%"
)

echo " -- This is a Menu --"
for ii in ${!menu_arr[*]}
do

   if [ $ii -gt 0 ] ; then
      echo "$ii) ${menu_arr[$ii]}"
   fi

done

# ${#arr[*]}


read -p "Choose something to do:  " val



case $val in
   1) echo ${menu_arr[1]}
      python vis-arb-10_p3.py -l 420 -b 15 -t 8 -n 0 -q '[0.05,1,0.2,0.025]' -c -1 -m 0
   ;;
   2) echo ${menu_arr[2]}
      python vis-arb-10_p3.py -t 8 -c 0 -s `ccalc -100.` -f 4 -l 300 -o 150 -m 0 -b 15 -n 2
   ;;
   3) echo ${menu_arr[3]}
      python vis-arb-10_p3.py -t 8 -c 0 -s `ccalc -100.` -f 4 -l 300 -o 150 -m 0 -b 15 -n 2 -a 1
   ;;
   4) echo ${menu_arr[4]}
      python vis-arb-10_p3.py -t 8 -c 0 -s `ccalc -100.` -f 4 -l 300 -o 150 -m 0 -b 15 -n 2 -a 0.2
   ;;
   5) echo ${menu_arr[5]}
      python vis-arb-10_p3.py -t 8 -c 0 -s `ccalc -100.` -f 4 -l 300 -o 150 -m 0 -b 15 -n 2 -a 0.05
   ;;
   6) echo ${menu_arr[6]}
      python vis-arb-10_p3.py -t 8 -c 0 -s `ccalc -100.` -f 4 -l 300 -o 150 -m 0 -b 15 -n 2 -a 0.025
   ;;
   7) echo ${menu_arr[7]}
      python vis-arb-10_p3.py -t 8 -c 0 -s `ccalc -100.` -f 4 -l 300 -o 225 -m 0 -b 15 -n 2 -a 0.20
   ;;
   8) echo ${menu_arr[8]}
      python vis-arb-10_p3.py -t 8 -c 0 -s `ccalc -100.` -f 4 -l 300 -o 100 -m 0 -b 15 -n 2 -a 0.20
   ;;
   9) echo ${menu_arr[9]}
      python vis-arb-10_p3.py -t 8 -c 0 -s `ccalc -1/20.` -f 4 -l 300 -o 100 -m 0 -b 15 -n 2 -a 0.20
   ;;
   10) echo ${menu_arr[10]}
      python vis-arb-10_p3.py -t 8 -c 0 -s `ccalc -1/60.` -f 4 -l 300 -o 100 -m 0 -b 15 -n 2 -a 0.20
   ;;
   11) echo ${menu_arr[11]}
      python tap-task4.py -t 8 -b 60 -l 5 -f '[0,1,0,2,0]' -q '[1,2,1,3]' -n 0 -r 60
   ;;
   12) echo ${menu_arr[12]}
      python tap-task4.py -t 8 -b 60 -l 4 -f '[0,1,2,0]' -q '[1,2,1,3]' -n 0 -r 60
   ;;
   13) echo ${menu_arr[10]}
      python vis-arb-10_p3.py -t 8 -c 0 -s `ccalc -1/60.` -f 4 -l 300 -o 100 -m 0 -b 15 -n 2 -a 0.05
   ;;
   14) echo ${menu_arr[10]}
      python vis-arb-10_p3.py -t 8 -c 0 -s `ccalc -1/20.` -f 4 -l 300 -o 100 -m 0 -b 15 -n 2 -a 0.05
   ;;

esac


#python vis-arb-3.py -t 8 -c 0 -s `ccalc -1/13` -f 4 -l 120 -o 60
#python vis-arb-3.py -t 8 -b 15 -l 120 -c 0.7 -f 4

#vis-arb-3.py -t 8 -b 15 [-l BLOCKS] [-s SK]
#                    [-o OFFSET] [-c CL] [-f FREQ] [-r FRATE]

