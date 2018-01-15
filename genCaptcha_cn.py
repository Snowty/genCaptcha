#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from PIL import ImageDraw,ImageFont
from PIL import Image
import random,os
import math, string

fontdir = "./font"

class RandomChar():
  @staticmethod
  def Unicode():
    val = random.randint(0x4E00, 0x9FBF)
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
                     size = (100, 40),
                     fontPath = './font/微软雅黑.ttf',
                     bgColor = (255, 255, 255),
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
    return (random.randint(0, 255),
           random.randint(0, 255),
           random.randint(0, 255))

  def randPoint(self):
    (width, height) = self.size
    return (random.randint(0, width), random.randint(0, height))

  def randLine(self, num):
    draw = ImageDraw.Draw(self.image)
    for i in range(0, num):
      draw.line([self.randPoint(), self.randPoint()], self.randRGB())
    del draw

  def randChinese(self, num):
    gap = 5
    start = 0
    charStr = ""
    for i in range(0, num):
      char = RandomChar().GB2312()
      x = start + self.fontSize * i + random.randint(0, gap) + gap * i
      self.drawText((x, random.randint(-5, 5)), char , self.randRGB())
      self.rotate()
      charStr += char
    self.randLine(18)
    return charStr

  def save(self, path):
    self.image.save(path)

def getFont(fontdir):   #获取 /font 文件夹下的字体
  fontList = os.listdir(fontdir)
  return fontList

def main():
    fontList = getFont(fontdir)
    for i in range(0,len(fontList)):
      print("Using: "+ fontList[i])
      font = os.path.join(fontdir,fontList[i])
      try:
        ic = ImageChar(fontPath = font)
        imgName = ic.randChinese(4)
        imgpath = os.path.join(imgdir,imgName+".jpg")
        ic.save(imgpath)
      except:
        pass

if __name__=='__main__':
    imgdir = "captcha_cn"
    if not os.path.exists(imgdir):
      os.mkdir(imgdir)
    for i in range(1,3):   # 循环次数
        main()
    print("Done.")