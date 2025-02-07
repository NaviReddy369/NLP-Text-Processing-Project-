import re
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
from nltk.sentiment import SentimentIntensityAnalyzer

# Download necessary NLTK resources
nltk.download(['punkt', 'stopwords', 'wordnet', 'vader_lexicon'])

def clean_text(
    text,
    remove_digits=True,
    remove_urls=True,
    remove_emails=True,
    remove_html=True,
    lowercase=True,
    remove_special_chars=True
):
    """
    Clean raw text with multiple optional preprocessing steps.
    
    Parameters:
        text (str): Input text to clean
        remove_digits (bool): Remove all digits
        remove_urls (bool): Remove URLs
        remove_emails (bool): Remove email addresses
        remove_html (bool): Remove HTML tags
        lowercase (bool): Convert to lowercase
        remove_special_chars (bool): Remove non-alphabetic characters
    
    Returns:
        str: Cleaned text
    """
    # Replace non-breaking spaces
    text = text.replace('\xa0', ' ')
    
    # Remove URLs
    if remove_urls:
        text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Remove emails
    if remove_emails:
        text = re.sub(r'\S+@\S+', '', text)
    
    # Remove HTML tags
    if remove_html:
        text = re.sub(r'<[^>]+>', '', text)
    
    # Remove digits and citation brackets
    if remove_digits:
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\[\d+\]', '', text)
    
    # Remove special characters
    if remove_special_chars:
        text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Convert to lowercase
    if lowercase:
        text = text.lower()
    
    return text.strip()

def process_text(
    text,
    clean=True,
    tokenize=True,
    remove_stopwords=True,
    lemmatize=True,
    language='english'
):
    """
    Full NLP preprocessing pipeline for text.
    
    Parameters:
        text (str): Raw input text
        clean (bool): Enable text cleaning
        tokenize (bool): Tokenize into words
        remove_stopwords (bool): Remove stopwords
        lemmatize (bool): Lemmatize tokens
        language (str): Language for stopwords
    
    Returns:
        list: Processed tokens
    """
    if clean:
        text = clean_text(text)
    
    # Tokenization
    tokens = word_tokenize(text) if tokenize else text.split()
    
    # Stopword removal
    if remove_stopwords:
        stop_words = set(stopwords.words(language))
        tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatization
    if lemmatize:
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return tokens

def process_large_file(file_path, batch_size=1000, **kwargs):
    """
    Generator to process large files line by line.
    
    Parameters:
        file_path (str): Path to input file
        batch_size (int): Lines to yield at a time
        kwargs: Arguments for process_text
    
    Yields:
        list: Batch of processed tokens
    """
    with open(file_path, 'r') as file:
        batch = []
        for line in file:
            processed_tokens = process_text(line, **kwargs)
            batch.extend(processed_tokens)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

def analyze_sentiment(text):
    """
    Analyze sentiment polarity using VADER.
    
    Parameters:
        text (str): Input text
    
    Returns:
        dict: Sentiment scores
    """
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)

def main():
    # Example usage
    input_file = 'about_india.txt'
    
    # Process file in batches (memory-efficient for large files)
    word_counter = Counter()
    for batch in process_large_file(input_file):
        word_counter.update(batch)
    
    total_words = sum(word_counter.values())
    print(f"Total words processed: {total_words}")
    print("\nTop 10 frequent words:")
    for word, freq in word_counter.most_common(10):
        print(f"{word}: {freq}")
    
    # N-gram analysis example
    sample_tokens = [token for batch in process_large_file(input_file) for token in batch]
    bigram_counts = Counter(ngrams(sample_tokens, 2))
    print("\nTop 5 bigrams:")
    for bigram, count in bigram_counts.most_common(5):
        print(f"{' '.join(bigram)}: {count}")
    
    # Sentiment analysis example (with different preprocessing)
    with open(input_file, 'r') as file:
        raw_text = file.read()
    
    # Preserve punctuation for sentiment analysis
    cleaned_text = clean_text(raw_text, 
                             remove_special_chars=False, 
                             lowercase=False)
    sentiment = analyze_sentiment(cleaned_text)
    print("\nSentiment analysis scores:")
    print(sentiment)

if __name__ == "__main__":
    main()
