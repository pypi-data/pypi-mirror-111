import time
def unix2yymmdd(unix_time):
    return time.strftime("%Y-%m-%d", time.localtime(unix_time))if unix_time != 0 else ''

def unix2day(unix_time: int):
    return (unix_time+28800)//86400

# 0:Class, 1:object, 2:input, 3:out
# or 
# 0:Class, 1:value, 2:input, 3:out

useattr = lambda *p:eval('setattr(p[1],p[3],getattr(p[0].objects.filter('+
p[2]+'=getattr(p[1],p[2])).first(),p[3])if getattr(p[1],p[2]) else "")') if eval('type(type(p[1]))==models.base.ModelBase') else eval('getattr(p[0].objects.filter('+
p[2]+'=p[1]).first(),p[3])')