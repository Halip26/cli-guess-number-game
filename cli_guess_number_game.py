import random

max_attempts = 10
attempts = 0
number = random.randint(1, 99)

print("--- Welcome to Guess the Number Game! ---")
name = input("What is your name: ")
print(f"Hello {name} You have {max_attempts} attempts to guess")

while attempts < max_attempts:
    guess = int(input("\nGuess the number from 1 to 99: "))
    print("-" * 35)

    if guess < number:
        print(f"Your guess is low {name}")
    elif guess > number:
        print(f"Your guess is high {name}")
    else:
        print(f"Congratulations {name} You guessed it!")
        break

    attempts += 1
    print(f"Attempts remaining: {max_attempts - attempts}")
else:
    print(f"Out of attempts, You Lost. The number was {number}")


# The simple one
"""
import random

number = random.randint(1, 99)
guess = int(input("Enter a number from 1 to 99: "))

while True:
    if guess < number:
        print("Your guess is low")
        guess = int(input("Enter a number from 1 to 99: "))
    elif guess > number:
        print("Your guess is high")
        guess = int(input("Enter a number from 1 to 99: "))
    else:
        print("Congrats, you guessed it!")
        break
        
"""
