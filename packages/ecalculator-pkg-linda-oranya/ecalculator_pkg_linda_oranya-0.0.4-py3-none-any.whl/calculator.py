from typing import Union

class Calculator:
    """
        This class performs basic calculator functions such as:
    
        - Addition / Subtraction
        - Multiplication / Division
        - Take (n) root of number
        - Reset memory
    """

    def __init__(self, start:int = 0)-> None:
        """
          Initializes memory to 0
        """
        self.__index = start
 

    @property
    def memory_val(self):
        """
            access the memory which is always set to 0
        """
        return self.__index

    @staticmethod
    def __input_validation(number: Union[int, float]):
        """
        Validates input
        """
        if not isinstance (number, (int, float)):
            raise TypeError("only numerical inputs allowed (float or integer)")

    def reset(self):
        """
            Resets memory to 0
        """
        self.__index = 0
       

    def add(self, num: Union[int, float]):
        """
           Add num to value in the memory
        """
        self.__input_validation(num)
        self.__index += num
        return self.__index

    def subtract(self, num: Union[int, float]):
        """
          Subtracts num from value in memory
        """
        self.__input_validation(num)
        self.__index -= num
        return self.__index

    def multiply(self, num: Union[int, float]):
        """
          Multiply number by value in memory
        """
        self.__input_validation(num)
        self.__index *= num
        return self.__index

    def divide(self, num: Union[int, float]):
        """
          Divide number by value in memory
        """
        self.__input_validation(num)
        try:
            self.__index /= num
            return self.__index
        except ZeroDivisionError as err:
            print(f"number cannot be zero => {err}")

    def modulus(self, num: Union[int, float]):
        """
          Divide number by value in memory and return the reminder
        """
        self.__input_validation(num)
        try:
            self.__index %= num
            return self.__index
        except ZeroDivisionError as err:
            print(f"number cannot be zero => {err}")

    def square_root(self, num: Union[int, float]):
        """
          Find the squreroot of number given that value is > 0
        """
        self.__input_validation(num)
        if self.__index <= 0:
            raise ValueError(f"The calculator does not have the capacity to compute negative roots")
        if num <= 0:
            raise ValueError("The calculator does not have the capacity to compute negative roots")

        self.__index = self.__index**(1./num)
        return self.__index
