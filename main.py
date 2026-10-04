from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
# Create FastAPI app instance
app = FastAPI()

# Define a simple GET endpoint
# @app.get("/")
# def read_root():
#     return {"message": "Hello from fastAPI"}


# @app.post("/greet")
# def greet_user(name: str):
#     return {"message": f"welcome {name}"}

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def homepage():
    with open("static/index.html", "r") as f:
        return f.read()
