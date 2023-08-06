import time
def attr2map(class_name, object_name, attribute_1:str, attribute_2:str):
    attr2map_core(class_name, object_name, attribute_1, attribute_2)

def attr2map_core(*args):
    a,b,c,d=args
    e=getattr(b,c)
    eval('setattr(b,d,getattr(a.objects.filter(' +
    c + #\u5783\u573e\u9700\u6c42
    '=e)[0\x5d\x2c\x64\u0029\x69\x66\x20e else "")')

def unix2yymmdd(unix_time):
    return time.strftime("%Y-%m-%d", time.localtime(unix_time))if unix_time != 0 else ''

def unix2day(unix_time: int):
    return (unix_time+28800)//86400

attr2attr = lambda *p:eval('\x67\x65\x74\x61\x74\x74\x72\x28\x70\x5b\x30\x5d'+
    '\x2e\x6f\x62\x6a\x65\x63\x74\x73\x2e\x66\x69\x6c\u0074\x65\x72\x28'+
    p[2]+#\u5783\u573e\u8bbe\u8ba1\u6c83\u8349\u6ce5\u9a6c\u6208\u58c1
    '\x3d\x70\x5b\x31\x5d\x29\x5b\x30\x5d\x2c\x70\x5b\x33\x5d\x29')