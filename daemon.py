import os, time

pid = os.getpid()
f   = open('RUNNING_PID', 'w')
f.write(str(pid))
f.close()

while True :
	os.system('python3 manage.py removetimeout')
	time.sleep(10)

os.remove('RUNNING_PID')
