import asyncio
import httpx
import os
from dotenv import load_dotenv
from pydantic import BaseModel,ValidationError
from typing import Optional 


load_dotenv()
MAX_STORIES=os.getenv('HN_MAX_STORIES')
if MAX_STORIES is None:
    raise ValueError('SET the key in .env first')
MAX_STORIES=int(MAX_STORIES)


class HNStory(BaseModel):
    id:int
    title:str
    score:int
    by:str
    url:Optional[str]=None
    descendants:Optional[int]=0
    time:int

async def fetch_top_ids(n):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
        return response.json()[:n]
    
async def fetch_story(story_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
        try:
            res=HNStory(**response.json())
        except ValidationError:
            return None
        return res
        


async def main():
    ids = await fetch_top_ids(MAX_STORIES)
    stories= await asyncio.gather(
         *[fetch_story(id) for id in ids]
    )
    for story in stories:
        if story is not None:
            print(story.title,story.score)


asyncio.run(main())

