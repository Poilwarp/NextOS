import random

def load_words():
    words = []
    try:
        with open('words.txt', 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().lower()
                if word and word.isalpha():
                    words.append(word)
    except:
        base_words = ['программирование', 'компьютер', 'информатика', 'математика', 
                     'литература', 'география', 'биология', 'история', 'философия']
        words = base_words
    return words

def get_random_word(word_list):
    while True:
        word = random.choice(word_list)
        if len(word) >= 6:
            return word

def can_form_word(main_word, candidate):
    main_letters = list(main_word)
    for letter in candidate:
        if letter in main_letters:
            main_letters.remove(letter)
        else:
            return False
    return True

def play_game():
    print("=== ИГРА 'СЛОВА ИЗ СЛОВ' ===")
    print("Составь слова из слов")
    
    all_words = load_words()
    main_word = get_random_word(all_words)
    used_words = set()
    score = 0
    
    print(f"\n слово: {main_word.upper()}")
    print(f"Буквы: {', '.join(main_word.upper())}")
    
    with open('word_variants.txt', 'r', encoding='utf-8') as f:
        possible_words = [line.strip().lower() for line in f if line.strip()]
    
    valid_possible_words = [w for w in possible_words if can_form_word(main_word, w)]
    
    while True:
        print(f"\nСчет: {score} | Угадано слов: {len(used_words)}")
        guess = input("Ваше слово: ").strip().lower()
        
        if guess == 'стоп':
            print(f"\n игра завершена! Итоговый счет: {score}")
            print(f"Вы нашли слов: {len(used_words)}")
            if valid_possible_words:
                print(f"Всего можно было составить слов: {len(valid_possible_words)}")
            break
            
        elif guess == 'помощь':
            if valid_possible_words:
                not_guessed = [w for w in valid_possible_words if w not in used_words]
                if not_guessed:
                    hint = random.choice(not_guessed)
                    print(f"Подсказка: попробуйте слово из {len(hint)} букв")
                else:
                    print("Вы уже угадали все возможные слова!")
            else:
                print("Нет доступных подсказок")
            continue
        
        if len(guess) < 3:
            print("Слово должно содержать минимум 3 буквы!")
            continue
            
        if guess in used_words:
            print("Это слово уже было!")
            continue
            
        if not guess.isalpha():
            print("Используйте только буквы!")
            continue
            
        if not can_form_word(main_word, guess):
            print("Нельзя использовать буквы, которых нет в основном слове!")
            continue
            
        if guess not in possible_words:
            print("Такого слова нет в словаре!")
            continue
        
        used_words.add(guess)
        points = len(guess) * 2
        score += points
        
        print(f"Правильно! +{points} очков")
        
        if len(used_words) == len(valid_possible_words):
            print("\n ура! Вы нашли все возможные слова!")
            print(f"Итоговый счет: {score}")
            break
    
    if valid_possible_words and len(used_words) < len(valid_possible_words):
        print("\nНеиспользованные слова, которые можно было составить:")
        missed = [w for w in valid_possible_words if w not in used_words]
        for i, word in enumerate(sorted(missed, key=len, reverse=True)[:10], 1):
            print(f"{i}. {word} ({len(word)} букв)")
        if len(missed) > 10:
            print(f"... и еще {len(missed) - 10} слов")

def main():
    print("Добро пожаловать в игру 'Слова из слов'!")
    
    while True:
        play_game()
        
        again = input("\nХочешь сыграть еще раз? (да/нет): ").lower()
        if again != 'да':
            print("ты уже ухожишь? пока! :/")
            break
            
play_game()            