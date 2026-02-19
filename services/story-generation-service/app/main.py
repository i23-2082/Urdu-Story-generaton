from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
import os
import sys
from .schemas import GenerateRequest, GenerateResponse
from .model_loader import TrigramModelLoader
from .tokenizer import BPETokenizer

# Fix pickling issue: The model/tokenizer was saved with module name 'bpe_tokenizer'
# We alias 'bpe_tokenizer' to the service's 'app.tokenizer' module.
import app.tokenizer
sys.modules['bpe_tokenizer'] = app.tokenizer

TOKENIZER_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "bpe_tokenizer.pkl")
tokenizer = BPETokenizer(vocab_size=250)
tokenizer.load(TOKENIZER_PATH)


app = FastAPI(title="Urdu Children's Story Generation API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "trigram_model.pkl")
try:
    model_loader = TrigramModelLoader(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model_loader = None

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model_loader is not None}

@app.post("/generate", response_model=GenerateResponse)
async def generate_story(request: GenerateRequest):
    if model_loader is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # 1. Encode the prefix using BPE Tokenizer
        prefix_ids = tokenizer.encode(request.prefix)
        
        # 2. Generate tokens using the Trigram Model
        # Pass mapping for sentence boundary detection
        generated_tokens = list(model_loader.generate_stream(
            prefix_ids, 
            tokenizer_mapping=tokenizer.id_to_token, 
            max_length=request.max_length or 700
        ))
        
        # 3. Filter and Decode
        special_chars = {model_loader.BOS, model_loader.EOS, model_loader.EOP, model_loader.EOT, '\uFFF0', '\uFFF1', '\uFFF2'}
        special_ids = {tokenizer.vocab.get(char) for char in special_chars if char in tokenizer.vocab}
        
        result_parts = []
        token_ids_to_decode = []
        
        for t in generated_tokens:
            if isinstance(t, str):
                # Flush pending token IDs before adding the string (like \n\n)
                if token_ids_to_decode:
                    decoded = tokenizer.decode(token_ids_to_decode)
                    # Clean any trailing special chars from decoding
                    for sc in special_chars:
                        decoded = decoded.replace(sc, "")
                    result_parts.append(decoded)
                    token_ids_to_decode = []
                result_parts.append(t)
            elif t not in special_ids:
                token_ids_to_decode.append(t)
        
        if token_ids_to_decode:
            decoded = tokenizer.decode(token_ids_to_decode)
            for sc in special_chars:
                decoded = decoded.replace(sc, "")
            result_parts.append(decoded)
            
        generated_text = "".join(result_parts)
            
        return GenerateResponse(generated_text=request.prefix + " " + generated_text)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-stream")
async def generate_story_stream(request: GenerateRequest):
    if model_loader is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    special_chars = {model_loader.BOS, model_loader.EOS, model_loader.EOP, model_loader.EOT, '\uFFF0', '\uFFF1', '\uFFF2'}
    special_ids = {tokenizer.vocab.get(char) for char in special_chars if char in tokenizer.vocab}
    
    async def token_generator():
        prefix_ids = tokenizer.encode(request.prefix)
        
        for token in model_loader.generate_stream(
            prefix_ids, 
            tokenizer_mapping=tokenizer.id_to_token, 
            max_length=request.max_length or 700
        ):
            if isinstance(token, str):
                yield token
            elif token not in special_ids and token not in special_chars:
                decoded_token = tokenizer.decode([token])
                yield decoded_token
            
            await asyncio.sleep(0.04) 

    return StreamingResponse(token_generator(), media_type="text/plain")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
