import numpy as np


##### UTILITIES #####
def str_to_binary(text):
	return ''.join(format(ord(i), '08b') for i in text)


def binary_to_str(bin):
	n = int(bin, 2)
	return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode("utf8",'ignore')

def int_to_binary(integer):
	return format(integer, "08b")


# Bits are counted least significant bit
def turn_bit_on(val, bit):
	pwr_of_two = 2**bit
	return val | pwr_of_two

def turn_bit_off(val, bit, maxi=8):
	pwr_of_two = 2**bit
	return val & (2**maxi-1-pwr_of_two)


##### MAIN CODE #####
def encode(img, text, density=1) -> np.array:
	'''
	This function takes image, message and density, then encodes message into image and returns it

	:param img: Numpy array representing image in which we encode message
	:param text: Text to be encoded
	:param density: How many bits of pixel's single channel should we use, default=1
	:return: Numpy array representing image with encoded message
	'''
	new_img = img.flatten()
	binary_string = str_to_binary(text)

	rng = min(len(new_img), len(binary_string))


	# for each pixel in image
	for pixel in range(rng):
		# for each needed bit in pixel
		for bit in range(density):

			bit_index = pixel * density + bit
			
			# If we need to turn on the bit
			if binary_string[bit_index] == '1':
				new_img[pixel] = turn_bit_on(new_img[pixel], bit)
			# If we need to turn off the bit
			elif binary_string[bit_index] == '0':
				new_img[pixel] = turn_bit_off(new_img[pixel], bit)

			

	return new_img.reshape(img.shape)





def decode(img, density=1) -> str:
	'''
	This function takes image and density, then decodes message from image and returns it

	:param img: Numpy array representing image from which we decode message
	:param density: How many bits of pixel's single channel should we use, default=1
	:return: String with decoded message
	'''
	img = img.flatten()
	binary_string = ''
	for pixel in range(len(img)):
		binary_string = binary_string + int_to_binary(img[pixel])[-density:][::-1]


	# cut of some data so we have only full bytes
	full_len = len(binary_string)
	cut_len = full_len - full_len % 8
	binary_string = binary_string[:cut_len]

	return binary_to_str(binary_string)





