# -*- coding: utf-8 -*-
'''
File Name: cmd.py
Author: JackeyGao
mail: junqi.gao@shuyun.com
Created Time: 三  7/22 23:26:54 2015
'''
import subprocess
import time
import sys

class Timeout(Exception):
    pass

def run(command, timeout=10):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    poll_seconds = .250
    deadline = time.time()+timeout
    while time.time() < deadline and proc.poll() == None:
        time.sleep(poll_seconds)

    if proc.poll() == None:
        if float(sys.version[:3]) >= 2.6:
            proc.terminate()
        raise Timeout()

    stdout, stderr = proc.communicate()
    return stdout, stderr, proc.returncode

if __name__=="__main__":
    print run(command='ls', timeout=10)

    print run(command='sleep 10', timeout=3) #should timeout
