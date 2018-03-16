#!/usr/bin/env python
#------------------------------------------------------------
#    FILE: gensyslog.py
# PURPOSE: genmon.py support program to allow SMS (txt messages)
# to be sent when the generator status changes
#
#  AUTHOR: Jason G Yates
#    DATE: 29-Nov-2017
#
# MODIFICATIONS:
#------------------------------------------------------------

import datetime, time, sys, signal, os, threading, socket
import atexit
import mynotify, mylog
try:
    from ConfigParser import RawConfigParser
except ImportError as e:
    from configparser import RawConfigParser

import syslog


#----------  Signal Handler ------------------------------------------
def signal_handler(signal, frame):

    GenNotify.Close()
    sys.exit(0)

#----------  OnRun ------------------------------------------
def OnRun(Active):

    if Active:
        print "Generator Running"
        SendNotice("Generator Running")
    else:
        print "Generator Running End"

#----------  OnRunManual ------------------------------------------
def OnRunManual(Active):

    if Active:
        print "Generator Running in Manual Mode"
        SendNotice("Generator Running in Manual Mode")
    else:
        print "Generator Running in Manual Mode End"

#----------  OnExercise ------------------------------------------
def OnExercise(Active):

    if Active:
        print "Generator Exercising"
        SendNotice("Generator Exercising")
    else:
        print "Generator Exercising End"

#----------  OnReady ------------------------------------------
def OnReady(Active):

    if Active:
        print "Generator Ready"
        SendNotice("Generator Ready")
    else:
        print "Generator Ready End"

#----------  OnOff ------------------------------------------
def OnOff(Active):

    if Active:
        print "Generator Off"
        SendNotice("Generator Off")
    else:
        print "Generator Off End"

#----------  OnManual ------------------------------------------
def OnManual(Active):

    if Active:
        print "Generator Manual"
        SendNotice("Generator Manual")
    else:
        print "Generator Manual End"

#----------  OnAlarm ------------------------------------------
def OnAlarm(Active):

    if Active:
        print "Generator Alarm"
        SendNotice("Generator Alarm")
    else:
        print "Generator Alarm End"

#----------  OnService ------------------------------------------
def OnService(Active):

    if Active:
        print "Generator Service Due"
        SendNotice("Generator Service Due")
    else:
        print "Generator Servcie Due End"

#----------  SendNotice ------------------------------------------
def SendNotice(Message):

    try:

        syslog.openlog("genmon")
        syslog.syslog("%s" % Message)
        syslog.closelog()

    except Exception as e1:
        log.error("Error: " + str(e1))
        print ("Error: " + str(e1))

#------------------- Command-line interface for gengpio -----------------#
if __name__=='__main__': # usage program.py [server_address]
    address='127.0.0.1' if len(sys.argv)<2 else sys.argv[1]

    # Set the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    try:
        log = mylog.SetupLogger("client", "/var/log/gensyslog.log")

        GenNotify = mynotify.GenNotify(
                                        host = address,
                                        onready = OnReady,
                                        onexercise = OnExercise,
                                        onrun = OnRun,
                                        onrunmanual = OnRunManual,
                                        onalarm = OnAlarm,
                                        onservice = OnService,
                                        onoff = OnOff,
                                        onmanual = OnManual,
                                        log = log)

        while True:
            time.sleep(1)

    except Exception as e1:
        log.error("Error: " + str(e1))
        print ("Error: " + str(e1))

