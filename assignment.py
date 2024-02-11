import nltk
from nltk.tokenize import word_tokenize
import os
import re

nltk.download('punkt')

# Load
corpus = 'corpus1'

# Store a tuple of (document_id, tokens)
document_tokens = []

# PREPROCESS


def preprocess_texts(corpus_texts):
    tokens = re.findall(r'\b[\w-]+\b', corpus_texts)
    normalized_tokens = [token.lower() for token in tokens]
    return normalized_tokens

# Load and preprocess each document
for filename in os.listdir(corpus):
    if filename.endswith('.txt'):
        filepath = os.path.join(corpus, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
            tokens = preprocess_texts(text)
            document_tokens.append((filename, tokens))



# Inverted Index
inverted_index = {}

for docment_id, tokens in document_tokens:
    for token in tokens:
        if token not in inverted_index:
            inverted_index[token] = set()
        inverted_index[token].add(docment_id)



# Searching algos

def search_and(terms):
    if not terms:
        return set()

    if terms[0] in inverted_index:
        result_set = inverted_index[terms[0]]
    else:
        return set()

    for term in terms[1:]:
        if term in inverted_index:
            result_set = result_set.intersection(inverted_index[term])
        else:
            return set()

    return result_set



def search_or(terms):
    if not terms:
        return set()  

    result_set = set()  


    for term in terms:
        if term in inverted_index:
            result_set = result_set.union(inverted_index[term])

    return result_set


def search_for_term(term):
    if term in inverted_index:
        return inverted_index[term]
    else:
        return set()

all_docs = set(doc_id for doc_id, _ in document_tokens)

def search_and_not(include_terms, exclude_terms):
    included_docs = search_and(include_terms) if include_terms else all_docs
    excluded_docs = set.union(*(inverted_index.get(term, set()) for term in exclude_terms)) if exclude_terms else set()
    return included_docs - excluded_docs



# REPL for usage
while True:
    query = input("Enter your search query (or type 'exit' to quit): ").strip()
    if query.lower() == 'exit':
        break

    # Normalize the entire query for consistent case handling
    query = query.lower()

    # Handling AND_NOT separately to ensure it doesn't conflict with AND or NOT
    if 'and_not?' in query:
        parts = query.split('and_not?')
        if len(parts) == 2 and '?' in parts[1]:
            include_str, exclude_str = parts[1].split('?')
            include_terms = include_str.strip().split()
            exclude_terms = exclude_str.strip().split()

            results = search_and_not(include_terms, exclude_terms)
        else:
            print("Invalid AND_NOT query format.")
    # Handling AND, OR, NOT
    elif '?' in query:
        operator, terms_str = query.split('?', 1)  # Split only on the first '?'
        terms = terms_str.strip().split()

        if operator == "and":
            results = search_and(terms)
        elif operator == "or":
            results = search_or(terms)
        else:
            print("Unsupported operator or incorrect query format.")
            continue
    else:
        # Handle single-term searches without any operator
        results = search_for_term(query)

    print("Found documents:", results)

