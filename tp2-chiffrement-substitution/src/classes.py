import string
import random


class Encodeur:
    def __init__(self,pwd=None):

        if pwd is None:
            self.password = list(string.ascii_lowercase)
            random.shuffle(self.password)
        else:
            self.password = list(pwd)

    def encode_string(self,input_string):
        crypted_string = [
            self.password[ord(c) - ord('a')] if c.islower()
            else self.password[ord(c.lower()) - ord('a')].upper() if c.isupper()
            else c
            for c in input_string
        ]       

        return ''.join(crypted_string)

    def encode_file(self,input_file,output_file):

        try:
            with open(input_file,'r', encoding='utf-8') as text_file:
                lines = text_file.readlines()

        except IOError:
            print("Cannot open file "+input_file)
            return

        encoded_lines= list(map(self.encode_string,lines))


        with open(output_file,'w', encoding='utf-8') as output:
            output.writelines(encoded_lines)
        



if __name__=="__main__" :

    enc = Encodeur("azertyuiopqsdfghjklmwxcvbn")
    print(enc.password)

    print(enc.encode_string("bonjour !"))

    enc.encode_file("data/test_encoding.txt","output/test_encoding_output.txt")
