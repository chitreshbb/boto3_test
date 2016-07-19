import threading
import time
from datetime import datetime

def aworker(num):
  # here we call awslambda.invoke() a function and ignore the response
  print(" worker %s started: %s" % (num, datetime.now().time()))
  time.sleep(1)
  print(" worker %s finished\n" % num)

max_workers = 3
print('without threading:')
start = time.time()
for i in range(0, max_workers):
  aworker(i)
end = time.time()
elapsed = end - start
print('%d seconds elapsed to invoke %d workers' % (elapsed, max_workers))

print("\nwith threading:")
start = time.time()
for i in range(0, max_workers):
  threading.Thread(target=aworker, args=(i,)).start()
end = time.time()
elapsed = end - start
print('%d seconds elapsed to invoke %d workers' % (elapsed, max_workers))

# here we get all messages/results from the SQS queue
print('do other stuff while waiting on workers...')
