# author: Jayden Chan
# date: February 18, 2023
# file: codec.py uses Codec, CaesarCypher, and Huffman to encode and decode messages
# input: message
# output: encryption
import numpy as np

class Codec():
    
    def __init__(self):
        self.name = 'binary'
        self.delimiter = '#' 

    # convert text or numbers into binary form    
    def encode(self, text):
        if type(text) == str:
            return ''.join([format(ord(i), "08b") for i in text])
        else:
            print('Format error')

    # convert binary data into text
    def decode(self, data):
        binary = []        
        for i in range(0,len(data),8):
            byte = data[i: i+8]
            if byte == self.encode(self.delimiter): # you need to find the correct binary form for the delimiter
                break
            binary.append(byte)
        text = ''
        for byte in binary:
            text += chr(int(byte,2))       
        return text 

class CaesarCypher(Codec):

    def __init__(self, shift=3):
        self.name = 'caesar'
        self.delimiter = '#'  
        self.shift = shift    
        self.chars = 256      # total number of characters

    # convert text into binary form
    # your code should be similar to the corresponding code used for Codec
    def encode(self, text):
        data = ''
        for character in text:
            character_code = ord(character)                             # convert character to ASCII
            shifted_code = (character_code + self.shift) % self.chars   # adds shift value and wrap around
            data += '{:08b}'.format(shifted_code)                       # convert shifted code to 8-bit binary string and adds to data
        return data
    
    # convert binary data into text
    # your code should be similar to the corresponding code used for Codec
    def decode(self, data):
        text = ''
        binary = []
        index = 0
        while index < len(data):            # iterates through the data string until the end is reached
            byte = data[index:index + 8]        # extracts  current 8-bit data
            if byte == self.encode(self.delimiter):
                break                  # if current data in delimiter, break
            binary.append(byte)
            index += 8                 # increment size of 8 bytes at a time
        for byte in binary:
            shifted_code = int(byte, 2)         #converts chunk into interger
            code = (shifted_code - self.shift) % self.chars  # shifts integer back by the cypher's value
            text += chr(code)           # converts shifted integer to corresponding character and adds to the string
        return text

# a helper class used for class HuffmanCodes that implements a Huffman tree
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.left = left
        self.right = right
        self.freq = freq
        self.symbol = symbol
        self.code = ''


class HuffmanCodes(Codec):

    def __init__(self):
        self.nodes = None
        self.name = 'huffman'
        self.delimiter = '#'

    # make a Huffman Tree
    def make_tree(self, data):
        # make nodes
        nodes = []
        for char, freq in data.items():
            nodes.append(Node(freq, char))

        # assemble the nodes into a tree
        while len(nodes) > 1:
            # sort the current nodes by frequency
            nodes = sorted(nodes, key=lambda x: x.freq)

            # pick two nodes with the lowest frequencies
            left = nodes[0]
            right = nodes[1]

            # assign codes
            left.code = '0'
            right.code = '1'

            # combine the nodes into a tree
            root = Node(left.freq + right.freq, left.symbol + right.symbol,
                        left, right)

            # remove the two nodes and add their parent to the list of nodes
            nodes.remove(left)
            nodes.remove(right)
            nodes.append(root)
        return nodes

    # traverse a Huffman tree
    def traverse_tree(self, node, val, codes):
        next_val = val + node.code
        if (node.left):
            self.traverse_tree(node.left, next_val, codes)
        if (node.right):
            self.traverse_tree(node.right, next_val, codes)
        if (not node.left and not node.right):
            codes[node.symbol] = next_val
            #print(f"{node.symbol}->{next_val}") # this is for debugging
            # you need to update this part of the code
            # or rearrange it so it suits your needs

    # convert text into binary form
    def encode(self, text):
        data = ''
        freq = {}
        # counts frequency of each character
        for char in text:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1

        self.nodes = self.make_tree(freq)   # make a Huffman tree
        codes = {}  # traverses the tree to get the Huffman codes for each character
        self.traverse_tree(self.nodes[0], '', codes)    # encodes the text using the Huffman codes
        for char in text:
            data += codes[char]
        data += codes[self.delimiter]   # adds delimiter to the end of the binary string
        return data

    # convert binary data into text
    def decode(self, data):
        text = ''
        codes = {}
        self.traverse_tree(self.nodes[0], '', codes)    # traverses the Huffman tree to get the codes for each character
        code = ''
        for bit in data:
            code += bit
            for char, c in codes.items():
                if c == code:                   # if the code matches a Huffman code for a character, adds that character to the output text
                    if char == self.delimiter:  # if the delimiter character is encountered, stops decoding
                        return text
                    text += char
                    code = ''                   # resets the current code being processed
                    break
        return text
# driver program for codec classes
if __name__ == '__main__':
    text = 'hello' 
    #text = 'Casino Royale 10:30 Order martini' 
    print('Original:', text)
    
    c = Codec()
    binary = c.encode(text + c.delimiter)
    # NOTE: binary should have a delimiter and text should not have a delimiter
    print('Binary:', binary) # should print '011010000110010101101100011011000110111100100011'
    data = c.decode(binary)  
    print('Text:', data)     # should print 'hello'
    
    cc = CaesarCypher()
    binary = cc.encode(text + cc.delimiter)
    # NOTE: binary should have a delimiter and text should not have a delimiter
    print('Binary:', binary)
    data = cc.decode(binary) 
    print('Text:', data)     # should print 'hello'
     
    h = HuffmanCodes()
    binary = h.encode(text + h.delimiter)
    # NOTE: binary should have a delimiter and text should not have a delimiter
    print('Binary:', binary)
    data = h.decode(binary)
    print('Text:', data)   # should print 'hello'

