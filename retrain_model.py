import pandas as pd
import numpy as np
import pickle
import os
import sys
from collections import Counter, defaultdict

# Add the root directory to path to import tokenizer
sys.path.append(os.getcwd())
# Alias bpe_tokenizer to tokenizer for pickle loading
import Tokenizer.bpe_tokenizer as bpe_tokenizer
sys.modules['bpe_tokenizer'] = bpe_tokenizer
from Tokenizer.bpe_tokenizer import BPETokenizer

class TrigramLanguageModel:
    def __init__(self, lambda1=0.1, lambda2=0.3, lambda3=0.6):
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.lambda3 = lambda3
        
        # Using unigram, bigram, trigram as Counter names to match service loader
        self.unigram = Counter()
        self.bigram = Counter()
        self.trigram = Counter()
        
        self.bigram_totals = Counter()
        self.unigram_totals = Counter()
        
        self.total_tokens = 0
        self.vocab = set()

    def train(self, corpus, start_id):
        print("Training trigram model...")
        for tokens in corpus:
            # For trigram, we need two START tokens
            full_tokens = [start_id, start_id] + tokens
            self.total_tokens += len(full_tokens)

            for i in range(len(full_tokens)):
                w3 = full_tokens[i]
                self.unigram[w3] += 1
                self.vocab.add(w3)

                if i >= 1:
                    w2 = full_tokens[i-1]
                    self.bigram[(w2, w3)] += 1
                    self.unigram_totals[w2] += 1

                if i >= 2:
                    w1, w2 = full_tokens[i-2], full_tokens[i-1]
                    self.trigram[(w1, w2, w3)] += 1
                    self.bigram_totals[(w1, w2)] += 1
        print(f"Trigram training completed. Vocab size: {len(self.vocab)}")

def main():
    tokenizer_path = "Tokenizer/bpe_tokenizer.pkl"
    corpus_path = "PreProcessing/urdu_stories_processed.csv"
    model_output_path = "Model/trigram_model.pkl"

    if not os.path.exists(tokenizer_path):
        print(f"Error: Tokenizer not found at {tokenizer_path}")
        return

    print("Loading tokenizer...")
    tokenizer = BPETokenizer.load(tokenizer_path)
    
    print("Loading corpus...")
    df = pd.read_csv(corpus_path)
    texts = df['content'].dropna().tolist()
    
    print("Tokenizing corpus...")
    tokenized_corpus = []
    for i, text in enumerate(texts):
        tokenized_corpus.append(tokenizer.encode(str(text)))
        if (i+1) % 200 == 0:
            print(f"Tokenized {i+1} stories")

    # Byte-level BPE typically doesn't have a reserved START token unless we add one.
    # However, for consistency with the service loader, we'll use a specific ID.
    # We'll use 0 as a dummy START token if it's not being used, 
    # but in Byte BPE 0 is the null byte. 
    # Let's just pick an ID far away from vocab or use -1.
    # But current loader uses integer IDs. 
    # Let's use 0 because it's already used in model_loader context.
    start_id = 0 
    
    model = TrigramLanguageModel()
    model.train(tokenized_corpus, start_id)
    
    print(f"Saving model to {model_output_path}...")
    with open(model_output_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Model saved successfully.")

if __name__ == "__main__":
    main()
