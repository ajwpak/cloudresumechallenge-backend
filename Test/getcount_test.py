import json, boto3, os


# TABLE_NAME env variable defined in SAM template, set to ViewCounts here for the pytest


def lambda_handler(event, context):
    TABLE_NAME = 'ViewCounts'
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    response = table.update_item(
        Key={
            'Page': 'cloudresumechallenge.andrewjpak.com'
        },
        UpdateExpression='SET ViewCount = if_not_exists(ViewCount, :val0) + :val1',
        ExpressionAttributeValues={
            ':val0': 0,
            ':val1': 1
        },
        ReturnValues="UPDATED_NEW"
    )

    retrieved_viewcount = json.dumps(int(response["Attributes"]["ViewCount"]))

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Methods': 'GET'
        },
        'body': retrieved_viewcount
    }
