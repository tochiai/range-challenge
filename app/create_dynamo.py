import boto3


def create_url_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://db:8000")

    table = dynamodb.create_table(
        TableName="Url",
        KeySchema=[{"AttributeName": "short_url", "KeyType": "HASH"}],  # Partition key
        AttributeDefinitions=[
            {"AttributeName": "short_url", "AttributeType": "B"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )
    return table


if __name__ == "__main__":
    url_table = create_url_table()
    print("Table status:", url_table.table_status)
