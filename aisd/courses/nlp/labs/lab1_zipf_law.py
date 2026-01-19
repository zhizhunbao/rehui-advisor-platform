"""
CST8507 Lab 1: Zipf's Law and Text Analysis

Author: [Your Name]
Section: [Your Section]
Date: [Date]

Empirically verify Zipf's Law: word frequency ∝ 1/rank^α
"""

import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import gutenberg, stopwords

# Download NLTK data
for resource in ['gutenberg', 'punkt', 'stopwords', 'averaged_perceptron_tagger']:
    nltk.download(resource, quiet=True)


# ============================================================================
# Data Loading
# ============================================================================

def load_texts():
    """Load two texts: literary and informational."""
    text1 = gutenberg.raw('austen-emma.txt')
    text2 = gutenberg.raw('bible-kjv.txt')
    return text1, text2


# ============================================================================
# Preprocessing
# ============================================================================

def tokenize(text):
    """Tokenize and clean text: lowercase, alphabetic only."""
    tokens = word_tokenize(text)
    return [t.lower() for t in tokens if t.isalpha()]


# ============================================================================
# Analysis
# ============================================================================

def analyze_frequency(tokens):
    """Compute word frequencies and rank them."""
    fdist = FreqDist(tokens)
    sorted_freq = sorted(fdist.items(), key=lambda x: x[1], reverse=True)
    return fdist, sorted_freq


def print_stats(tokens, fdist, sorted_freq, name):
    """Print frequency statistics."""
    print(f"\n{'='*60}")
    print(f"{name}")
    print(f"{'='*60}")
    print(f"Total tokens: {len(tokens):,}")
    print(f"Vocabulary size: {len(fdist):,}")
    print(f"\nTop 20 words:")
    print(f"{'Rank':<8} {'Word':<15} {'Frequency':<10}")
    print("-" * 35)
    for rank, (word, freq) in enumerate(sorted_freq[:20], 1):
        print(f"{rank:<8} {word:<15} {freq:<10,}")


# ============================================================================
# Visualization
# ============================================================================

def plot_zipf(sorted_freq, title, color='blue'):
    """Plot Zipf's Law on log-log scale."""
    ranks = np.arange(1, len(sorted_freq) + 1)
    frequencies = [freq for _, freq in sorted_freq]
    
    plt.figure(figsize=(10, 6))
    plt.loglog(ranks, frequencies, '.', color=color, alpha=0.6)
    plt.xlabel('Rank (log scale)')
    plt.ylabel('Frequency (log scale)')
    plt.title(f"Zipf's Law: {title}")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_comparison(sorted_freq1, sorted_freq2, name1, name2):
    """Compare two Zipf distributions."""
    ranks1 = np.arange(1, len(sorted_freq1) + 1)
    freq1 = [f for _, f in sorted_freq1]
    
    ranks2 = np.arange(1, len(sorted_freq2) + 1)
    freq2 = [f for _, f in sorted_freq2]
    
    plt.figure(figsize=(12, 7))
    plt.loglog(ranks1, freq1, '.', color='blue', alpha=0.6, label=name1)
    plt.loglog(ranks2, freq2, '.', color='green', alpha=0.6, label=name2)
    plt.xlabel('Rank (log scale)')
    plt.ylabel('Frequency (log scale)')
    plt.title("Zipf's Law: Comparative Analysis")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# ============================================================================
# Main Analysis
# ============================================================================

if __name__ == "__main__":
    
    # Step 1-2: Load and tokenize
    print("Loading texts...")
    text1_raw, text2_raw = load_texts()
    
    print("Tokenizing...")
    tokens1 = tokenize(text1_raw)
    tokens2 = tokenize(text2_raw)
    
    # Step 3-4: Analyze frequencies
    fdist1, sorted_freq1 = analyze_frequency(tokens1)
    fdist2, sorted_freq2 = analyze_frequency(tokens2)
    
    print_stats(tokens1, fdist1, sorted_freq1, "Emma (Literary)")
    print_stats(tokens2, fdist2, sorted_freq2, "Bible (Informational)")
    
    # Step 4: Plot individual distributions
    plot_zipf(sorted_freq1, "Emma", 'blue')
    plot_zipf(sorted_freq2, "Bible", 'green')
    
    # Step 5: Comparative analysis
    plot_comparison(sorted_freq1, sorted_freq2, "Emma", "Bible")
    
    print("\n" + "="*60)
    print("TODO: Write comparative analysis in Lab1.docx")
    print("="*60)
    
    # Step 6.1: Remove stopwords
    print("\n\nRemoving stopwords...")
    stop_words = set(stopwords.words('english'))
    tokens1_no_stop = [t for t in tokens1 if t not in stop_words]
    
    fdist_no_stop, sorted_no_stop = analyze_frequency(tokens1_no_stop)
    print_stats(tokens1_no_stop, fdist_no_stop, sorted_no_stop, 
                "Emma (No Stopwords)")
    plot_zipf(sorted_no_stop, "Emma (No Stopwords)", 'red')
    
    print("\n" + "="*60)
    print("TODO: Discuss impact of removing stopwords")
    print("="*60)
    
    # Step 6.2: Nouns only
    print("\n\nExtracting nouns...")
    pos_tags = nltk.pos_tag(tokens1)
    nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
    
    fdist_nouns, sorted_nouns = analyze_frequency(nouns)
    print_stats(nouns, fdist_nouns, sorted_nouns, "Emma (Nouns Only)")
    plot_zipf(sorted_nouns, "Emma (Nouns Only)", 'purple')
    
    print("\n" + "="*60)
    print("TODO: Discuss impact of POS filtering")
    print("="*60)
    
    print("\n\nLab completed! Write your analysis in Lab1.docx")
