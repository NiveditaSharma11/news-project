from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

app = FastAPI()

# Allow CORS (adjust origins if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Hugging Face summarizer model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/summary")
async def generate_summary(request: Request):
    try:
        payload = await request.json()
        text = payload.get("text", "")
        tone = payload.get("tone", "neutral")  # Optional use

        if not text:
            raise HTTPException(status_code=400, detail="Text input is required.")

        # Generate summary
        summary = summarizer(
            text,
            max_length=200,  # you can increase this if needed
            min_length=50,
            do_sample=False
        )[0]["summary_text"]

        return {"summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

# ✅ Updated bias route with confidence
@app.post("/bias")
async def check_bias(request: Request):
    try:
        payload = await request.json()
        text = payload.get("text", "")

        if not text:
            raise HTTPException(status_code=400, detail="Text input is required.")

        lower_text = text.lower()

        if any(word in lower_text for word in ["corrupt", "wasting", "failure", "chaos"]):
            bias = "Negative"
            confidence = 0.87
        elif any(word in lower_text for word in ["innovation", "progress", "growth"]):
            bias = "Positive"
            confidence = 0.82
        else:
            bias = "Neutral"
            confidence = 0.70

        return {
            "bias": bias,
            "confidence": round(confidence * 100, 2)  # Return percentage
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking bias: {str(e)}")
