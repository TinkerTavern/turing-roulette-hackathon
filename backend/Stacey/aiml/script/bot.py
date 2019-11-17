"""
This script demonstrates how to create a bare-bones, fully functional
chatbot using PyAIML.
"""
from __future__ import print_function

import os.path
import sys
import argparse
import io

import aiml

class smarter():


    def __init__(self, mode):

        if mode == "standard":
            chdir = os.path.join( aiml.__path__[0],'botdata','standard' )
            kern.bootstrap(learnFiles="startup.xml", commands="load aiml b",
                           chdir=chdir)
        else:
            chdir = os.path.join( aiml.__path__[0],'botdata','alice' )
            kern.bootstrap(learnFiles="startup.xml", commands="load alice",
                           chdir=chdir)

    def sendMessage(self, message):
        return kern.respond(message)

