from typing import Optional
from pydantic import BaseModel, HttpUrl
import hashlib
import base64
import boto3

from fastapi import FastAPI

app = FastAPI()


def put_url(short_url: bytes, created_at: str, long_url: str, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://db:8000")

    table = dynamodb.Table("Url")
    response = table.put_item(Item={"short_url": short_url})
    return response


class Request(BaseModel):
    long_url: HttpUrl
    custom_url: str


@app.post("/short_url", status_code=201)
def create_short_url(req: Request):
    hash = hashlib.md5(req.long_url.encode("utf-8"))
    # TODO: trim ==
    short_url = base64.urlsafe_b64encode(hash.digest())
    response = put_url(short_url, "time", req.long_url)
    return response


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
