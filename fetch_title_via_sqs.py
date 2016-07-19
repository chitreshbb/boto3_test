from __future__ import print_function
import boto3
import json
import time
import uuid

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

max_urls = 5

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
  response = awslambda.invoke(
    FunctionName='fetch_title',
    InvocationType='Event', # async
    Payload=json.dumps(json_params)
  )
  # commented out the following print's as
  # we don't expect a response since we are async:
  # print('response: ')
  # print(response)
  # print('payload: ')
  # print(response['Payload'].read())
end = time.time()
elapsed = end - invoke_start
print('%d seconds elapsed to invoke %d lambda functions' % (elapsed, max_urls))

msg_start = time.time()
# get all messages/results from the SQS queue:
num_msgs_expected = max_urls
num_msgs_received = 0
# note: we need a count of "expected" messages so we can continue
# to loop until all of those messages are received or some
# amount of time has elapsed and we give up waiting:
while num_msgs_received < num_msgs_expected:
  # we may get 10 or less messages in 10 seconds:
  messages = queue.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=10)
  for message in messages:
    num_msgs_received += 1
    print('id: ' + message.message_id + ':')
    print("\t" + message.body)
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
