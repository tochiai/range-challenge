from pydantic import BaseModel, HttpUrl
import hashlib
import base64
import datetime
from app.dynamo.client import DynamoClient

from fastapi import FastAPI, Path

app = FastAPI()


dynamo = DynamoClient()


class PostRequest(BaseModel):
    long_url: HttpUrl
    custom_url: str | None = None


class PostResponse(BaseModel):
    long_url: HttpUrl
    custom_url: str | None = None
    short_url: str


@app.post("/short_url", status_code=201, response_model_exclude_unset=True)
def create_short_url(req: PostRequest):
    hash = hashlib.md5(req.long_url.encode("utf-8"))
    # TODO: trim ==
    short_url = base64.urlsafe_b64encode(hash.digest())
    dynamo.put_url(short_url, datetime.datetime.now().isoformat(), req.long_url)
    return PostResponse(
        long_url=req.long_url, custom_url=req.custom_url, short_url=short_url
    )


@app.get("/short_url/{short_url}")
def create_short_url(short_url: str = Path(..., example="x7kg9X5VPfK7aCcvYVcCEA==")):
    short_url = short_url.encode("utf-8")
    item = dynamo.get_url(short_url)["Item"]
    return {
        "long_url": item["long_url"],
        "created_at": item["created_at"],
        "short_url": item["short_url"],
    }
