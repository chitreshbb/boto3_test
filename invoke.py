from __future__ import print_function
import json
import boto3

client = boto3.client('lambda')

json_params = {
  # 'url': 'http://www.ghtctheatres.com/location/41139/Lewisburg-Cinema-8',
  'url': 'http://cleesmith.github.io/health.html',
  'queue': 'clsq'
  # 'queue': ''
}

# is a param present?
# q_param = json_params.get('queue')
# if q_param is None or len(q_param) <= 0:
#   print('not found!')
# else:
#   print('found')

# (1) invoke a lambda function and expect a response:
# resp = client.invoke(
#   FunctionName='fetch_title',
#   InvocationType='RequestResponse',
#   Payload=json.dumps(json_params)
# )

# (2) invoke a lambda function which then invokes another lambda function:
# resp = client.invoke(
#   FunctionName='lambda_invoker',
#   InvocationType='RequestResponse',
#   Payload='{"ignored":"nothing"}'
# )

# (3) invoke a lambda function asynchronously
#     i.e. no response is returned,
#     instead view the SQS queue to see the results:
for x in range(0, 10):
  resp = client.invoke(
    FunctionName='fetch_title',
    InvocationType='Event',
    Payload=json.dumps(json_params)
  )

print(resp)
print(resp['Payload'].read())
