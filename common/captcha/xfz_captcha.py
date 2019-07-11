# -*- coding: utf-8 -*-#

"""
Name:           xfz_captcha 
# Author:       wangyunfei
# Date:         2019-05-09
# Description:  
"""


from PIL import Image, ImageDraw, ImageFont
import time
import os
import string
import random


class Captcha(object):

    # 字体位置
    font_path = os.path.join(os.path.dirname(__file__), 'GriffonLight.ttf')
    # 生成验证码的位数
    number = 4
    # 生成验证码的宽带和高度
    size = (100, 40)
    # 背景颜色
    bg_color = (0, 0, 0)
    #随机字体颜色
    random.seed(int(time.time()))
    font_color = (random.randint(200, 255), random.randint(100, 255), random.randint(100, 255))
    # 验证码字体大小
    font_size = 20
    # 随机干扰颜色
    line_color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    # 是否加入干扰线
    draw_line = True
    # 是否加入干扰点
    draw_point = True
    # 加入干扰线的数量
    line_number = 3

    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))


    # 用来生成一个字符串，包括英文和字符串
    #定义成类方法，不能在外部调用
    @classmethod
    def get_text(cls):
        return ''.join(random.sample(cls.SOURCE, cls.number))


    # 用例绘制干扰线
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.line_color)



    #用例绘制干扰点
    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))


    # 生成验证码
    @classmethod
    def gene_code(cls):
        width, height = cls.size
        image = Image.new('RGBA', (width, height), cls.bg_color)
        font = ImageFont.truetype(cls.font_path, cls.font_size)
        draw = ImageDraw.Draw(image)
        text = cls.get_text()
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / 2, (height - font_height) /2), text, font=font, fill=cls.font_color)


        if cls.draw_line:
            for x in range(0, cls.line_number):
                cls.__gene_line(draw, width, height)

        if cls.draw_point:
            cls.__gene_points(draw, 10, width, height)


        return (text, image)


if __name__ == '__main__':

    x ,y = Captcha.gene_code()






