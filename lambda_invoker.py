from __future__ import print_function
import json
import boto3

def lambda_handler(event, context):
  client = boto3.client('lambda')
  resp = client.invoke(
    FunctionName='fetch_title',
    InvocationType='RequestResponse',
    Payload='{"url":"http://www.ghtctheatres.com/location/41139/Lewisburg-Cinema-8"}'
  )
  print(resp)
  url_title = resp['Payload'].read()
  return url_title

if __name__ == '__main__':
  pt = lambda_handler('event', 'handler')
  print("pt: "+pt)
