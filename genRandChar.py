#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from PIL import ImageDraw,ImageFont
from PIL import Image
import random
import math, string
import os,time
import random
import hashlib

fontdir = "./font"
class RandomChar():
    @staticmethod
    def Unicode():
      val = random.randint(0x4E00, 0x9FBF)     ##用来索引unicode常用汉字(编码范围：0x4e00 - 0x9fbf)的拼音首字母
      return unichr(val)

    @staticmethod
    def GB2312():
      head = random.randint(0xB0, 0xCF)
      body = random.randint(0xA, 0xF)
      tail = random.randint(0, 0xF)
      val = ( head << 8 ) | (body << 4) | tail
      str = "%x" % val
      return str.decode('hex').decode('gb2312')

class ImageChar():
    def __init__(self, fontColor = (0, 0, 0),
                     size = (120, 32),
                     fontPath = './font/微软雅黑.ttf',
                     bgColor = (255,255,255),
                     fontSize = 20):
        self.size = size
        self.fontPath = fontPath
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)
        self.image = Image.new('RGB', size, bgColor)

    def rotate(self):
        self.image.rotate(random.randint(0, 30), expand=0)

    def drawText(self, pos, txt, fill):
        draw = ImageDraw.Draw(self.image)
        draw.text(pos, txt, font=self.font, fill=fill)
        del draw

#   def randRGB(self):
#     return (random.randint(0, 255),
#            random.randint(0, 255),
#            random.randint(0, 255))
    def randRGB(self):
        return (random.randint(0, 0),
                random.randint(0, 0),
                random.randint(0, 0))

    def randPoint(self):
        (width, height) = self.size
        return (random.randint(0, width), random.randint(0, height))

    def randLine(self, num):
        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
          draw.line([self.randPoint(), self.randPoint()], self.randRGB())
        del draw

    def randChinese(self, num):
        gap = 0
        start = 0
        charStr = ""
        for i in range(0, num):
            char = RandomChar().GB2312()
            charStr += char
            x = start + self.fontSize * i + random.randint(0, gap) + gap * i
            #self.drawText((x, random.randint(-5, 5)), char, self.randRGB())
            self.drawText((x, random.randint(0, 0)), char, self.randRGB())
            self.rotate()
        return charStr
        #self.randLine(18)

    def save(self, path):
        self.image.save(path)

def getFont(fontdir):   #获取 /font 文件夹下的字体
    fontList = os.listdir(fontdir)
    return fontList


def main():
    basepath = "./Image/newImg"
    fontList = getFont(fontdir)
    for j in range(1,11):
        charNumber = j     #中文字符个数，生成1~10个字符
        picWidth = j * 20    #图片宽度
        basepath = basepath + "_" + str(j)
        if not os.path.exists(basepath):
            os.mkdir(basepath)
        for i in range(0,len(fontList)):
            print("Using: "+ fontList[i])
            font = os.path.join(fontdir,fontList[i])
            #print(font)
            ic = ImageChar(size = (picWidth, 32), fontPath = font ,bgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            now = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
            try:
                charStr = ic.randChinese(charNumber)
                md5name = hashlib.md5(charStr.encode('utf-8')).hexdigest()
                imgName = os.path.join(basepath,md5name+"_"+now+".jpg")
                textName = os.path.join(basepath,md5name+"_"+now+".txt")
                f = open(textName,'w')
                f.write(charStr)
                f.close()
                ic.save(imgName)
                #print(charStr,md5name,imgName)
            except:
                pass
        basepath = basepath.split("_")[0]

if __name__=='__main__':
    img = "./Image"
    if not os.path.exists(img):
        os.mkdir(img)
    for i in range(1,3):   # 循环次数
        main()
    print("Done.")
       
    