import boto3

# cache_key: primary key (partition key)
# value and expire: flexible column (attributes)
# if you set sort keys, they'll be required when get_item as attributes
# item == record/row

class CacheUtils:
    def __init__(self, table):
        self.table = table

    def get(self, key: str) -> None:
        response: dict = self.table.get_item(
            Key={
                "cache_key": key,
            }
        )
        print(response['Item'])

    def put(self, key: str, value: str) -> None:
        self.table.put_item(
            Item={
                "cache_key": key,
                "value": value
            }
        )
        item = self.table.get_item(Key={"cache_key": key})
        print(item)

    def delete(self, key):
        self.table.delete_item(
            Key={
                "cache_key": key
            }
        )


# if __name__ == '__main__':
#     dynamo = CacheUtils(boto3.resource('dynamodb').Table('test-dynamo-db'))
#
#     dynamo.get(key="dummykey")
#     dynamo.put(key="dummykey3", value="eeeeeeeeeee")
#     dynamo.delete(key="dummykey2")
    # dynamo.put(key="dummykey2", value="ddddddddd")
    # dynamo.put(key="dummykey3", value="eeeeeeeeeee")
