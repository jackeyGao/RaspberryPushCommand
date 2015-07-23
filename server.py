# -*- coding: utf-8 -*-
'''
File Name: main.py
Author: JackeyGao
mail: junqi.gao@shuyun.com
Created Time: 三  7/22 21:22:48 2015
'''

VERSION = "0.2"

import time
import logging
import json
import argparse
from pushbullet import Pushbullet
from pushbullet import Listener
import cmd

class _NullHandler(logging.Handler):
    def emit(self, record):
        pass

logger = logging.getLogger(__name__)
logger.addHandler(_NullHandler())

HTTP_PROXY_HOST = None
HTTP_PROXY_PORT = None


class ListenerRealTime(Listener):

    def __init__(self, account,
                on_push=None,
                http_proxy_host=None,
                http_proxy_port=None):

        devices = [ d for d in account.devices if d.nickname == "Raspberry" ]
        if not devices:
            device = account.new_device("Raspberry")
        else:
            device = devices[0]

        self.device = device
        self.pb = account
        super(ListenerRealTime, self).__init__(account, 
                on_push, http_proxy_host, http_proxy_port)

    def on_message(self, ws, message):
        logger.debug('Message received:' + message)
        try:
            json_message = json.loads(message)
            if json_message["type"] != "nop":
                self.on_push(json_message, self)
        except Exception as e:
            print e
            logging.exception(e)


def on_push(data, listener):
    logger.debug("Received data: \n{}".format(data))
    ts = time.time() - 5
    status, pushes = listener.pb.get_pushes(modified_after=ts)
    if status is True:
        logger.debug("Received pushes: \s".format(json.dumps(pushes)))
        
        outputs = [ push for push in pushes if push.has_key("title") ]
        command = [ push for push in pushes if not push.has_key("title") ]
        if len(outputs) > 0 and command > 0:
            # 避免造成push死循环， 所以这个等待时间应当超过上面的2
            logger.debug("Have output type push, will continue")
            time.sleep(3)
            return

        if not command:
            logger.debug("No command , will retrun ")
            return

        command = command[0]["body"]
        try:
            output, error, status = cmd.run(command=command, timeout=5)
            listener.device.push_note("Output", output)
            logger.info("Complated run(%s)" % command)
        except cmd.Timeout as e:
            raspberry.push_note("Output", "command(%s) timeout(5s)." % command)
            print("Command timeout .")
            logger.info("command(%s) timtout" % command)
    else:
        logger.info("Not get pushes.")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", type=str, 
            required=True, help="The pushbullet api key.")
    args = parser.parse_args()
    try:
        pb = Pushbullet(args.key)
        s = ListenerRealTime(account=pb, on_push=on_push,
                http_proxy_host=HTTP_PROXY_HOST,
                http_proxy_port=HTTP_PROXY_PORT)
        s.run_forever()
    except KeyboardInterrupt:
        s.close()

