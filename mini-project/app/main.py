from fastapi import FastAPI, HTTPException
from app.schema import PredictRequest, PredictResponse
from app.service import load_latest_model

app = FastAPI(title="NLP Service (TF-IDF + LinearSVC)", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        model = load_latest_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    label = model.predict([req.text])[0]
    proba = None

    try:
        tfidf = model.named_steps["tfidf"]
        clf = model.named_steps["clf"]
        if hasattr(clf, "predict_proba"):
            proba = float(clf.predict_proba(tfidf.transform([req.text]))[0].max())
            # proba = round(proba, 4)
    except Exception:
        pass
    return PredictResponse(label=label, proba=proba)