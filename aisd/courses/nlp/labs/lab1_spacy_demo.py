"""
Lab 1 Part 2: spaCy Demo

Installation:
    conda install -c conda-forge spacy
    python -m spacy download en_core_web_sm

Import and Load Model:
    python
    >>> import spacy
    >>> nlp = spacy.load('en_core_web_sm')
"""

import spacy

# Load the English language model
nlp = spacy.load('en_core_web_sm')

# Sample text about Sebastian Thrun and self-driving cars
text = ("When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. \"I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn't "
        "worth talking to,\" said Thrun, in an interview with Recode earlier "
        "this week.")

# Process the text with spaCy
doc = nlp(text)

# Extract and print noun phrases and verbs
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
