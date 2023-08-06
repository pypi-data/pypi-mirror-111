def add(num1, num2):
    if type(num1 or num2) is not int:
        raise TypeError("Inputs must be a number!")

    else:
        x=num1 + num2
        return x