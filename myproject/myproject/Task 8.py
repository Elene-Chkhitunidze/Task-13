#Task 1

w1=str(input("Please enter a word: "))
w2=str(input("Please enter a word: "))

def isanagram(word1,word2):
    if sorted(word1)==sorted(word2):
        return 'These two words are anagram'
    else:
        return 'These two words are not anagram'

print(isanagram(w1,w2))


#Task 2

text=str(input("Please enter a word: "))
symbol=str(input("Please enter a symbol: "))


def symbolsCount(t,s):
    counter = 0
    for i in t:
        if s==i:
            counter=counter+1

    return counter

print(symbolsCount(text,symbol))


#Task 3

fib= int(input("Please enter a number: "))
def fibonacci(n):
    first = 0
    second = 1
    number = 0
    lt = [0, 1]
    while n-2>0:
     number=first+second
     first=second
     second=number
     lt.append(number)
     n=n-1
    return lt


print(fibonacci(fib))










