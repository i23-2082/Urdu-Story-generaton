import pickle
import numpy as np
import random
from typing import List, Tuple
from collections import Counter

class TrigramLanguageModel:
    def __init__(self, lambda1=0.1, lambda2=0.3, lambda3=0.6):
        # Placeholder matching the notebook structure
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.lambda3 = lambda3
        self.unigram = Counter()
        self.bigram = Counter()
        self.trigram = Counter()
        self.bigram_totals = Counter()
        self.unigram_totals = Counter()
        self.total_tokens = 0
        self.vocab = set()

    def train(self, tokenized_corpus):
        for tokens in tokenized_corpus:
            self.total_tokens += len(tokens)
            for i in range(len(tokens)):
                self.unigram_counts[tokens[i]] += 1
                self.vocab.add(tokens[i])
                if i >= 1:
                    bigram = (tokens[i-1], tokens[i])
                    self.bigram_counts[bigram] += 1
                if i >= 2:
                    trigram = (tokens[i-2], tokens[i-1], tokens[i])
                    self.trigram_counts[trigram] += 1

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'TrigramLanguageModel':
            return TrigramLanguageModel
        return super().find_class(module, name)

class TrigramModelLoader:
    def __init__(self, model_path: str):
        # We need TrigramLanguageModel in the namespace for pickle to work
        # If the model was saved as an instance of TrigramLanguageModel
        with open(model_path, 'rb') as f:
            unpickler = CustomUnpickler(f)
            model_obj = unpickler.load()
            
        if isinstance(model_obj, TrigramLanguageModel):
            self.unigram = model_obj.unigram
            self.bigram = model_obj.bigram
            self.trigram = model_obj.trigram
            self.unigram_totals = model_obj.unigram_totals
            self.bigram_totals = model_obj.bigram_totals
            self.total_tokens = model_obj.total_tokens
            self.vocab = list(model_obj.vocab)
            self.vocab_set = model_obj.vocab
            self.lambda1 = model_obj.lambda1
            self.lambda2 = model_obj.lambda2
            self.lambda3 = model_obj.lambda3
        else:
            # Fallback for the dictionary format if it exists
            data = model_obj
            self.unigram = data['unigram']
            self.bigram = data['bigram']
            self.trigram = data['trigram']
            self.unigram_totals = data.get('unigram_totals', Counter())
            self.bigram_totals = data.get('bigram_totals', Counter())
            self.total_tokens = data['total_tokens']
            self.vocab = list(data['vocab'])
            self.vocab_set = data['vocab']
            self.lambda1 = data['lambda1']
            self.lambda2 = data['lambda2']
            self.lambda3 = data['lambda3']

        self.EOS = '\uFFF0'
        self.EOP = '\uFFF1'
        self.EOT = '\uFFF2'
        self.BOS = '<BOS>'

    def mle_trigram_prob(self, w_i: str, w_i1: str, w_i2: str) -> float:
        denom = self.bigram_totals.get((w_i2, w_i1), 0)
        if denom == 0:
            return 0.0
        return self.trigram.get((w_i2, w_i1, w_i), 0) / denom

    def mle_bigram_prob(self, w_i: str, w_i1: str) -> float:
        denom = self.unigram_totals.get(w_i1, 0)
        if denom == 0:
            return 0.0
        return self.bigram.get((w_i1, w_i), 0) / denom

    def mle_unigram_prob(self, w_i: str) -> float:
        return self.unigram.get(w_i, 0) / self.total_tokens if self.total_tokens else 0

    def interpolated_prob(self, w_i: str, w_i1: str, w_i2: str) -> float:
        p_tri = self.mle_trigram_prob(w_i, w_i1, w_i2)
        p_bi = self.mle_bigram_prob(w_i, w_i1)
        p_uni = self.mle_unigram_prob(w_i)
        # Note: notebook uses lambda3 for trigram, lambda2 for bigram, lambda1 for unigram
        return self.lambda3 * p_tri + self.lambda2 * p_bi + self.lambda1 * p_uni

    def get_next_token_distribution(self, w_i2: str, w_i1: str) -> Tuple[List[str], np.ndarray]:
        probs = np.array([self.interpolated_prob(t, w_i1, w_i2) for t in self.vocab], dtype=np.float64)
        total = probs.sum()
        if total > 0:
            probs /= total
        else:
            probs = np.ones(len(self.vocab)) / len(self.vocab)
        return self.vocab, probs

    def generate_stream(self, prefix: any, tokenizer_mapping: dict = None, max_length: int = 800, min_tokens: int = 600):
        """Generates a stream of tokens targeting exactly ~600-800 tokens with 5-6 sentences per paragraph."""
        # Ensure we always generate enough for the user's request
        max_length = max(max_length, 800)
        min_tokens = max(min_tokens, 600)
        
        if isinstance(prefix, str):
            prefix_tokens = prefix.split()
        else:
            prefix_tokens = list(prefix)
            
        context = [self.BOS, self.BOS] + prefix_tokens
        
        # Urdu sentence ending punctuations
        end_punctuations = {'۔', '؟', '!', '.', '?', '!'}
        special_tokens = {self.BOS, self.EOS, self.EOP, self.EOT, '\uFFF0', '\uFFF1', '\uFFF2'}

        token_count = 0
        sentences_in_para = 0
        
        # Increased loop range for safety
        for i in range(max_length * 3):
            w_i2 = context[-2]
            w_i1 = context[-1]
            
            tokens, probs = self.get_next_token_distribution(w_i2, w_i1)
            next_token = np.random.choice(tokens, p=probs)
            
            if hasattr(next_token, 'item'):
                next_token = next_token.item()
            
            # Force continue if EOT sampled too early
            if next_token == self.EOT and token_count < min_tokens:
                continue
                
            context.append(next_token)
            
            if next_token in special_tokens:
                if next_token == self.EOT:
                    break
                continue

            token_count += 1
            yield next_token
            
            token_str = ""
            if tokenizer_mapping and next_token in tokenizer_mapping:
                val = tokenizer_mapping[next_token]
                if isinstance(val, bytes):
                    token_str = val.decode('utf-8', errors='replace')
                else:
                    token_str = val
            
            # Paragraph injection logic:
            # Strictly 5-6 sentences per paragraph.
            if any(p in token_str for p in end_punctuations):
                sentences_in_para += 1
                if sentences_in_para >= random.randint(5, 6) and token_count < max_length - 80:
                    yield "\n\n"
                    sentences_in_para = 0

            # Stop conditions
            if token_count >= max_length:
                break
            
            # Stop only after hitting minimum tokens and seeing a sentence end
            if token_count >= min_tokens and any(p in token_str for p in end_punctuations):
                # Gradually increase stop probability
                if token_count > (max_length * 0.9) or np.random.random() < 0.1:
                    break

    def generate(self, prefix_text: str, tokenizer_mapping: dict = None, max_length: int = 200) -> str:
        tokens = list(self.generate_stream(prefix_text, tokenizer_mapping, max_length))
        result = []
        for t in tokens:
            if isinstance(t, str):
                result.append(t)
            elif tokenizer_mapping and t in tokenizer_mapping:
                result.append(tokenizer_mapping[t])
            else:
                result.append(str(t))
        return "".join(result).strip()
