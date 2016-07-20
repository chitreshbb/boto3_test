from __future__ import print_function
import boto3
import json
import threading
import time
import uuid

def lambda_invoker(json_params):
  response = awslambda.invoke(
    FunctionName='fetch_title',
    InvocationType='Event', # async
    Payload=json.dumps(json_params)
  )
  if response['StatusCode'] == 202:
    pass
  else:
    print('****************** ERROR *****************************')
    print('StatusCode: ')
    print(response['StatusCode'])
    print('response: ')
    print(response)
    print('****************** ERROR *****************************')

all_start = time.time()

# create AWS SQS queue:
sqs_client = boto3.client('sqs')
sqs_resource = boto3.resource('sqs')
# create an SQS.Queue instance with a random uuid name:
q = 'queue-' + str(uuid.uuid4())
queue = sqs_resource.create_queue(QueueName=q)
print("SQS queue uuid name:")
print(q)
print("queue.url:")
print(queue.url)

max_urls = 100

# jul 19, 2016: this caused some invocations to be throttled but they all succeeded:
# max_urls = 500
# viewing/sorting the goweb server log file showed access from 4 amazon IP's:
#   54.174.37.171
#   54.208.199.58
#   54.210.195.127
#   54.237.249.41
# which indicates that the aws lambda service "scaled/started"
# up 4 instances(probably containers) for our lambda function
# fetch_title.py ... cool!

# invoke AWS Lambda function asynchronously (an event):
awslambda = boto3.client('lambda')

json_params = {
  'url': 'http://162.243.160.249/',
  'queue': q
}

invoke_start = time.time()

# invoke the lambda function asynchronously
# i.e. no response is returned as we will
# retrieve the results from a SQS queue:
for x in range(0, max_urls):
  threading.Thread(target=lambda_invoker, args=(json_params,)).start()

end = time.time()
elapsed = end - invoke_start
print('%d seconds elapsed to invoke %d lambda functions' % (elapsed, max_urls))

msg_start = time.time()
# get all messages/results from the SQS queue:
max_polls = 3
num_msgs_expected = max_urls
num_msgs_received = 0
# note: we need a count of "expected" messages so we can continue
# to loop until all of those messages are received or some
# amount of time has elapsed and we give up waiting:
while (num_msgs_received < num_msgs_expected) and (max_polls > 0):
  # we may get 10 or less messages in 10 seconds:
  # print('polling for 10 seconds...')
  messages = queue.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=10)
  num_msgs = len(messages)
  # print('polling ended: %d messages received' % num_msgs)
  # give up after 3 long polls of 10 seconds, i.e. only wait 30 seconds total
  if num_msgs <= 0: max_polls -= 1
  for message in messages:
    num_msgs_received += 1
    # print('id: ' + message.message_id + ':')
    # print("\t" + message.body)
    # acknowledge message was processed and delete it from the queue
    message.delete()
print('total messages received: '+str(num_msgs_received))
end = time.time()
elapsed = end - msg_start
print('%d seconds elapsed to received %d messages' % (elapsed, num_msgs_received))

# we're all done, so delete the queue:
print('delete SQS queue: %s' % queue.url)
response = sqs_client.delete_queue(QueueUrl=queue.url)
print('delete SQS queue response: ')
print(response)

end = time.time()
elapsed = end - all_start
print('%d seconds elapsed to process %d lambda functions' % (elapsed, max_urls))
