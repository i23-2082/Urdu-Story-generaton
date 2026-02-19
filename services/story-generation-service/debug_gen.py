import os
import sys
import pickle

# Add paths
sys.path.append("app")
# Alias bpe_tokenizer to tokenizer
import app.tokenizer
sys.modules['bpe_tokenizer'] = app.tokenizer

from app.tokenizer import BPETokenizer
from app.model_loader import TrigramModelLoader

def debug():
    models_dir = "models"
    tokenizer_path = os.path.join(models_dir, "bpe_tokenizer.pkl")
    model_path = os.path.join(models_dir, "trigram_model.pkl")
    
    # Load tokenizer
    tokenizer = BPETokenizer(vocab_size=250)
    tokenizer.load(tokenizer_path)
    print(f"Tokenizer loaded. Vocab size: {len(tokenizer.vocab)}")
    
    # Load model
    loader = TrigramModelLoader(model_path)
    print("Model loaded.")
    
    # Prefix
    prefix = "ایک دفعہ کا ذکر ہے"
    prefix_ids = tokenizer.encode(prefix)
    print(f"Prefix: '{prefix}'")
    print(f"Encoded prefix IDs: {prefix_ids}")
    
    # Generate
    print("\nGenerating story...")
    yielded_count = 0
    for token in loader.generate_stream(prefix_ids, tokenizer_mapping=tokenizer.id_to_token, max_length=600, min_tokens=550):
        if isinstance(token, str):
            print(f"SRV_TOKEN: {repr(token)}")
        else:
            yielded_count += 1
            # print(f"ID: {token} -> '{tokenizer.decode([token])}'") # Suppressed for clarity
    
    print(f"\nFinal yielded token count: {yielded_count}")

if __name__ == "__main__":
    debug()
