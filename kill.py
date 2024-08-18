import os
import time
while True:
	current_time=int(time.time())
	x = os.popen("""ps aux | grep "intercept" | grep -v "grep" | awk '{print $2, $9}' | while read pid start_time; do   epoch_start_time=$(date -d "$(ps -p $pid -o lstart=)" +%s);   echo " $pid, $epoch_start_time"; done""")
	y = x.read()
	print(y)
	data = y.strip('\n')
	info = []
	for i in data.split('\n'):
		info.append(i.replace(' ','').split(','))
		print(i)
	for i in range(len(info)):
		print(i,end='\r')
		try:
			if (current_time-int(info[i][1])) > 600:
				os.system(f"sudo kill {info[i][0]}")
		except:
			pass
#	time.sleep(600)
