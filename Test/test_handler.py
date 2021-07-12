import boto3
import pytest
from moto import mock_dynamodb2
from Test import getcount_test

#Example API Gateway proxy event
test_api_event = {
    "Records": [{
        "resource": "/",
        "path": "/",
        "httpMethod": "GET",
        "requestContext": {
            "resourcePath": "/",
            "httpMethod": "GET",
            "path": "/Prod/",

            },
        "headers": {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "Host": "70ixmpl4fl.execute-api.us-east-2.amazonaws.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "X-Amzn-Trace-Id": "Root=1-5e66d96f-7491f09xmpl79d18acf3d050",

        },
        "multiValueHeaders": {
            "accept": [
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            ],
            "accept-encoding": [
                "gzip, deflate, br"
            ],

        },
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "body": None,
        "isBase64Encoded": False
    }]
}

#Create fake DynamoDB table
@mock_dynamodb2
def test_lambda_handler():
    dynamodb = boto3.resource('dynamodb', 'us-west-1')
    table_name = 'ViewCounts'
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'Page', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'Page', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    table.put_item(
        Item={
            'Page': 'cloudresumechallenge.andrewjpak.com',
            'ViewCount': 0,
        }
    )

    response = getcount_test.lambda_handler(event=test_api_event, context="")

    assert response["statusCode"] == 200
    assert "body" in response
    assert response["body"]
    assert int(response["body"])
    assert int(response["body"]) > 0



