import re
from collections import Counter
def clean_text(text):
    # Replace non-breaking spaces with a regular space
    text = text.replace('\xa0', ' ')
    # Remove digits and their brackets if needed
    text = re.sub(r'\[\d+\]', '', text)
    # Remove all digits and non-alphabetic characters except spaces
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

# Function to count words in a list of lines
def count_words(lines):
    word_count = 0
    word_freq = Counter()
    for line in lines:
        words = line.split()
        word_count += len(words)
        word_freq.update(words)
    return word_count, word_freq
# clean it
with open('about_india.txt', 'r') as file:
    cleaned_lines = [clean_text(line) for line in file]
# Count words and get word frequency
total_words, word_frequencies = count_words(cleaned_lines)
# Optionally, print the first few cleaned lines (change the number to print more or fewer lines)
for line in cleaned_lines[:5]:
    print(line)
# removing non-breaking spaces, digits, and special characters
print(f"Total number of words in the file: {total_words}")
# Print the first few cleaned lines
print("\nFirst few cleaned lines:")
for line in cleaned_lines[:5]:
    print(line)
# Print the most common words
print("\nMost common words:")
for word, freq in word_frequencies.most_common(10):  # Adjust number to show more or fewer common words
    print(f"{word}: {freq}")