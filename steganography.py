# author: Jayden Chan
# date: February 18, 2023
# file: steganography.py encodes and decodes messages on a picture
# input: message and file
# output: file with encryption
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher, HuffmanCodes

class Steganography():
    
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None

    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein)
        #print(image) # for debugging
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            self.codec = HuffmanCodes()
        binary = self.codec.encode(message+self.delimiter)
        
        # check if possible to encode the message
        num_bytes = ceil(len(binary)//8) + 1 
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            self.text = message
            self.binary = binary
            bit_index = 0
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    for k in range(3):
                        if bit_index < len(binary):
                            # gets current pixel value and converts to binary
                            pixel = format(image[i, j, k], '08b')
                            # modifys least significant bit of pixel
                            pixel = pixel[:-1] + binary[bit_index]
                            # updates pixel value in image
                            image[i, j, k] = int(pixel, 2)
                            bit_index += 1
            cv2.imwrite(fileout, image)
                   
    def decode(self, filein, codec):
        image = cv2.imread(filein)
        #print(image) # for debugging      
        flag = True
        
        # convert into text
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        if flag:
            # extract the message bits from the image pixels
            binary_data = ''
            bit_index = 0
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    for k in range(3):
                        if bit_index < len(self.binary):
                            # gets current pixel value and converts to binary
                            pixel = format(image[i, j, k], '08b')
                            # extracts least significant bit of  pixel
                            binary_data += pixel[-1]
                            bit_index += 1
                # updates data
                self.text = self.codec.decode(binary_data)
                self.binary = binary_data
        
    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)          

    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()

if __name__ == '__main__':
    
    s = Steganography()

    s.encode('fractal.jpg', 'fractal.png', 'hello', 'binary')
    # NOTE: binary should have a delimiter and text should not have a delimiter
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'

    s.decode('fractal.png', 'binary')
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'
    print('Everything works!!!')
   
