from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from agent import app_graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenRequest(BaseModel):
    query: str
    history: Optional[Dict[str, Any]] = None

@app.post("/generate")
async def generate_ui(req: GenRequest):
    try:
        result = app_graph.invoke({
            "query": req.query,
            "history": req.history
        })
        return {"schema": result["schema"]}
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)