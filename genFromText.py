#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from PIL import ImageDraw,ImageFont
from PIL import Image
import random
import math, string
import os,time,re
import random
import hashlib

fontdir = "./font"
class RandomChar():
    @staticmethod
    def Unicode():
      val = random.randint(0x4E00, 0x9FBF)     ##用来索引unicode常用汉字(编码范围：0x4e00 - 0x9fbf)的拼音首字母
      return unichr(val)

    @staticmethod
    def GB2312(x = "好"):
        str = x.encode('gb2312').encode('hex')
        return str.decode('hex').decode('gb2312')

class ImageChar():
    def __init__(self, fontColor = (0, 0, 0),
                     size = (210, 32),
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

    def randChinese(self):
        gap = 5
        start = 0
        text = getText(textdir)
        slice = random.sample(text,1)[0]
        length = len(slice)
        if length > 30:
            slice = re.findall(r'.{30}',slice)[0]   #   切割成10个字
            print("modify:"+slice)
            print(len(slice))
            char = RandomChar().GB2312(slice)
            x = start
            self.drawText((x, random.randint(-5, 5)), char , self.randRGB())
        return char

    def save(self, path):
        self.image.save(path)

def getFont(fontdir):   #获取 /font 文件夹下的字体
    fontList = os.listdir(fontdir)
    return fontList

textdir = "text"
def getText(textdir):
  textList = os.listdir(textdir)
  list = []
  for textfile in textList:
      path = os.path.join(textdir,textfile)
      f = open(path,'r')
      for line in f:
        line = line.strip("\r\n")
        if line:
          for l in line.split():
              list.append(l)  
  return list

def main():
    fontList = getFont(fontdir)
    for i in range(1,len(fontList)):
        print("Using: "+ fontList[i])
        font = os.path.join(fontdir,fontList[i])
        now = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
        try:
            
            ic = ImageChar(fontPath = font ,bgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
           
            charStr = ic.randChinese()
        
            # print charStr
            # print(len(charStr))
            md5name = hashlib.md5(charStr.encode('utf-8')).hexdigest()
            imgName = os.path.join(img,md5name+"_"+now+".jpg")
            textName = os.path.join(img,md5name+"_"+now+".txt")
            f = open(textName,'w')
            f.write(charStr)
            f.close()
            ic.save(imgName)
            #print(charStr,md5name,imgName)
        except Exception as e:
            print e
        

if __name__=='__main__':
    img = "./captcha_fromText"
    if not os.path.exists(img):
        os.mkdir(img)
    for i in range(1,3):   # 循环次数
        main()
    print("Done.")
       
    