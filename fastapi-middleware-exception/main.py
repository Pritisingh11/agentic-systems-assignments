from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "Hello, Welcome to FastAPI!"}

@app.middleware("http")
async def log_request(request: Request, call_next):
    print("Before processing request:", request.url)
    response = await call_next(Request)
    print("After processing request:", request.url)
    return response

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "The requested resource was not found"},
    )