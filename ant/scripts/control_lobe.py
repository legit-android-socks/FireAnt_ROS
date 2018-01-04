#!/usr/bin/env python

import sys
import ast
#import time
#import xml.etree.ElementTree as ET
import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO

#tree = ET.parse('config.xml')
#root = tree.getroot()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

def control_topic_listener():
    rospy.init_node('control_lobe', anonymous=True)
    rospy.Subscriber('control', String, callback, queue_size=10)
    rospy.spin()

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + data.data)
    control_data = ast.literal_eval(data.data)
    try:
        on_off = control_data['leds']['left']
    except ValueError:
        on_off = 0
        print("TYPE ERROR: leds.left")
    turn_leds(on_off)

def turn_leds(state):
    if state is True:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)

if __name__ == '__main__':
    while True:
        try:
            control_topic_listener()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print("Exited with keyboard interropt!")
    GPIO.cleanup()