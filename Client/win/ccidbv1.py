# -*- coding: utf-8 -*-\
import psutil
import socket
import time
import datetime
import array
import redis
import pyodbc


sqlstr01 = "SELECT isnull(datediff(ss,min(dtd.database_transaction_begin_time),getdate()),0) as opentransec FROM sys.dm_tran_database_transactions dtd with(nolock) ,sys.dm_tran_session_transactions dts with(nolock) where dtd.transaction_id = dts.transaction_id and ( (database_transaction_state = 4 and is_user_transaction =1)  or (database_transaction_state = 3 and is_user_transaction =0) )"
sqlstr02 = "SELECT count(9) as counts from sys.sysprocesses with(nolock) where blocked>0"
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=master;')
cursor = conn.cursor()

clientname = socket.gethostname()
pool = redis.ConnectionPool(host="redis.devops.pousheng.com", port=6379, password="redis")
r = redis.Redis(connection_pool=pool)

a=0
while a<28 :
    cpupercent = psutil.cpu_percent(0)
    localtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
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
    
    try:
        cursor.execute( sqlstr01 )
        rows01 = cursor.fetchall()
        cursor.execute( sqlstr02 )
        rows02 = cursor.fetchall()

        for row01 in rows01:
            opentrantime = row01.opentransec
        
        for row02 in rows02:
            blocktime = row02.counts
            
    except Exception as err:
        opentrantime = -1
        blocktime = -1


    try:
        uptimelist = r.time()
        uptime =uptimelist[0]
        dic = {"cpu":cpupercent,"block":blocktime,"opentran":opentrantime,"mem":{"memtotal":memtotal,"memfree":memfree},"disks":disklist,"uptime":uptime}
        r.hset("prd",clientname,dic)
    except Exception as err:
        time.sleep(20)
    time.sleep(2)
