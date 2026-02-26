from fastapi import FastAPI

app = FastAPI(title="Action Tracker API")


@app.get("/health")
def health():
    return {"status": "ok"}
