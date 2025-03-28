
import random
import os
from colorama import Fore


class Game:
    def __init__(self, words):
        self.words = words  # სიტყვების სია
        self.guessing_word = random.choice(words).lower()  # შემთხვევით ამოირჩევს სიტყვას სიიდან და ჩაწერს პატარა ასოებით
        self.attempts_max = 6  # ცდების რაოდენობა
        self.attempts_left = self.attempts_max  # დარჩენილი მცდელობები
        self.letters = set()  # შეინახავს ყველა მომხმარებლის მიერ შეყვანილ ასოს
        self.guessed_correct = set()  # შეინახავს ყველა იმ ასოს, რომელიც მომხარებელმა სწორად გამოიცნო
        self.game_finished = False  # თამაშის დასრულების სტატუსი

    # მეთოდი თუ როგორ უნდა აჩვენოს სიტყვა გამოცნობილი და გამოუცნობი ასოების შემთხვევაში
    def show_word(self):
        word_show = list()  # სიის სახით შენახული შედეგი
        for i in self.guessing_word:  # ნახავს სიტყვის თითოეულ ასოს
            if i in self.guessed_correct:  # თუ ეს ასო სწორია
                word_show.append(f"{Fore.BLUE}{i}{Fore.RESET}")  # მაშინ ამ ასოს გამოიტანს
            else:  # თუ ასო არ არის სწორი
                word_show.append("-")  # მაშინ მის ნაცვლად ტირეს დაწერს
        return " ".join(word_show)  # ვაერთიანებთ ამ სიის ელემენტებს ერთ სტრიქონში, რომლებიც ერთმანეთისგან სფეისით იქნება გამოყიფილი, რომ აღქმადი იყოს

    # ამოწმებს მომხმარებლსი მიერ შეყვანილი ასო არის თუ არა სიტყვაში
    def guess_letter(self, letter):
        if letter in self.letters:  # თუ შეყვანილი ასო მეორედ ხელახლა შეიყვანე
            print(f"⚠️ თქვენ უკვე გამოიყენეთ '{Fore.YELLOW}{letter}{Fore.RESET}'. სცადეთ სხვა ასო ⚠️")  # გეტყვის, რომ ეს ასო უკვე გამოყენებულია და სხვა ასო ცადე
            return False
        self.letters.add(letter)  # ხოლო თუ ეს ასო არ არსებობს, მაშინ ამ სიაში ჩაემატება

        if letter in self.guessing_word:  # თუ შეყვანილი ასო არის სიტყვაში
            print(f"✅ ყოჩაღ, სწორია! ასო '{Fore.GREEN}{letter}{Fore.RESET}' არის სიტყვაში ✅")  # გაცნობებს, რომ ასო სწორად გამოიცანი
            self.guessed_correct.add(letter)  # ეს ასო დაემატება სწორად გამოცნობილი ასოების სეტს

            # შევამოწმოთ, ყველა ასო გამოიცნო თუ არა
            all_guessed = True
            for i in self.guessing_word:  # ნახავს სიტყვის თითოეულ ასოს
                if i not in self.guessed_correct:  # თუ რომელიმე ამ სიტყვის ასო არ არის სწორად გამოცენული ასოების სეტში
                    all_guessed = False  # ესე იგი, ყველა ასო არ გამოუცნია
                    break  # და თამაშის გაგრძლებას აზრი არ აქვს და ციკლიდან უნდა გამოვიდეთ

            if all_guessed:  # თუ ყველა ასო გამოიცნო
                self.game_finished = True  # მაშინ, თამაში დასრულებულია
            return True  # სწორი ასო შეიყვანე

        else:  # თუ არასწორი ასო შეიყვანე
            print(f"❌ სამწუხაროდ, ასო '{Fore.RED}{letter}{Fore.RESET}' არ არის სიტყვაში ❌")
            self.attempts_left = self.attempts_left - 1  # მცდელობების რაოდენობას ვამცირებთ
            if self.attempts_left == 0:  # თუ მცდელობების რაოდენობა ამოწურე
                self.game_finished = True  # თამაში დასრულდა
            return False  # არასწორი ასო შეიყვანე

    # წერს და ინახავს თამაშის შედეგებს, რომ მერე შეძლო გადახედვა
    def results_save(self, guess):  # guess აქვს True ან False მნისვნელობა
        with open("results.txt", "a",encoding="utf-8") as file:  # open ფუნქციის მეშვეობით ვქმნით ფაილს, სადაც ჩაიწერება შედეგები. 'a', ანუ append ნიშნავს, რომ ფაილს ახალი შედეგები დაემატება ნაცვლად არსებულზე გადაწერისა
            result = "გამოიცანი" if guess else "ვერ გამოიცანი"  # შედეგი, რითაც დაიწყება ახალი სტიქონი. სიტყვა "გამოიცნო" თუ "ვერ გამოიცნო"
            file.write(f"სიტყვა: {self.guessing_word}, შედეგი: {result}\n")  # ყოველი ახალი შედეგი ჩაიწერება ახალი სტრიქონით


# მეთოდი, რომელიც წაიკითხავს სიტყვების ფაილს
def read_words_file(file="C:/Users/Elene/Desktop/words.txt"):
    try:
        with open(file, "r", encoding="utf-8") as file:
            lines = []
            for i in file.readlines():
                lines.append(i.strip())
            return lines
    except FileNotFoundError:
        print("ფაილი ვერ მოიძებნა. გთხოვთ, შექმნათ შესაბამისი ფაილი")
        return []


# ფუნქცია საშუალებას აძლევს მომხმარებელს ნახოს ყველა ის შედეგი, რომელიც ადრე იქნა ჩაწერილი results.txt ფაილში
def view_results():
    if not os.path.exists("results.txt"):  # ჯერ უნდა ითამაშოს, იმისთვის, რომ შედეგებიც ნახვა შეძლოს. ამიტომ ვამოწმებთ ჯერ ფაილი არსებობს თუ არა
        print(" ⚠️ ჯერ თამაში არ დაგიწყია, ამიტომ შედეგებიც არ არის! ⚠️")  # თუ არ არსებობს, ანუ ჯერ თამაში არ დაუწყია და შესაბამის კომენტარსაც ნახავს
        return  # და ფუნქციაც დასრულდება
    with open("results.txt", "r",encoding="utf-8") as file:  # თუ ფაილი არსებობს, ვხსნით ფაილს წაკითხვის რეჟიმით და ვბეჭდავთ შედეგებს
        results = file.readlines()
        print(f"\n📊 შედეგების რაოდენობა 📊: {Fore.BLUE}{len(results)}{Fore.RESET}")

        correct = 0  # დავთვალოთ გამოცნობილი სიტყვების რაოდენობა
        incorrect = 0  # დავთვალოთ ვერ გამოცნობილი სიტყვების რაოდენობა

        for i in results:
            if "შედეგი: გამოიცანი" in i:  # თუ გამოიცანი
                correct = correct + 1
            elif "შედეგი: ვერ გამოიცანი" in i:  # ვერ გამოიცანი
                incorrect = incorrect + 1
        print(f"\n✅ გამოიცანი: {Fore.GREEN}{correct}{Fore.RESET}")
        print(f"❌ ვერ გამოიცანი: {Fore.RED}{incorrect}{Fore.RESET}\n")

        for i in results:
            print(i.strip())  # დაბეჭდავს დეტალურად სიტყვებს- რა გამოიცანი, რა ვერა

# ფუნქცია, რომელიც აღწერს თამაშის წესებს
def show_rules():
    print("""
    ----- 📜 თამაშის წესები 📜 -----

    1. 🧩 თქვენ უნდა გამოიცნოთ სიტყვა ასოების გამოცნობით.
    2. 🔤 ყოველ ცდაზე უნდა შეიყვანოთ მხოლოდ ერთი ასო.
    3. ✔️ თუ ასო არის სიტყვაში, ის ჩაჯდება სიტყვაში სწორ ადგილას.
    4. ❌ თუ ასო არ არის სიტყვაში, მცდელობების რაოდენობა შემცირდება.
    5. 🎯 მოიგებთ იმ შემთხევაში, თუ ყველა ასოს გამოიცნობთ მცდელობების ამოწურვამდე.
    6. 📊 თქვენი შედეგების, ანუ გამოცნობილი ან ვერ გამოცნობილი სიტყვების ნახვა, შეგიძლიათ.

    ----- 🌟 გისურვებთ წარმატებებს! 🌟 -----
    """)


# გრაფიკული გამოსახულება
class Graphic(Game):
    def __init__(self, words):
        super().__init__(words)
        self.has_drawn = False

    # სულ აქვს მომხარებელს 6 ცდა და თითოეული არასწორი ნაბიჯი გამოისახება გრაფიკულად
    def draw_hangman(self):
        stages = [
            r'''
              ----
              |  
            ''',
            r'''
              ----
              |    
              O    
            ''',
            r'''
              ----
              |    
              O    
              |    
            ''',
            r'''
              ----
              |    
              O    
             /|       
            ''',
            r'''
              ----
              |    
              O    
             /|\   
            ''',
            r'''
              ----
              |    
              O    
             /|\  
             /     
            ''',
            r'''
              ----
              |    
              O    
             /|\   
             / \   
            '''
        ]
        print(stages[self.attempts_max - self.attempts_left])  # მცდელობების მიხედვით იხატება

    def guess_letter(self, letter):
        attempts_saver = self.attempts_left  # ვიმახსოვრებთ მცდელობების რაოდენობას
        correct = super().guess_letter(letter)  # მშობლიური კლასის მეთოდის გამოძახება
        if self.attempts_left<attempts_saver:  # თუ ასო არასწორია, ანუ მცდელობები შემცირდა
            self.draw_hangman()  # დაამატებს კაცუნას ნაწილებს
        else:  # თუ ასო სწორია
            self.draw_hangman()  # უბრალოდ წინა ნახატს გამოიტანს
        return correct


# ფუნქცია, რომელიც ასრულებს სარჩევის როლს, სადაც მომხარებელს შეუძლია აირჩიოს რომელი მოქმედების განხორციელება უნდა
# წესების ნახვა, თამაშის დაწყება, შედეგების ნახვა თუ თამაშის დასრულება
def content():
    while True:
        print("""
        🎯 ----- Hangman თამაში ----- 🎯
        1. 📜 წესების ნახვა 
        2. 🎮 თამაშის დაწყება 
        3. 📊 შედეგების ნახვა 
        4. 🛑 თამაშის დასრულება 
        """)
        select = input("👉 გთხოვთ, აირჩიეთ მოქმედება: ")

        if select == "1":  # 1-იანის არჩევის შემთხვევაში ნახავს წესებს
            show_rules()

        elif select == "2":
            words_list = read_words_file("C:/Users/Elene/Desktop/words.txt")
            hangman_game = Graphic(words_list)

            while not hangman_game.game_finished:  # სანამ თამაში არ დასრულდება (ანუ სანამ მცდელობების ამოწურვამდე მომხმარებელი გამოიცნობს ან ვერ გამოიცნობს სიტყვას)
                print("\nსიტყვა:",hangman_game.show_word())  # დაბეჭდავს სიტყვას (გამოცნობილი ასოები იქნება შესაბამის ადგილას, გამოუცნობი კი ტირეების სახით)
                print(f"დარჩენილი მცდელობების რაოდენობა: {Fore.RED}{hangman_game.attempts_left}{Fore.RESET}")  # მომხარებელს ეცოდინება რამდენი მცდელობა აქვს დარჩენილი
                letter = input("შეიყვანეთ ასო: ").lower()  # მომხარებელს შეჰყავს ასო-ბგერა

                if len(letter) != 1 or not letter.isalpha() or not letter.isascii():  # თუ მომხარებელი შეიყვანს ას-ბგერის გარდა სხვა მნიშვნელობას, ან 1-ზე მეტ სიმბოლოს
                    print("⚠️ მხოლოდ ლათინური ასო-ბგერის შეყვანის უფლება გაქვთ. გთხოვთ, სცადოთ თავიდან ⚠️")  # მომხარებელი მიიღებს შესაბამის გაფრთხილებას
                    continue

                correct = hangman_game.guess_letter(letter)

            if all(letter in hangman_game.guessed_correct for letter in
                   hangman_game.guessing_word):  # თუ ყველა ასო გამოიცნო
                print(f"\n🎉🎉🎉 გილოცავთ! თქვენ გამოიცანით სიტყვა: {Fore.GREEN}{hangman_game.guessing_word}{Fore.RESET} 🎉🎉🎉")
                hangman_game.results_save(guess=True)
            else:  # თუ ვერ გამოიცნო
                print(f"\n👎 სამწუხაროდ, თქვენ ვერ გამოიცანით სიტყვა. სიტყვა იყო: {Fore.RED}{hangman_game.guessing_word}{Fore.RESET} 👎")
                hangman_game.results_save(guess=False)

        elif select == "3":  # 3-იანის არჩევის შემთხვევაში ნახავს შედეგებს
            view_results()

        elif select == "4":  # 4-იანის არჩევის შემთხვევაში თამაში დასრულდება
            print("🙏 მადლობა მონაწილეობისთვის! გისურვებთ წარმატებას! 👋")
            open("results.txt", "w", encoding="utf-8").close() # წაშალოს ინოფრმაცია ფაილში
            break

        else:  # თუ 1,2,3 და 4-ის გარდა სხვა მნიშვნელობას შეიყვანს
            print("⚠️ გთხოვთ, აირჩიეთ ციფრი 1-დან 4-მდე! ⚠️")


def main():
    try:
        content()
    except KeyboardInterrupt:
        print("\n🛑 თამაში შეჩერებულია. მადლობას გიხდით მონაწილეობისთვის!")

if __name__ == "__main__":
    main()