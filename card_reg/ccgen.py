#!/usr/bin/python
from random import Random
import copy

mastercardPrefixList = [
['5','1','3','7','6','8'],
['5','1','3','7','6','7'],
['5','1','3','7','6','6'],
['5','1','3','7','6','5']
        ]

#mc_prefix = ['5','1','3','7','6']
mc_prefix = ['5','1','3','7','5']
visa_prefix = ['4','1','2','5','1'] #4489281606131355

def completed_number(prefix, length):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """

    ccnumber = prefix

    # generate digits

    while len(ccnumber) < (length - 1):
        digit = str(generator.choice(range(0, 10)))
        #digit = str(0)
        ccnumber.append(digit)


    # Calculate sum

    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    mynumber = ccnumber

    while pos < length - 1:

        #odd = int(reversedCCnumber[pos]) * 2
        if (pos % 2 == 0):
            odd = int(mynumber[pos]) * 2
            if odd > 9:
                odd -= 9
            sum += odd
        else: sum += int(mynumber[pos])

        pos += 1

    # Calculate check digit

    #print("summa: ",sum)
    checkdigit = sum % 10
    #print(checkdigit)
    if(checkdigit == 0):
        checkdigit = 0
    else: checkdigit = 10 - checkdigit

    ccnumber.append(str(checkdigit))
    return ''.join(ccnumber)


def credit_card_number(prefixList, length):

    result = []
    i = 0

    while i < len(prefixList):

        ccnumber = copy.copy(prefixList[i])
        result.append(completed_number(ccnumber, length))
        i = i + 1

    return result

def credit_card_number_2(prefix, length, amount):

    result = []
    i = 0

    while i < amount:

        ccnumber = copy.copy(prefix)
        result.append(completed_number(ccnumber, length))
        i += 1

    return result


def output(title, numbers):

    result = []
    result.append(title)
    result.append('-' * len(title))
    result.append('\n'.join(numbers))
    result.append('')

    return '\n'.join(result)

#
# Main
#

generator = Random()
generator.seed()        # Seed from current time

#mastercard = credit_card_number(mastercardPrefixList, 16)
mastercard = credit_card_number_2(visa_prefix, 16, 3000)
#print(output("Mastercard", mastercard))
f = open('cards.txt', 'w')
for item in mastercard:
	f.write(item + '\n')
f.close()
