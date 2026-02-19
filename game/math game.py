import random
while True:
        mode = input("mode: easy, normal, hard, madness, genius: ")
        if mode == "easy":
            a = random.randint(1, 50)
            b = random.randint(1, 50)
            oper = random.randint(1, 2)
            if oper == 1:
                answer = a+b
                print(f"{a} + {b}")
            elif oper == 2:
                answer = a-b
                print(f"{a} - {b}")    
            user_answer = input("answer: ")   
            if str(user_answer).lower() == "exit":
                break
            elif int(user_answer) == answer:
                print("правильно")
            else:
                print(f"неправильно! ответ: {answer}")
                 
        if mode == "normal":
            a = random.randint(1, 100)
            b = random.randint(1, 100)
            oper = random.randint(1, 2)
            if oper == 1:
                answer = a+b
                print(f"{a} + {b}")
            elif oper == 2:
                answer = a-b
                print(f"{a} - {b}")    
            user_answer = input("answer: ")   
            if str(user_answer).lower() == "exit":
                break
            elif int(user_answer) == answer:
                print("правильно")
            else:
                print(f"неправильно! ответ: {answer}")
                  
        if mode == "hard":
            a = random.randint(1, 100)
            b = random.randint(1, 100)
            oper = random.randint(1, 4)
            if oper == 1:
                answer = a+b
                print(f"{a} + {b}")
            elif oper == 2:
                answer = a-b
                print(f"{a} - {b}")
            elif oper == 3:
                answer = a*b
                print(f"{a} × {b}")
            elif oper == 4:
                answer = a/b
                print(f"{a} ÷ {b}")            
            user_answer = input("answer: ")   
            if str(user_answer).lower() == "exit":
                break
            elif int(user_answer) == answer:
                print("правильно")
            else:
                print(f"неправильно! ответ: {answer}")                                 
        if mode == "madness":
            a = random.randint(1, 100)
            b = random.randint(1, 100)
            c = random.randint(1, 100)
            oper = random.randint(1, 12)
            if oper == 1:
                answer = a+b+c
                print(f"{a} + {b} + {c}")
            elif oper == 2:
                answer = a-b-c
                print(f"{a} - {b} - {c}")
            elif oper == 3:
                answer = a*b*c
                print(f"{a} × {b} × {c}")
            elif oper == 4:
                answer = a/b/c
                print(f"{a} ÷ {b} ÷ {c}")
            elif oper == 5:
                answer = a+b-c
                print(f"{a} + {b} - {c}")
            elif oper == 6:
                answer = a-b+c
                print(f"{a} - {b} + {c}")
            elif oper == 7:
                answer = a+b*c
                print(f"{a} + {b} × {c}")
            elif oper == 8:
                answer = a+b/c
                print(f"{a} + {b} ÷ {c}")
            elif oper == 9:
                answer = a-b*c
                print(f"{a} - {b} × {c}")
            elif oper == 10:
                answer = a-b/c
                print(f"{a} - {b} ÷ {c}")
            elif oper == 11:
                answer = a/b*c
                print(f"{a} ÷ {b} × {c}")
            elif oper == 12:
                answer = a*b/c
                print(f"{a} × {b} ÷ {c}")                                        
            user_answer = input("answer: ")   
            if str(user_answer).lower() == "exit":
                break
            elif int(user_answer) == answer:
                print("правильно")
            else:
                print(f"неправильно! ответ: {answer}")
        if mode == "genius":
            a = random.randint(1, 1000)
            b = random.randint(1, 1000)
            c = random.randint(1, 1000)
            oper = random.randint(1, 12)
            if oper == 1:
                answer = a+b+c
                print(f"{a} + {b} + {c}")
            elif oper == 2:
                answer = a-b-c
                print(f"{a} - {b} - {c}")
            elif oper == 3:
                answer = a*b*c
                print(f"{a} × {b} × {c}")
            elif oper == 4:
                answer = a/b/c
                print(f"{a} ÷ {b} ÷ {c}")
            elif oper == 5:
                answer = a+b-c
                print(f"{a} + {b} - {c}")
            elif oper == 6:
                answer = a-b+c
                print(f"{a} - {b} + {c}")
            elif oper == 7:
                answer = a+b*c
                print(f"{a} + {b} × {c}")
            elif oper == 8:
                answer = a+b/c
                print(f"{a} + {b} ÷ {c}")
            elif oper == 9:
                answer = a-b*c
                print(f"{a} - {b} × {c}")
            elif oper == 10:
                answer = a-b/c
                print(f"{a} - {b} ÷ {c}")
            elif oper == 11:
                answer = a/b*c
                print(f"{a} ÷ {b} × {c}")
            elif oper == 12:
                answer = a*b/c
                print(f"{a} × {b} ÷ {c}")                                        
            user_answer = input("answer: ")   
            if str(user_answer).lower() == "exit":
                break
            elif int(user_answer) == answer:
                print("правильно")
            else:
                print(f"неправильно! ответ: {answer}")