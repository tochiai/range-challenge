import boto3


class DynamoClient:
    def __init__(self):
        self.resource = dynamodb = boto3.resource(
            "dynamodb", endpoint_url="http://db:8000"
        )

    def put_url(self, short_url: bytes, created_at: str, long_url: str):
        table = self.resource.Table("Url")
        response = table.put_item(
            Item={
                "short_url": short_url,
                "created_at": created_at,
                "long_url": long_url,
            }
        )
        return response

    def get_url(self, short_url: bytes):
        table = self.resource.Table("Url")
        response = table.get_item(Key={"short_url": short_url})
        return response
