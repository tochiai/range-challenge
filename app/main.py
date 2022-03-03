from pydantic import BaseModel, HttpUrl
import hashlib
import base64
import boto3

from fastapi import FastAPI, Path

app = FastAPI()


def put_url(short_url: bytes, created_at: str, long_url: str, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://db:8000")

    table = dynamodb.Table("Url")
    print(f"put short_url {short_url}")
    response = table.put_item(
        Item={"short_url": short_url, "created_at": created_at, "long_url": long_url}
    )
    return response


def get_url(short_url: bytes, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://db:8000")
    table = dynamodb.Table("Url")
    print(f"get short_url {short_url}")
    response = table.get_item(Key={"short_url": short_url})
    return response


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
    put_url(short_url, "time", req.long_url)
    return PostResponse(
        long_url=req.long_url, custom_url=req.custom_url, short_url=short_url
    )


@app.get("/short_url/{short_url}")
def create_short_url(short_url: str = Path(..., example="x7kg9X5VPfK7aCcvYVcCEA==")):
    short_url = short_url.encode("utf-8")
    item = get_url(short_url)["Item"]
    return {
        "long_url": item["long_url"],
        "created_at": item["created_at"],
        "short_url": item["short_url"],
    }
