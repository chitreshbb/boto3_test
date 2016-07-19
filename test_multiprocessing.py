import urllib2
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool

print("cores=%d" % multiprocessing.cpu_count()) # detect number of cores

urls = [
  'http://www.python.org',
  'http://www.python.org/about/',
  'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
  'http://www.python.org/doc/',
  'http://www.python.org/download/',
  'http://www.python.org/getit/',
  'http://www.python.org/community/',
  'https://wiki.python.org/moin/',
  ]

pool = ThreadPool(4)
# open the urls in their own threads and return the results
results = pool.map(urllib2.urlopen, urls)
# close the pool and wait for the work to finish
pool.close()
pool.join()
print(results)
for result in results:
  print(".............................. start ............................................")
  print(result.read())
  print("______________________________ end ____________________________________________\n")
