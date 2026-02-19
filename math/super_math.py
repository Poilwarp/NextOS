import math
from decimal import Decimal, getcontext
from typing import Union

Number = Union[int, float, Decimal]

class MathLib:
    def __init__(self, precision: int = 28):
        getcontext().prec = precision
    
    @staticmethod
    def plus(a: Number, b: Number) -> Decimal:
        return Decimal(str(a)) + Decimal(str(b))
    
    @staticmethod
    def minus(a: Number, b: Number) -> Decimal:
        return Decimal(str(a)) - Decimal(str(b))
    
    @staticmethod
    def mplus(a: Number, b: Number) -> Decimal:
        return Decimal(str(a)) * Decimal(str(b))
    
    @staticmethod
    def mminus(a: Number, b: Number) -> Decimal:
        if Decimal(str(b)) == 0:
            raise ZeroDivisionError("Division by zero")
        return Decimal(str(a)) / Decimal(str(b))
    
    @staticmethod
    def deg(a: Number, b: Number) -> Decimal:
        return Decimal(str(a)) ** Decimal(str(b))
    
    @staticmethod
    def root(a: Number, n: Number) -> Decimal:
        n_dec = Decimal(str(n))
        if n_dec == 0:
            raise ValueError("Root degree cannot be zero")
        return Decimal(str(a)) ** (Decimal("1") / n_dec)
    
    @staticmethod
    def log(a: Number, base: Number = math.e) -> Decimal:
        a_dec = Decimal(str(a))
        base_dec = Decimal(str(base))
        if a_dec <= 0 or base_dec <= 0 or base_dec == 1:
            raise ValueError("Invalid arguments for logarithm")
        return a_dec.ln() / base_dec.ln()
    
    @staticmethod
    def sin(x: Number) -> Decimal:
        x_dec = Decimal(str(x))
        return Decimal(math.sin(float(x_dec)))
    
    @staticmethod
    def cos(x: Number) -> Decimal:
        x_dec = Decimal(str(x))
        return Decimal(math.cos(float(x_dec)))
    
    @staticmethod
    def tet(a: Number, n: int) -> Decimal:
        if n < 0:
            raise ValueError("Tetration requires non-negative integer height")
        result = Decimal("1")
        for _ in range(n):
            result = Decimal(str(a)) ** result
        return result
    
    @staticmethod
    def untet(a: Number, b: Number, max_iter: int = 1000) -> float:
        def tetration_height(x, target, height):
            result = Decimal("1")
            for h in range(height):
                result = Decimal(str(x)) ** result
                if result > target:
                    return h, result
            return height, result
        
        low, high = 0, max_iter
        for _ in range(max_iter):
            mid = (low + high) / 2
            h, val = tetration_height(a, b, int(mid))
            if abs(val - b) < 1e-10:
                return mid
            elif val < b:
                low = mid
            else:
                high = mid
        return (low + high) / 2
    
    @staticmethod
    def pen(a: Number, n: int) -> Decimal:
        if n < 0:
            raise ValueError("Pentation requires non-negative integer height")
        result = Decimal("1")
        for _ in range(n):
            result = MathLib.tet(a, int(result))
        return result
    
    @staticmethod
    def unpen(a: Number, b: Number, max_iter: int = 100) -> float:
        def pentation_height(x, target, height):
            result = Decimal('1')
            for h in range(height):
                result = MathLib.tet(x, int(result))
                if result > target:
                    return h, result
            return height, result
        
        low, high = 0, max_iter
        for _ in range(max_iter):
            mid = (low + high) / 2
            h, val = pentation_height(a, b, int(mid))
            if abs(val - b) < 1e-10:
                return mid
            elif val < b:
                low = mid
            else:
                high = mid
        return (low + high) / 2
        
sm = MathLib()       