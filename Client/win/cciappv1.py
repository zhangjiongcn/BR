# -*- coding: utf-8 -*-\
import psutil
import socket
import time
import array
import redis

clientname = socket.gethostname()
pool = redis.ConnectionPool(host="redis.devops.pousheng.com", port=6379, password="redis")
r = redis.Redis(connection_pool=pool)

a=0
while a<28 :
    cpupercent = psutil.cpu_percent(0)
    localtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    # mem
    memtotal = psutil.virtual_memory().total
    memfree = psutil.virtual_memory().free

     # disk
    disklist=[]
    disks = psutil.disk_partitions()
    for disk in disks:
        disklabel = disk.mountpoint
        disktype = disk.fstype
        if disktype == 'NTFS' :
            disksize = psutil.disk_usage(disklabel)
            disktotal = disksize.total
            diskfree = disksize.free
            diskfreepercent = 100 - disksize.percent
            diskdic = {"disklabel":disklabel,"disktotal":disktotal,"diskfree":diskfree,"diskfreepercent":diskfreepercent}
            disklist.append(diskdic)

    # dic={"svrtime":localtime,"svrcpu":cpupercent}
    
    try:
        uptimelist = r.time()
        uptime =uptimelist[0]
        dic = {"cpu":cpupercent,"mem":{"memtotal":memtotal,"memfree":memfree},"disks":disklist,"uptime":uptime}
        r.hset("prd",clientname,dic)
    except Exception as err:
        time.sleep(20)
    time.sleep(2)
