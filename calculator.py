import math


class Calculator:
    def addition(self, *args):
        return sum(args)

    def multiplication(self, *args):
        return math.prod(args)

    def subtraction(self, *args):
        if len(args) < 2:
            raise ValueError("At least two values are needed for substraction.")
        result = args[0]
        for val in args[1:]:
            result -= val
        return result

    def division(self, *args):
        if len(args) < 2:
            raise ValueError("At least two values are needed for division.")

        if 0 in args:
            raise ValueError("Can not divide by zero.")

        result = args[0]
        for val in args[1:]:
            result //= val
        return result


if __name__ == "__main__":
    calc = Calculator()
