import pickle
from collections import defaultdict, Counter

class BPETokenizer:
    def __init__(self, vocab_size=1500):
        """Initialize Byte-level BPE tokenizer"""
        self.vocab_size = vocab_size
        self.vocab = {bytes([i]): i for i in range(256)}
        self.id_to_token = {i: bytes([i]) for i in range(256)}
        self.merges = []  # List of ((p1_bytes, p2_bytes), new_token_bytes)
        self.token_id = 256
        
    def get_stats(self, split_text):
        """Find the most frequent pair of tokens in the corpus"""
        pairs = defaultdict(int)
        for tokens, freq in split_text.items():
            for i in range(len(tokens) - 1):
                pair = (tokens[i], tokens[i+1])
                pairs[pair] += freq
        return pairs
    
    def merge_vocab(self, pair, split_text):
        """Merge a frequent pair in the split text representation of the corpus"""
        new_split = {}
        for tokens, freq in split_text.items():
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i+1] == pair[1]:
                    new_tokens.append(pair[0] + pair[1])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            new_split[tuple(new_tokens)] = freq
        return new_split

    def train(self, text):
        """Train BPE tokenizer on raw text by treating it as a sequence of bytes"""
        if isinstance(text, str):
            corpus_bytes = text.encode('utf-8')
        else:
            corpus_bytes = text
            
        import re
        words = []
        current_word = []
        for b in corpus_bytes:
            current_word.append(bytes([b]))
            if b == 32: # Space
                words.append(tuple(current_word))
                current_word = []
        if current_word:
            words.append(tuple(current_word))
            
        word_counts = Counter(words)
        split_text = {word: count for word, count in word_counts.items()}
        
        num_merges = self.vocab_size - len(self.vocab)
        for i in range(num_merges):
            pairs = self.get_stats(split_text)
            if not pairs:
                break
            best_pair = max(pairs, key=pairs.get)
            new_token = best_pair[0] + best_pair[1]
            self.vocab[new_token] = self.token_id
            self.id_to_token[self.token_id] = new_token
            self.merges.append((best_pair, new_token)) 
            split_text = self.merge_vocab(best_pair, split_text)
            self.token_id += 1
        return self

    def encode(self, text):
        """Encode text into token IDs using Byte-level BPE"""
        if isinstance(text, str):
            text_bytes = text.encode('utf-8')
        else:
            text_bytes = text
        tokens = [bytes([b]) for b in text_bytes]
        for pair, new_token in self.merges:
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i+1] == pair[1]:
                    new_tokens.append(new_token)
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens
        return [self.vocab[t] for t in tokens if t in self.vocab]

    def decode(self, token_ids):
        """Decode token IDs back to a string"""
        byte_parts = [self.id_to_token.get(idx, b'') for idx in token_ids]
        full_bytes = b"".join(byte_parts)
        return full_bytes.decode('utf-8', errors='replace')

    def save(self, filepath):
        """Save tokenizer object to file"""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    def load(self, filepath):
        """Load tokenizer from file (supports instance or class call)"""
        with open(filepath, 'rb') as f:
            obj = pickle.load(f)
            
        if hasattr(obj, 'vocab'):
            self.vocab = obj.vocab
            self.merges = getattr(obj, 'merges', [])
            self.id_to_token = getattr(obj, 'id_to_token', {v: k for k, v in self.vocab.items()})
            self.vocab_size = getattr(obj, 'vocab_size', len(self.vocab))
            self.token_id = getattr(obj, 'token_id', len(self.vocab))
            
        print(f"Tokenizer loaded from {filepath}. Vocab size: {len(self.vocab)}")
        return self
