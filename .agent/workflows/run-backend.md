---
description: How to run the backend story generation service
---

1. Navigate to the backend directory:
```bash
cd services/story-generation-service
```

2. (Optional) Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Run the FastAPI server:
// turbo
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The health check will be available at `http://localhost:8000/health`.
