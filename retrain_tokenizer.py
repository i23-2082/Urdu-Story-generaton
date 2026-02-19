import pandas as pd
import os
import sys
import pickle

# Add the Tokenizer directory to the path
sys.path.append(os.path.join(os.getcwd(), "Tokenizer"))
from bpe_tokenizer import BPETokenizer

def train_tokenizer():
    corpus_path = "PreProcessing/urdu_stories_processed.csv"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        return

    print("Loading corpus...")
    df = pd.read_csv(corpus_path)
    # Combine all stories into a list of strings, filter out anything not a string
    texts = [str(t) for t in df['content'].dropna().tolist() if isinstance(t, (str, bytes)) or pd.notnull(t)]
    # Double check for empty strings or non-string leftovers
    texts = [t for t in texts if len(t) > 0]
    
    print(f"Total stories after cleaning: {len(texts)}")
    full_text = "\n".join(texts)
    
    vocab_size = 1500
    print(f"Training Byte-level BPE Tokenizer with vocab_size={vocab_size}...")
    
    tokenizer = BPETokenizer(vocab_size=vocab_size)
    tokenizer.train(full_text)
    
    output_path = "Tokenizer/bpe_tokenizer.pkl"
    tokenizer.save(output_path)
    print(f"Tokenizer trained and saved to {output_path}")
    print(f"Final vocab size: {len(tokenizer.vocab)}")

if __name__ == "__main__":
    train_tokenizer()
