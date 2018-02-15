from django.http import HttpResponse
import redis

def index(request):
    pool = redis.ConnectionPool(host="redis.devops.pousheng.com", port=6379, password="redis")
    r = redis.Redis(connection_pool=pool)

    try:
        gettimelist = r.time()
        gettime = gettimelist[0]
        svrdic=r.hgetall("prd")
        resp_str = "["
        for key,value in svrdic.items():
            svrname = str(key.decode('utf-8'))
            svroptiondic = eval(str(value.decode('utf-8')))

            resp_str = resp_str + "{"
            # servername
            resp_str = resp_str + "\"svrname\":\""+svrname+"\","

            # cpu
            # if svroptiondic.get("cpu") != None :
            #     resp_str = resp_str + "\"cpu\":" + str(svroptiondic['cpu'])+","

            # sqlserver block
            # if svroptiondic.get("block") != None :
            #     resp_str = resp_str + "\"block\":"+str(svroptiondic['block'])+","

            # sqlserver opentran
            # if svroptiondic.get("opentran") != None :
            #     resp_str = resp_str + "\"opentran\":"+str(svroptiondic['opentran'])+","
                
            # memory
            # if svroptiondic.get("mem") != None :
            #     memdic = eval(str(svroptiondic['mem']))
            #     resp_str = resp_str + "\"mem\":{\"memtotal\":"+str(memdic["memtotal"])+",\"memfree\":"+str(memdic["memfree"])+",},"
            
            # # disks
            # if svroptiondic.get("disks") != None :
            #     resp_str = resp_str + "\"disks\":"+str(svroptiondic['disks'])+","

            # uptime
            diffuptime = None
            if svroptiondic.get("uptime") != None :
                difftime = gettime - svroptiondic['uptime']
                diffuptime = difftime
                if diffuptime >6 :
                    resp_str = resp_str + "\"dt\":"+str(difftime)+","
                else:
                    resp_str = resp_str + "\"dt\":\"\","

            # cpu 2
            if svroptiondic.get("cpu") != None :
                cpu2 = svroptiondic['cpu']
                if diffuptime != None and diffuptime>6:
                    if cpu2 < 50 :
                        resp_str = resp_str + "\"c\":[10," + str(cpu2)+"],"
                    elif cpu2 >=50 and cpu2 < 85 : 
                        resp_str = resp_str + "\"c\":[11," + str(cpu2)+"],"
                    else:
                        resp_str = resp_str + "\"c\":[12," + str(cpu2)+"],"  
                else:
                    if cpu2 < 50 :
                        resp_str = resp_str + "\"c\":[0," + str(cpu2)+"],"
                    elif cpu2 >=50 and cpu2 < 85 : 
                        resp_str = resp_str + "\"c\":[1," + str(cpu2)+"],"
                    else:
                        resp_str = resp_str + "\"c\":[2," + str(cpu2)+"],"

            # sqlserver block 2
            if svroptiondic.get("block") != None :
                block2 = svroptiondic['block']
                if diffuptime != None and diffuptime>6:
                    if block2 == 0 :
                        resp_str = resp_str + "\"b\":[10," + str(block2)+"],"
                    elif block2 > 0 and block2 <= 10 : 
                        resp_str = resp_str + "\"b\":[11," + str(block2)+"],"
                    else:
                        resp_str = resp_str + "\"b\":[12," + str(block2)+"],"
                else:
                    if block2 == 0 :
                        resp_str = resp_str + "\"b\":[0," + str(block2)+"],"
                    elif block2 > 0 and block2 <= 10 : 
                        resp_str = resp_str + "\"b\":[1," + str(block2)+"],"
                    elif block2 == -1 :
                        resp_str = resp_str + "\"b\":[12," + str(block2)+"],"
                    else:
                        resp_str = resp_str + "\"b\":[2," + str(block2)+"],"

            # sqlserver opentran 2
            if svroptiondic.get("opentran") != None :
                opentran2 = svroptiondic['opentran']
                if diffuptime != None and diffuptime>6:
                    if opentran2 == 0 :
                        resp_str = resp_str + "\"o\":[10," + str(opentran2)+"],"
                    elif opentran2 > 0 and opentran2 <= 20 : 
                        resp_str = resp_str + "\"o\":[11," + str(opentran2)+"],"
                    else:
                        resp_str = resp_str + "\"o\":[12," + str(opentran2)+"],"
                else:
                    if opentran2 == 0 :
                        resp_str = resp_str + "\"o\":[0," + str(opentran2)+"],"
                    elif opentran2 > 0 and opentran2 <= 20 : 
                        resp_str = resp_str + "\"o\":[1," + str(opentran2)+"],"
                    elif opentran2 == -1:
                        resp_str = resp_str + "\"o\":[12," + str(opentran2)+"],"
                    else:
                        resp_str = resp_str + "\"o\":[2," + str(opentran2)+"],"

            # memory 2
            if svroptiondic.get("mem") != None :
                memdic2 = eval(str(svroptiondic['mem']))
                memtotal2 = memdic2["memtotal"]
                memfree2 = memdic2["memfree"]
                memfreepercent3 = memfree2 / memtotal2 * 100
                memfreepercent2 = round(memfreepercent3 ,3)
                memfree3 = round(memfree2/1024/1024/1024,3)

                if diffuptime != None and diffuptime>6:
                    if memfreepercent2 > 0.05 or  memfree2 > 5368709120 :
                        resp_str = resp_str + "\"m\":[10,\"" + str(memfreepercent2)+"%/"+str(memfree3)+"GB\"],"
                    elif memfreepercent2 > 0.03 or memfree2 >3221225472 : 
                        resp_str = resp_str + "\"m\":[11,\"" + str(memfreepercent2)+"%/"+str(memfree3)+"GB\"],"
                    else:
                        resp_str = resp_str + "\"m\":[12,\"" + str(memfreepercent2)+"%/"+str(memfree3)+"GB\"],"
                else:
                    if memfreepercent2 > 0.05 or  memfree2 > 5368709120 :
                        resp_str = resp_str + "\"m\":[0,\"" + str(memfreepercent2)+"%/"+str(memfree3)+"GB\"],"
                    elif memfreepercent2 > 0.03 or memfree2 >3221225472 : 
                        resp_str = resp_str + "\"m\":[1,\"" + str(memfreepercent2)+"%/"+str(memfree3)+"GB\"],"
                    else:
                        resp_str = resp_str + "\"m\":[2,\"" + str(memfreepercent2)+"%/"+str(memfree3)+"GB\"],"

            # disks 2
            if svroptiondic.get("disks") != None :
                disks2list = svroptiondic['disks']
                disk2minpercent = 0
                disk2minfree = 0
                disk2red=0
                disk2yellow=0
                diskfor=0
                for disk2obj in disks2list :
                    disk2label = disk2obj['disklabel']
                    disk2diskfree = disk2obj['diskfree']
                    disk3diskfree = round(disk2diskfree/1024/1024/1024,3)
                    disk2freepercent = round(disk2obj['diskfreepercent'],3)

                    if diskfor ==0 :
                        disk2minfree = disk3diskfree
                        disk2minpercent = disk2freepercent
                    else:
                        if disk3diskfree<disk2minfree:
                            disk2minfree = disk3diskfree
                        if disk2freepercent<disk2minpercent:
                            disk2minpercent = disk2freepercent

                    if disk2freepercent<5 and disk2diskfree < 2147483648 :
                        if disk2red == 0:
                            disk2red = 1
                    elif disk2freepercent<15 and disk2diskfree < 5368709120 :
                        if disk2yellow == 0:
                            disk2yellow = 1
                    else :
                        diskfor = diskfor+0
                        
                    diskfor = diskfor +1

                if diffuptime != None and diffuptime>6:
                    if disk2red == 1:
                        resp_str = resp_str + "\"di\":[12,\"" + str(disk2minpercent)+"%/"+str(disk2minfree)+"GB\"],"
                    elif disk2yellow == 1:
                        resp_str = resp_str + "\"di\":[11,\"" + str(disk2minpercent)+"%/"+str(disk2minfree)+"GB\"],"
                    else:
                        resp_str = resp_str + "\"di\":[10,\"" + str(disk2minpercent)+"%/"+str(disk2minfree)+"GB\"],"
                else:
                    if disk2red == 1:
                        resp_str = resp_str + "\"di\":[2,\"" + str(disk2minpercent)+"%/"+str(disk2minfree)+"GB\"],"
                    elif disk2yellow == 1:
                        resp_str = resp_str + "\"di\":[1,\"" + str(disk2minpercent)+"%/"+str(disk2minfree)+"GB\"],"
                    else:
                        resp_str = resp_str + "\"di\":[0,\"" + str(disk2minpercent)+"%/"+str(disk2minfree)+"GB\"],"
                    
                # resp_str = resp_str + "\"di\":"+str(disk2freepercent)+","
                # resp_str = resp_str + "\"disks\":"+str(svroptiondic['disks'])+","

            
            resp_str = resp_str + "},"
        resp_str = resp_str + "]"
    except Exception as err:
        resp_str = "["
        resp_str += "{\"svrname\":\"test01\",\"cpu\":86,\"block\":10,\"opentran\":12,},"
        resp_str += "{\"svrname\":\"test02\",\"cpu\":61,\"block\":10,\"opentran\":12,},"
        resp_str += "{\"svrname\":\"test03\",\"cpu\":20,\"block\":10,\"opentran\":12,},"
        resp_str += "]"

    return HttpResponse(resp_str)
