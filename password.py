import random
import string

def generate_password(length=12):
    """Generate a random password with at least one uppercase letter, one lowercase letter,
       one number, and one special character."""
    # Define the character sets
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = '!@#$%^&*()'

    # Ensure at least one character from each category
    password = [random.choice(lowercase_letters),
                random.choice(uppercase_letters),
                random.choice(digits),
                random.choice(special_characters)]

    # Fill the rest of the password length with random characters
    remaining_length = length - 4
    password.extend(random.choices(lowercase_letters + uppercase_letters + digits + special_characters, k=remaining_length))

    # Shuffle the password to ensure randomness
    random.shuffle(password)

    # Convert the list to a string
    password = ''.join(password)
    return password

def main():
    print("Welcome to the Password Generator!")

    while True:
        try:
            num_passwords = int(input("How many passwords would you like to generate? "))
            length = int(input("Enter the length for each password: "))

            for _ in range(num_passwords):
                password = generate_password(length)
                print("Generated Password:", password)

            break
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
