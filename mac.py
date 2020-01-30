import random
import time

import station

class NullMac(station.Station):
	'''
	`NullMac` is essentially having no MAC protocol. The node sends
	whenever it has a packet ready to send, and tries up to two retries
	if it doesn't receive an ACK.

	The node makes no attempt to avoid collisions.
	'''
	def __init__(self, id, q_to_ap, q_to_station, interval):
		super().__init__(id, q_to_ap, q_to_station, interval)

	def run(self):
		# Continuously send packets
		while True:
			# Block until there is a packet ready to send
			self.wait_for_next_transmission()

			# Try up to three times to send the packet successfully
			for i in range(0, 3):
				self.send('DATA')

				# Wait for a possible ACK. If we get one, we are done with this
				# packet. If all of our retries fail then we just consider this
				# packet lost and wait for the next one.
				recv = self.receive()
				if recv == 'ACK':
					break


class NullMacExponentialBackoff(station.Station):
	'''
	`NullMacExponentialBackoff` extends the basic NullMac to add exponential
	backoff if a packet is sent and an ACK isn't received.

	The sender should use up to two retransmissions if an ACK is not received.
	'''
	def __init__(self, id, q_to_ap, q_to_station, interval):
		super().__init__(id, q_to_ap, q_to_station, interval)

	def run(self):

		# Continuously send packets
		while True:
			# Block until there is a packet ready to send
			self.wait_for_next_transmission()

			# Implement NullMacExponentialBackoff here.

			# Let maximum backoff time be 500ms
			maxBackoff = .05

			# Try up to two time to send the packet successfully
			for i in range(0, 2):
				self.send('DATA')

				recv = self.receive()
				if (recv == 'ACK'):
					break

				# The wait time is min(((2^n)+random_number_milliseconds), maximum_backoff), with n incremented by 1 for each iteration (request).
				# Following the example algorithm from Google's IoT documentation
				t = (float)(2 ^ i) + random.uniform(.01, .025)
				if (t < maxBackoff):
					waitTime = t
				else:
					waitTime = maxBackoff

				time.sleep(waitTime)





class CSMA_CA(station.Station):
	'''
	`CSMA_CA` should implement Carrier Sense Multiple Access with Collision
	Avoidance. The node should only transmit data after sensing the channel is
	clear.
	'''
	def __init__(self, id, q_to_ap, q_to_station, interval):
		super().__init__(id, q_to_ap, q_to_station, interval)

	def run(self):
		# Continuously send packets
		while True:
			# Block until there is a packet ready to send
			self.wait_for_next_transmission()


			# Time to wait for another transmission attempt is a random number between 10 and 50ms
			wait_time = random.uniform(.01, .025)

			packetSent = False

			# Use random backoff before trying to transmit again
			while packetSent is False:
				while self.sense() is True:
					time.sleep(wait_time)
					
				self.send('DATA')
				recv = self.receive()
				if recv == 'ACK':
					packetSent = True



class RTS_CTS(station.Station):
	'''
	`RTS_CTS` is an extended CSMA/CA scheme where the transmitting station also
	reserves the channel using a Request to Send packet before transmitting. In
	this network, receiving a CTS message reserves the channel for a single DATA
	packet.
	'''
	def __init__(self, id, q_to_ap, q_to_station, interval):
		super().__init__(id, q_to_ap, q_to_station, interval)


	def run(self):
		# Continuously send packets
		while True:
			# Block until there is a packet ready to send
			self.wait_for_next_transmission()
			received_ACK = False
			ready_to_send = False
			while received_ACK is False:

				# Time to wait for another transmission attempt is a random number between 10 and 50ms
				wait_time = random.uniform(.02, .05)



				while ready_to_send is False:
					if self.sense() is False:
						#print((str)(self.id) + " attempting to send RTS signal")
						self.send('RTS')
						recv = self.receive()
						if recv == 'CTS':
							#print((str)(self.id) + " received CTS signal")
							ready_to_send = True

					time.sleep(wait_time)

				# Received a CTS response from the access point
				#print((str)(self.id) + " Received CTS signal.")
				# Try to send DATA packet to access point
				#print("Sending data packet")
				self.send('DATA')
				recv2 = self.receive()
				if recv2 == 'ACK':
					#print((str)(self.id) + " received ACK")
					received_ACK = True





























