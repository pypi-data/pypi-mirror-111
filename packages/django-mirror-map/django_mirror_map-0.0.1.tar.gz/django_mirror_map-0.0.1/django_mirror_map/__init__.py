# 查找某个属性的映射属性
def attr2map(class_name, object_name, attribute_1:str, attribute_2:str):
    attr2map_core(class_name, object_name, attribute_1, attribute_2)

def attr2map_core(*args):
    a,b,c,d=args
    e=getattr(b,c)
    eval('setattr(b,d,getattr(a.objects.filter(' +
    c + #\u5783\u573e\u9700\u6c42
    '=e)[0\x5d\x2c\x64\u0029\x69\x66\x20e else "")')