import sys
import os
os.chdir("../math")
sys.path.insert(0, "../math")
import super_math


sm = super_math.MathLib()
example = input("операции: +, -, *, /, deg, root, log, sin, cos, tet, untet, pen, unpen. \nвыражение: ")

if "+" in example:
    a, b = map(float, example.split("+"))
    print(f"= {sm.plus(a, b)}")
    
elif "-" in example:
    a, b = map(float, example.split("-"))
    print(f"= {sm.minus(a, b)}")
elif "*" in example:
    a, b = map(float, example.split("*"))
    print(f"= {sm.mplus(a, b)}")
    
elif "/" in example:
    a, b = map(float, example.split("/"))
    print(f"= {sm.mminus(a, b)}")
    
elif "deg" in example:
    a, b = map(float, example.split("deg"))
    print(f"= {sm.deg(a, b)}")
    
elif "root" in example:
    parts = example.split("root")
    a = float(parts[0].strip())
    n = float(parts[1].strip())
    print(f"= {sm.root(a, n)}")
    
elif "log" in example:
    if "base" in example:
        parts = example.split("log")
        a = float(parts[1].split("base")[0].strip())
        base = float(parts[1].split("base")[1].strip())
        print(f"={sm.log(a, base)}")
    else:
        parts = example.split("log")
        a = float(parts[1].strip())
        print(f"={sm.log(a)}")
        
elif "sin" in example:
    a = float(example.replace("sin", "").strip())
    print(f"={sm.sin(a)}")
    
elif "cos" in example:
    a = float(example.replace("cos", "").strip())
    print(f"={sm.cos(a)}")
    
elif "tet" in example:
    parts = example.replace("tet", " ").split()
    a = float(parts[0])
    n = int(float(parts[1]))
    print(f"={sm.tet(a, n)}")
    
elif "untet" in example:
    parts = example.replace("untet", " ").split()
    a = float(parts[0])
    b = float(parts[1])
    print(f"= {sm.untet(a, b)}")
    
elif "pen" in example:
    parts = example.replace("pen", " ").split()
    a = float(parts[0])
    n = int(float(parts[1]))
    print(f"= {sm.pen(a, n)}")
    
elif "unpen" in example:
    parts = example.replace("unpen", " ").split()
    a = float(parts[0])
    b = float(parts[1])
    print(f"= {sm.unpen(a, b)}")
    
else:
    print("не нашёл такую операцию :/")