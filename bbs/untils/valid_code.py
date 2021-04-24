# 方式一
# import random
# r = random.randint(1,254)
# g = random.randint(1,254)
# b = random.randint(1,254)
# from PIL import Image
# img = Image.new('RGB',(270,40),color=(r, g, b))
# with open('validcode.png', 'wb') as f:
#     img.save(f,'png')
# with open('validcode.png', 'rb') as f:
#     data = f.read()

# 方式二（不再用磁盘进行存储图片）
# import random
# r = random.randint(1, 254)
# g = random.randint(1, 254)
# b = random.randint(1, 254)
# from PIL import Image
# # 内存处理
# from io import BytesIO
# img = Image.new('RGB', (270, 40), color=(r, g, b))
# # f为内存句柄
# f = BytesIO()
#
# img.save(f,'png')
# data = f.getvalue()

# 方式3：
import random
import string
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def getRandomColor():
    '''获取一个随机颜色(r,g,b)格式的'''
    c1 = random.randint(0, 255)
    c2 = random.randint(0, 255)
    c3 = random.randint(0, 255)
    return (c1, c2, c3)


def get_code_img(request):
    rand_color = getRandomColor()
    img = Image.new('RGB', (270, 40), color=rand_color)
    draw = ImageDraw.Draw(img)
    kumo_font = ImageFont.truetype('statics/bootstrap/fonts/lhandw.ttf', size=30)
    char_list = random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, 5)
    char_str = ''.join(char_list)
    char = ' '.join(char_list)
    # 在这里面不能随机，所以要调用函数生成随机颜色
    draw.text((60, 5), char, getRandomColor(), font=kumo_font)

    # 噪点噪线
    width = 270
    height = 40
    # for i in range(8):
    #     x1 = random.randint(0,width)
    #     x2 = random.randint(0,width)
    #     y1 = random.randint(0,height)
    #     y2 = random.randint(0,height)
    #     draw.line((x1,y1,x2,y2),fill=getRandomColor())
    #
    # for i in range(100):
    #     draw.point([random.randint(0,width),random.randint(0,height)],fill=getRandomColor())
    #     x = random.randint(0,width)
    #     y = random.randint(0, height)
    #     draw.arc((x,y,x+4,y+4),0,90,fill=getRandomColor())

    # 保存到session
    request.session['code'] = char_str
    # f为内存句柄
    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()
    return data
