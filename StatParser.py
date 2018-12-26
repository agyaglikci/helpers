#!/usr/bin/python

import os 

RUN_TEST = False

class StatParser(object):
    
    def __init__(self, file_path, verbose=False):
        
        self.verbose = verbose
        self.stats_dict={
            "stats_file": (file_path, "Path to stats file")
        }

        # Check if file exists 
        if not os.path.isfile(file_path):
            # print "No file at " + file_path + "!"
            return None

        if self.verbose: 
            print "# Parsing " + file_path        
        
        with open(file_path) as f:
            for line in f.readlines():
                lineparts = line.strip().split("#")
                infoparts = lineparts[0].strip().split()
                desc = safeget(lineparts,1,defval="")
                name = safeget(infoparts,0).replace("ramulator.","")
                value= float(safeget(infoparts,1))
                if name in self.stats_dict:
                    if self.verbose:
                        print "#  Repeating stat name: " + name,
                        print " was " + str(self.get_value(name)),
                        print " is " + str(value),
                        print " means " + desc 
                self.stats_dict[name] = (value, desc.strip())

    def get_value(self, name):
        if name in self.stats_dict:
            return self.stats_dict[name][0]
        else :
            if self.verbose: 
                print "#  Could not found " + name 
            return -1

    def get_desc(self, name):
        if name in self.stats_dict:
            return self.stats_dict[name][1]  
        else :
            return ""

    def dump_stats(self):
        for name in self.stats_dict:
            print name + ":" + str(self.get_value(name)) + " # " + self.get_desc(name)

def safeget(l, i, defval=False):
    if len(l) > i :
        return l[i]
    else :
        return defval
        
def StatParserTest(): 
    stat_parser = StatParser("./DDR3.stats", verbose=True)
    # stat_parser.dump_stats()
    quit()

if RUN_TEST:
    StatParserTest()