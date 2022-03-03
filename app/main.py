from typing import Optional
from pydantic import BaseModel, HttpUrl
import hashlib
import base64

from fastapi import FastAPI

app = FastAPI()


class Request(BaseModel):
    long_url: HttpUrl
    custom_url: str


@app.post("/short_url", status_code=201)
def create_short_url(req: Request):
    hash = hashlib.md5(req.long_url.encode("utf-8"))
    # TODO: trim ==
    return base64.urlsafe_b64encode(hash.digest())


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
