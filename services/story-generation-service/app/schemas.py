from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    prefix: str = Field(..., description="The seed text to start story generation", example="ایک دفعہ کا")
    max_length: int = Field(default=600, ge=1, le=1000, description="Maximum number of tokens to generate")

class GenerateResponse(BaseModel):
    generated_text: str = Field(..., description="The generated Urdu story")
