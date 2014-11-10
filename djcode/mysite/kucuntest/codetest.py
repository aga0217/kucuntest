# -*- coding: utf-8 -*-
import re
from models import GongyingshangGL
"""#判断只有中文
#re_p = ur"[\u4e00-\u9fa5]*$"
#p = "侯利鹏"

#print re.match(re_p , p.decode('utf-8'))

#判断只有中文和字母和数字

re_p = ur"[\w\u4E00-\u9FA5\uF900-\uFA2D]*$"
p = "侯利@鹏"

#print re.match(re_p , p.decode('utf-8'))

#判断只有数字不能有空格
#re_p = ur"[0-9]*$"
#p = "1234568"

print re.match(re_p , p.decode('utf-8'))
"""""

gongyingshanglist = GongyingshangGL.objects.all()



