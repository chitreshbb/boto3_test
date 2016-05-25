from __future__ import print_function
import json
import boto3

client = boto3.client('lambda')
# resp = client.invoke(
#   FunctionName='fetch_title',
#   InvocationType='RequestResponse',
#   Payload='{"url":"http://www.ghtctheatres.com/location/41139/Lewisburg-Cinema-8"}'
# )
resp = client.invoke(
  FunctionName='lambda_invoker',
  InvocationType='RequestResponse',
  Payload='{"ignored":"nothing"}'
)
print(resp)
print(resp['Payload'].read())
