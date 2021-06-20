
#config
ROUND_NUM = 0.00000001
MAX_NUMBER = 10**300

#initialized anything it will need later
import math
class EquationSyntaxError(Exception):
    def __init__ (self, description):
        self.description = description
    def __str__ (self):
        return(repr("Error, {}.".format(self.description)))
class UnknownCharacter(Exception):
    def __init__ (self, character, index):
        self.character = character
        self.index = index
        self.error = "Error. At index {} there was an unknown character \"{}\"".format(index,character)
    def __str__ (self):
        return(repr(self.error))
class TooBigNumber(Exception):
    def __init__ (self,action):
        self.action = action
    def __str__ (self):
        return "Numbers became too big while {}, please do not let numbers go above {}".format(self.action,MAX_NUMBER)

#also watch for OverflowError, since floats are raise to smaller numbers than ints

class MakingNumber: #since going through 1.01 char by char would end up as 1.1
    def __init__ (self,starting_chars,constant=False):
        self.string_rep = starting_chars
        self.constant = constant
    def add_chars(self,chars):
        self.string_rep += chars
    def get_float(self):
        return float(self.string_rep)

digit_chars = "1234567890."

#main method of modules
def evaluate_string(string):
        formatted_equation = format_string(string)
        return evaluate(formatted_equation)

#main methods

#split expression into a list of operands and operators 
def format_string(expression_string):

    expression_list = [0]
    index = -1
    for x in expression_string:
        index += 1
        #adding operators
        if x == "+" or x == "-" or x == "/" or x == "*" or x == "^" or x == "√" or x == "∫" or x == "!":
            if len(expression_list) == 1 and expression_list[0] == 0:
                expression_list[0] = x
            else:
                expression_list.append(x)
        
        #adding paranthases
        elif x == "(" or x == ")":
            if len(expression_list) == 1 and expression_list[0] == 0:
                expression_list[0] = x
            else:
                if x == "(":
                    if isinstance(expression_list[len(expression_list)-1],MakingNumber) or expression_list[len(expression_list)-1] == ")":
                        expression_list.append("*")
                        expression_list.append("(")
                    else:
                        expression_list.append("(")
                elif x == ")":
                    expression_list.append(")")

        #adding pi
        elif x == "π":
            if len(expression_list) == 1 and expression_list[0] == 0:
                expression_list[0] = MakingNumber(str(math.pi),True)
            elif isinstance(expression_list[len(expression_list)-1], MakingNumber):
                expression_list.append("*")
                expression_list.append(MakingNumber(str(math.pi),True))
            else:
                expression_list.append(MakingNumber(str(math.pi),True))
        
        #adding e
        elif x == "e":
            if len(expression_list) == 1 and expression_list[0] == 0:
                expression_list[0] = MakingNumber(str(math.e),True)
            elif isinstance(expression_list[len(expression_list)-1], MakingNumber):
                expression_list.append("*")
                expression_list.append(MakingNumber(str(math.e),True))
            else:
                expression_list.append(MakingNumber(str(math.e),True))
        
        #adding numbers
        elif x in digit_chars:
            if len(expression_list) == 1 and expression_list[0] == 0:
                expression_list[0] = MakingNumber(x)
            elif isinstance(expression_list[len(expression_list)-1], MakingNumber):
                if expression_list[len(expression_list)-1].constant:
                    expression_list.append("*")
                    expression_list.append(MakingNumber(x))
                else:
                    expression_list[len(expression_list)-1].add_chars(x)
            elif expression_list[len(expression_list)-1] == ")":
                expression_list.append("*")
                expression_list.append(MakingNumber(x))
            else:
                expression_list.append(MakingNumber(x))
        elif x == " ":
                pass
        else:
            raise(UnknownCharacter(x,index))
    

    for index,item in enumerate(expression_list):
        if isinstance(item,MakingNumber):
            expression_list[index] = atttempt_round(item.get_float())
            if abs(item.get_float()) > MAX_NUMBER:
                raise(TooBigNumber("parsing your input"))

    #add paranthases before and after list
    expression_list.append(")")
    expression_list.insert(0,"(")
    return(expression_list)

#evaluates a list as created above
def evaluate(table):
    #remove paranthases
    expression_list = table[1:len(table)-1]

    #first character checks
    if expression_list[0] == "√":
        expression_list.insert(0,2)

    #iterates through the list multiple times, each time doing next step of order of ops

    #calculates paranthases
    counter = 0
    paranthases = 0
    while counter < len(expression_list):
        if expression_list[counter] == "(":
            if paranthases == 0:
                start_p = counter
            paranthases += 1
        if expression_list[counter] == ")":
            if paranthases == 0:
                raise(EquationSyntaxError("It appears you have a closing parenthesis with no opening"))
            else:
                paranthases -= 1
                if paranthases == 0:
                    #when it detects a pair of paranthases, it evaluates whats in between them and replaces them with the answer.
                    end_p = counter
                    expression_list[start_p] = evaluate(expression_list[start_p:end_p+1])
                    del expression_list[start_p + 1:end_p+1]
                    counter = start_p
        counter += 1
    if paranthases > 0:
        raise(EquationSyntaxError("It appears you have opened a paranthesis without closing it"))

    # evaluates negatives
    counter = 0
    while counter < len(expression_list):
        if expression_list[counter] == "-":
            if counter >= len(expression_list) - 1:
                raise EquationSyntaxError("You have nothing after your negative sign")
            elif counter == 0:
                expression_list[counter] = -1*expression_list[counter+1]
                del expression_list[counter+1]
            elif not isinstance(expression_list[counter-1], int) and not isinstance(expression_list[counter-1], float) and not isinstance(expression_list[counter-1], complex):
                expression_list[counter] = -1*expression_list[counter+1]
                del expression_list[counter+1]
        counter += 1
        
    # evaluates functions
    counter = 0
    while counter < len(expression_list):
        if expression_list[counter] == "!":
            
            if counter == 0:
                raise(EquationSyntaxError("There is nothing before your factorial"))
            elif not isinstance(expression_list[counter-1], int):
                raise(EquationSyntaxError("There is a non-integer value \"{}\" before the factorial".format(str(expression_list[counter-1]))))
            else:
                expression_list[counter-1] = atttempt_round(expression_list[counter-1])
                for x in range(expression_list[counter-1]-1,0,-1):
                    expression_list[counter-1] *= x
                    if abs(expression_list[counter-1]) > MAX_NUMBER:
                        raise(TooBigNumber("doing a factorial"))
                del expression_list[counter]
        else:
            counter += 1
    
    

    #goes through checking for general errors so it doesn't need to do it on each following step of order of ops
    must_have_before = "^*/+-"
    must_have_after = "√∫^*/+-"
    if isinstance(expression_list[0], str) and expression_list[0] in must_have_before:
        raise(EquationSyntaxError("There is nothing before your {} sign".format(expression_list[0])))
    if isinstance(expression_list[-1], str) and expression_list[-1] in must_have_after:
        raise(EquationSyntaxError("There is nothing after your {} sign".format(expression_list[-1])))

    counter = 0
    while counter < len(expression_list):
        value = expression_list[counter]
        if isinstance(value, str):
            if value in must_have_before:
                before = expression_list[counter-1]
                if not (isinstance(before,int) or isinstance(before,float) or isinstance(before,complex)) and ((not isinstance(before,str)) or before in must_have_after):
                     raise(EquationSyntaxError("There is a non-number character behind your {} sign".format(value)))
            if value in must_have_after:
                after = expression_list[counter+1]
                if (not (isinstance(after,int) or isinstance(after,float) or isinstance(after,complex))) and ((not isinstance(after,str)) or after in must_have_before):
                     raise(EquationSyntaxError("There is a non-number character after your {} sign".format(value)))
    
        counter += 1

    # evaluate exponentials and factorials
    counter = 0
    while counter < len(expression_list):
        if expression_list[counter] == "^":
            expression_list[counter] = expression_list[counter-1] ** expression_list[counter+1]
            if abs(expression_list[counter]) > MAX_NUMBER:
                raise(TooBigNumber("evaluating an exponent"))
            del expression_list[counter + 1]
            del expression_list[counter - 1]
        elif expression_list[counter] == "√":
            if not isinstance(expression_list[counter - 1], int) and not isinstance(expression_list[counter-1], float)and not isinstance(expression_list[counter-1], complex):
                expression_list[counter] = expression_list[counter + 1] ** 0.5
                del expression_list[counter + 1]
                if abs(expression_list[counter]) > MAX_NUMBER:
                    raise(TooBigNumber("evaluating a root"))
            else:
                expression_list[counter] = expression_list[counter + 1] ** (1/expression_list[counter -1])
                del expression_list[counter + 1]
                del expression_list[counter - 1]
                if abs(expression_list[counter-1]) > MAX_NUMBER:
                    raise(TooBigNumber("evaluating a root"))
        elif expression_list[counter] == "∫":
            expression_list[counter + 1] = math.log(expression_list[counter + 1])
            if abs(expression_list[counter+1]) > MAX_NUMBER:
                    raise(TooBigNumber("doing a logarithm"))
            if counter > 0:
                if isinstance(expression_list[counter-1],int) or isinstance(expression_list[counter-1],float) or isinstance(expression_list[counter-1],complex):
                    expression_list[counter] = "*"
                else:
                    del expression_list[counter]
            else:
                del expression_list[counter]
        else:
            counter += 1
    counter = 0

    # evaluate multiply and divide operators
    while counter < len(expression_list):
        if expression_list[counter] == "*":
            expression_list[counter] = expression_list[counter-1] * expression_list[counter+1]
            if abs(expression_list[counter]) > MAX_NUMBER:
                raise(TooBigNumber("multiplying numbers"))
            del expression_list[counter + 1]
            del expression_list[counter - 1]
        elif expression_list[counter] == "/":
            expression_list[counter] = expression_list[counter-1] / expression_list[counter+1]
            if abs(expression_list[counter]) > MAX_NUMBER:
                raise(TooBigNumber("dividing numbers"))
            del expression_list[counter + 1]
            del expression_list[counter - 1]
        else:
            counter += 1
    counter = 0

    # evaluate addition and subtraction
    while counter < len(expression_list):
        if expression_list[counter] == "+":
            expression_list[counter] = expression_list[counter-1] + expression_list[counter+1]
            if abs(expression_list[counter]) > MAX_NUMBER:
                raise(TooBigNumber("adding numbers"))
            del expression_list[counter + 1]
            del expression_list[counter - 1]
        elif expression_list[counter] == "-":
            expression_list[counter] = expression_list[counter-1] - expression_list[counter+1]
            if abs(expression_list[counter]) > MAX_NUMBER:
                raise(TooBigNumber("subtracting numbers"))
            del expression_list[counter + 1]
            del expression_list[counter - 1]
        else:
            counter += 1
    
    #round final answer if close for floating point errors
    answer = atttempt_round(expression_list[0])
    

    return(answer)

#helper methods
def atttempt_round(float_value):
    if isinstance(float_value,complex):
        return float_value
    rounded_answer = int(round(float_value))
    if abs(float_value-rounded_answer) <= ROUND_NUM:
        return rounded_answer
    return float_value

#if ran by itself
if __name__ == "__main__":
    #gives display message
    print("Welcome to the Expression Evaluator!")
    print("")
    print("The expression evaluator can understand numbers, addition, subtraction, multiplication, division, exponents, pi, parenthesis, roots, e, natural logs, and factorials. Please use +-*/^π()√e∫!. (You can copy and paste non-keyboard characters into your equation, like pi).")
    print("")
    print("Follows order of operation.")
    print("")
    #calculates input
    while True:
        expression = input("Please insert your expression: ")
        try:
            print("The answer is: {}".format(evaluate_string(expression)))
        except (ZeroDivisionError, EquationSyntaxError,UnknownCharacter, TooBigNumber,OverflowError) as e:
            if isinstance(e,ZeroDivisionError):
                msg = "Attempt to divide by zero"
            else:
                msg = str(e)
            print("Error solving your equation: {}".format(msg))
