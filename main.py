#Make a thing that says redo shift application if message remains the same
#Add something that ensures shift input ciphered is actual words
    #If so, add a did you mean that? [like google] part

import string
import random

def line():
    print('-------')

def load_words(file_name):

    inFile = open(file_name, 'r')
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    return wordlist

VALID_WORDS = load_words('words.txt')

def add_to_file(file, name, number, feedback):
    output_file = open(file, 'a')
    output_file.write('{}: {} {}\n'.format(name, number, feedback))
    output_file.close()

def build_shift_dict(shift):
    shiftDict = {}
    uppercaseLetters = list(string.ascii_uppercase)
    lowercaseLetters = list(string.ascii_lowercase)

    def dictMapping(shiftDict, shift, letters):
        for i in range(len(letters)):
            if i + shift >= 26:
                tempShift = (i + shift) - 26
                shiftDict[letters[i]] = letters[tempShift]
            else:
                shiftDict[letters[i]] = letters[i + shift]

    dictMapping(shiftDict, shift, uppercaseLetters)
    dictMapping(shiftDict, shift, lowercaseLetters)

    return shiftDict

def apply_shift(text, shift, crypted):

    returnStr = ''
    shiftDict = build_shift_dict(shift)
    if crypted == True:
        shiftDict = dict(zip(shiftDict.values(), shiftDict.keys()))

    for letter in text:
        if letter in shiftDict:
            shiftLetter = shiftDict[letter]
            returnStr += shiftLetter
        else:
            returnStr += letter

    return returnStr

def decrypt_message(message_text):
    prevCount = 0
    shiftVal = 0
    for i in range(1, 26):
        count = 0
        for word in message_text.split():
            decryptedWord = apply_shift(word, i, True)
            for validword in VALID_WORDS:
                if decryptedWord == validword.lower():
                    count += 1
        if count > prevCount:
            prevCount = count
            shiftVal = i
        
    return tuple((26 - shiftVal, apply_shift(message_text, shiftVal, True))) 

def general_Morse(message, crypted):
    morse_dict = {'a': '.- ', 'b': '-... ', 'c': '-.-. ', 'd': '-.. ', 'e': '. ', 'f': '..-. ', 'g': '--. ', 'h': '.... ', 'i': '.. ', 'j': '.--- ', 'k': '-.- ', 'l': '.-.. ', 'm': '-- ', 'n': '-. ', 'o': '--- ', 'p': '.--. ', 'q': '--.- ', 'r': '.-. ', 's': '... ', 't': '- ', 'u': '..- ', 'v': '...- ', 'w': '.-- ', 'x': '-..- ', 'y': '-.-- ', 'z': '--.. ', '1': '.---- ', '2': '..--- ', '3': '...-- ', '4': '....- ', '5': '..... ', '6': '-.... ', '7': '--... ', '8': '---.. ', '9': '----. ',  '0': '----- ', '.': '.-.-.- ', ',': '--..-- ', '?': '..--.. ', "'": '.----. ', '/': '-..-. ', ':': '---... ', ';': '-.-.-. ', '+': '.-.-. ', '-': '-....- ', '=': '-...- ', '(': '-.--.- ', ')': '-.--.- ', '_': '..--.- ', '&': '.-... ', '$': '...-..- '}
    returnStr = ''

    if crypted == True:
        morse_dict = dict(zip(morse_dict.values(), morse_dict.keys()))
        message = message.split(' ')

    for letter in message:
        if crypted == True:
            letter = letter + ' '
        if letter in morse_dict:
            newLetter = morse_dict[letter]
            returnStr += newLetter
        else:
            returnStr += letter
    return returnStr

def generateCipher():
    flag = True
    line()
    message = input('Text: ')
    while flag == True:
        shift = random.randint(1, 26)

        def question_format(question_text, choice1, choice2):
            exitFlag = True
            while exitFlag == True:
                typeMessage = (input(question_text)).lower()
                if choice1 not in typeMessage and choice2 not in typeMessage:
                    print('Specify {} or {}. '.format(choice1, choice2))
                else:
                    exitFlag = False
            return typeMessage
    
        text_type = question_format('Plain/Cipher: ', 'plain', 'cipher')

        cipher_type = question_format('Shift/Morse: ', 'shift', 'morse' )

        if 'plain' in text_type and 'shift' in cipher_type: 
            print(apply_shift(message, shift, False))
        elif'cipher' in text_type and 'shift' in cipher_type:
            print(decrypt_message(message)[1])
        elif 'plain' in text_type and 'morse' in cipher_type:
            message = message.lower()
            print(general_Morse(message, False))
        elif 'cipher' in text_type and 'morse' in cipher_type:
            print(general_Morse(message, True))

        line()
        message = input('Text (Type !! if done): ')

        if message == '!!':
            line()
            flag = True
            while flag == True:
                feedback = (input('Would you like to give feedback? ')).lower()
                if feedback == 'no':
                    line()
                    exit()
                elif feedback != 'yes':
                    print('Type in yes or no.')
                else:
                    flag = False

            flag = True
            while flag == True:
                rating = input('On a scale from 1 - 10 with 1 being very dissatisfied and 10 being very satisfied, rate your experience: ')
                if rating.isnumeric() == False or int(rating) < 1 or int(rating) > 10:
                    print('Please type in a number from 1 to 10.')
                    line()
                else:
                    flag = False
            if int(rating) <= 5:
                review = input('Sorry you feel that way, what could we do to improve our service? ')
            else:
                review = input('Is there anything we can improve upon? ')
            line()
            print('Okay, thanks!')
            line()
            name = input('Please enter your name: ')
            line()
            print('Goodbye,', name + '. Hope to see you again!')
            line()
            if review.lower() == 'no':
                add_to_file('feedback.txt', name, rating, ' ')
            else:
                add_to_file('feedback.txt', name, rating, review)
            exit()

if __name__ == '__main__':
    generateCipher()