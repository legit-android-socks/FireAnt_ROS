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
GPIO.output(LED_PIN, GPIO.LOW)

MOTOR_L_PIN_1 = 9
MOTOR_L_PIN_2 = 10
MOTOR_R_PIN_1 = 11
MOTOR_R_PIN_2 = 12
GPIO.setup(MOTOR_L_PIN_1, GPIO.OUT)
GPIO.setup(MOTOR_L_PIN_2, GPIO.OUT)
GPIO.setup(MOTOR_R_PIN_1, GPIO.OUT)
GPIO.setup(MOTOR_R_PIN_2, GPIO.OUT)
GPIO.output(MOTOR_L_PIN_1, GPIO.LOW)
GPIO.output(MOTOR_L_PIN_2, GPIO.LOW)
GPIO.output(MOTOR_R_PIN_1, GPIO.LOW)
GPIO.output(MOTOR_R_PIN_2, GPIO.LOW)

def control_topic_listener():
    rospy.init_node('control_lobe', anonymous=True)
    rospy.Subscriber('control', String, callback, queue_size=10)
    rospy.spin()

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + data.data)
    control_data = ast.literal_eval(data.data)
    try:
        leds = control_data['leds']
        movement = {
            control_data['fwd'],
            control_data['back'],
            control_data['left'],
            control_data['right']
            }
    except ValueError:
        print("TYPE ERROR")
    switch_leds(leds)
    move(movement)

def switch_leds(led_states):
    if led_states['left'] is True:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)

def move(movement):
    if int(movement["fwd"]) == 1:
        foreward()

def stop():
    GPIO.output(MOTOR_L_PIN_1, GPIO.LOW)
    GPIO.output(MOTOR_L_PIN_2, GPIO.LOW)
    GPIO.output(MOTOR_R_PIN_1, GPIO.LOW)
    GPIO.output(MOTOR_R_PIN_2, GPIO.LOW)

def foreward():
    GPIO.output(MOTOR_L_PIN_1, GPIO.HIGH)
    GPIO.output(MOTOR_L_PIN_2, GPIO.LOW)
    GPIO.output(MOTOR_R_PIN_1, GPIO.HIGH)
    GPIO.output(MOTOR_R_PIN_2, GPIO.LOW)

def back():
    GPIO.output(MOTOR_L_PIN_1, GPIO.LOW)
    GPIO.output(MOTOR_L_PIN_2, GPIO.HIGH)
    GPIO.output(MOTOR_R_PIN_1, GPIO.LOW)
    GPIO.output(MOTOR_R_PIN_2, GPIO.HIGH)

def left():
    GPIO.output(MOTOR_L_PIN_1, GPIO.LOW)
    GPIO.output(MOTOR_L_PIN_2, GPIO.HIGH)
    GPIO.output(MOTOR_R_PIN_1, GPIO.HIGH)
    GPIO.output(MOTOR_R_PIN_2, GPIO.LOW)

def right():
    GPIO.output(MOTOR_L_PIN_1, GPIO.HIGH)
    GPIO.output(MOTOR_L_PIN_2, GPIO.LOW)
    GPIO.output(MOTOR_R_PIN_1, GPIO.LOW)
    GPIO.output(MOTOR_R_PIN_2, GPIO.HIGH)

if __name__ == '__main__':
    try:    
        while True:
            control_topic_listener()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Exited with keyboard interrupt!")
        exit(0)
    GPIO.cleanup()
