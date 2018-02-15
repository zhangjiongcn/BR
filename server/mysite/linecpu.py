from django.http import HttpResponse
import redis

def index(request):
    pool = redis.ConnectionPool(host="redis.devops.pousheng.com", port=6379, password="redis")
    r = redis.Redis(connection_pool=pool)

    try:
        resp_str = 0
        gettimelist = r.time()
        gettime = gettimelist[0]

        svroption = r.hget("prd","WMS-EDI01")

        svroptiondic = eval(str(svroption.decode('utf-8')))

        difftime = gettime - svroptiondic['uptime']

        if difftime>6:
            cpu2 = -1
        else:
            cpu2 = round(svroptiondic['cpu'])

        resp_str = cpu2
    except Exception as err:
        resp_str = -2

    return HttpResponse(resp_str)
