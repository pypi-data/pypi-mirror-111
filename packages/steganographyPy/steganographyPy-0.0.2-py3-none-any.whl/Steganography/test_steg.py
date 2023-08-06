import unittest
import steg

import numpy as np

class TestSteg(unittest.TestCase):

	def test_encode_decode(self):

		# DATA
		# text for coding
		message = 'I am secret message'
		# fake image for stego
		image = np.zeros((50, 50, 3), dtype=int)


		# DATA PROCESSING
		# image with stego
		image = steg.encode(image, message)
		# decode message from stego image
		secret_message = steg.decode(image)[:len(message)]


		# RESULTS CHECK
		# original message should match decoded message
		self.assertEqual(message, secret_message)
