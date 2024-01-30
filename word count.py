def count_words(input_text):
    """
    Count the number of words in the given input text.

    Parameters:
    input_text (str): The input text to be processed.

    Returns:
    int: The number of words in the input text.
    """
    # Check if the input is empty
    if not input_text.strip():
        return 0
    
    # Split the input text into words using whitespace as the delimiter
    words = input_text.split()

    # Return the count of words
    return len(words)

def get_user_input():
    """
    Prompt the user to enter a sentence or paragraph.

    Returns:
    str: The user-inputted text.
    """
    return input("Please enter a sentence or paragraph: ")

def display_word_count(word_count):
    """
    Display the word count to the console.

    Parameters:
    word_count (int): The number of words to be displayed.
    """
    print(f"Word count: {word_count}")

def main():
    # Get user input
    user_input = get_user_input()

    # Call the function to count words
    word_count = count_words(user_input)

    # Display the word count to the console
    display_word_count(word_count)

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
