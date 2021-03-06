#!/usr/bin/env python

from time import sleep, clock
import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
StateLock = threading.Lock()

class GPIO_Switch:
	
	def __init__(self, gpio_number):
		self.GPIO_Number = gpio_number
		self.Switch_State = False
		
		GPIO.setup(self.GPIO_Number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			
	def Standard_Switch(self,):	# Version 2.1
		print("Standard Switch gestartet \nzum Schalten Enter Drücken:")
		while True:
			#~ input()
			GPIO.wait_for_edge(self.GPIO_Number, GPIO.FALLING)
			self.Switch_State = not self.Switch_State
			#~ print("\nswitch: ", self.Switch_State)
			sleep(0.01)
			GPIO.wait_for_edge(self.GPIO_number, GPIO.RISING)
			self.Switch_State = not self.Switch_State
			#~ print("\nswitch: ", self.Switch_State)
		print("Standard Switch beendet")
		return True
		
class GPIO_DipSwitch:
	
	def __init__(self, gpio_number):
		self.GPIO_Number = gpio_number
		self.Switch_State = False
		self.Comfort_State = False
		
		GPIO.setup(self.GPIO_Number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			
	def Standard_DipSwitch(self,):	# Version 2.1
		print("Standard DipSwitch gestartet \nzum Schalten Enter Drücken:")
		while True:
			#~ input()
			GPIO.wait_for_edge(self.GPIO_Number, GPIO.FALLING)
			self.Switch_State = not self.Switch_State
			sleep(0.01)
			GPIO.wait_for_edge(self.GPIO_Number, GPIO.RISING)
			self.Switch_State = not self.Switch_State
			#~ print("\nswitch: ", self.Switch_State)
		print("Standard DipSwitch beendet")
		return True
	
	def Static_DipSwitch(self,):	# Version 2.1
		print("Static DipSwitch gestartet \nzum Schalten Enter Drücken:")
		while True:
			#~ input()
			GPIO.wait_for_edge(self.GPIO_Number, GPIO.FALLING)
			self.Switch_State = not self.Switch_State
			#~ print("\nswitch: ", self.Switch_State)
		print("Static DipSwitch beendet")
		return True
		
	def Comfort_DipSwitch(self,):	# Version 2.1
		print("Comfort DipSwitch gestartet \nzum schalten enter drücken")
		while True:
			GPIO.wait_for_edge(self.GPIO_Number, GPIO.FALLING)
			a = clock()
			print("falling edge detected")
			sleep(0.01)
			GPIO.wait_for_edge(self.GPIO_Number, GPIO.RISING)
			print("rising edge detected")
			b = clock()
			c = b-a
			print("duration: ", c)
			if c > 0.0015:
				self.Comfort_State = True
			
			self.Switch_State = not self.Switch_State
			#~ print("\nswitch: ", self.Switch_State, "\ncomfort switch: ", self.Comfort_State)
			sleep(0.1)
			self.Comfort_State = False
		print("Comfort DipSwitch beendet")
		return True

class GPIO_Target:		
	
	def __init__(self, gpio_number):
		self.GPIO_Number = gpio_number
		self.State = False
		self.frequency = 0.6
		
		GPIO.setup(self.GPIO_Number, GPIO.OUT)

		
	def Turn(self, Ziel):
		i = 0
		while True:
			if Ziel.Switch_State and not Ziel.Comfort_State:	
				GPIO.output(self.GPIO_Number, GPIO.HIGH)
				sleep(self.frequency)
				GPIO.output(self.GPIO_Number, GPIO.LOW)
				sleep(self.frequency)
			if Ziel.Switch_State and Ziel.Comfort_State:
				print("\nKomfort-Blinker gestartet")
				while i < 5:
					GPIO.output(self.GPIO_Number, GPIO.HIGH)
					sleep(self.frequency)
					GPIO.output(self.GPIO_Number, GPIO.LOW)
					sleep(self.frequency)
					i += 1
				print("\nKomfort-Blinker beendet")
				Ziel.Switch_State = False
			if not Ziel.Switch_State and i > 0:
				i = 0
			else:
				sleep(0.1)			
		return True
		
	def Standard_IO(self, Ziel):
		while True:
			if Ziel.Switch_State:
				GPIO.output(self.GPIO_Number, GPIO.HIGH)
			else:
				GPIO.output(self.GPIO_Number, GPIO.LOW)
		
if __name__ == '__main__':

	KillSwitchIn = GPIO_Switch(25)
	KillSwitchOut = GPIO_Target(4)
	EngineStartIn = GPIO_DipSwitch(8)
	EngineStartOut = GPIO_Target(17)
	
	#~ KillSwitch und Enginge Start
	thread1 = threading.Thread(target=KillSwitchIn.Standard_DipSwitch, args=())
	thread1.start()
	thread2 = threading.Thread(target=KillSwitchOut.Standard_IO, args=(KillSwitchIn,))
	thread2.start()
