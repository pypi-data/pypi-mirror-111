import math 
import random

class Calculator():
    def calc_easy(string):
        try:
            number1 = string.split(' ')[2]
            operator = string.split(' ')[3]
            number2 = string.split(' ')[4]

            print(number1 + operator + number2)

            calculatedResult = 0

            if operator == '+':
                print("calc")
                calculatedResult = float(number1) + float(number2)
                return calculatedResult
            elif operator == '-':
                print("calc")
                calculatedResult = float(number1) - float(number2)
                return calculatedResult
            elif operator == '*':
                print("calc")
                calculatedResult = float(number1) * float(number2)
                return calculatedResult
            elif operator == '/':
                print("calc")
                calculatedResult = float(number1) / float(number2)
                return calculatedResult
            else:
                try:
                    number1 = string.split(' ')[2]
                    operator = string.split(' ')[3]
                    number2 = string.split(' ')[4]

                    calcResult = 0

                    if operator == '**':
                        calcResult = math.pow(float(number1), float(number2))
                    if operator == '//':
                        calcResult = float(number2)**(1/float(number1))

                    return calcResult

                except:
                    return 0

        except:
            return 0

    def calc_advanced(string):
        operator = string.split(' ')[3]
        number = string.split(' ')[4]

        calculatedResult = 0

        print (operator + number)

        if (operator == "sqrt"):
            calculatedResult = math.sqrt(float(number))
        if (operator == "sin"):
            calculatedResult = math.sin(float(number))
        if (operator == "tan"):
            calculatedResult = math.tan(float(number))
        if (operator == "cos"):
            calculatedResult = math.cos(float(number))

        return calculatedResult


    def get_random(number1, number2):

        print(str(number1) + " " + str(number2))

        randomInt = random.randint(float(number1), float(number2))

        return randomInt

    

