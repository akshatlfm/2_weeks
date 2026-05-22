import requests
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import ValidationError,BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware



class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
API_KEY = os.getenv("API_KEY")


@app.get("/posts", response_model=List[Post])
def get_posts():
    try:
        url = "https://jsonplaceholder.typicode.com/posts"

        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        validated = [Post(**item) for item in data]
        return validated

    except requests.exceptions.RequestException:
        return {"error": "Network error occurred"}

    except ValidationError:
        return {"error": "Data validation failed"}