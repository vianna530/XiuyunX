# -*- coding: utf-8 -*-

# word cloud of the three kingdoms

#Import wordcloud library and define two functions
from wordcloud import (WordCloud, get_single_color_func)

class SimpleGroupedColorFunc(object):

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


class GroupedColorFunc(object):

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)
    
#Import the imread function in the imageio library, and use this function to read the local image as a word cloud shape image
import imageio
mk = imageio.imread("chinamap.png")

w = WordCloud(width=1000, height=700, background_color='white', font_path='msyh.ttc',
              mask=mk, scale=15, max_font_size=60, max_words=20000, font_step=1)

import jieba

#Perform Chinese word segmentation on the text from an external file to get a string
f = open('三国演义.txt',encoding='utf-8')
txt = f.read()
txtlist = jieba.lcut(txt)
string = " ".join(txtlist)

#Pass the string variable into the generate () method of w, and input text to the word cloud
w.generate(string)

#Create a dictionary and arrange different colors according to the different camps of the characters. Green is Shu, orange is Wei, purple is Soochow, and pink is the princes
color_to_words = {
    'green': ['刘备','刘玄德','孔明','诸葛孔明', '玄德', '关公', '玄德曰','孔明曰',
              '张飞', '赵云','后主', '黄忠', '马超', '姜维', '魏延', '孟获',
              '关兴','诸葛亮','云长','孟达','庞统','廖化','马岱'],
    'red': ['曹操', '司马懿', '夏侯', '荀彧', '郭嘉','邓艾','许褚',
            '徐晃','许诸','曹仁','司马昭','庞德','于禁','夏侯渊','曹真','钟会'],
    'purple':['孙权','周瑜','东吴','孙策','吕蒙','陆逊','鲁肃','黄盖','太史慈'],
    'pink':['董卓','袁术','袁绍','吕布','刘璋','刘表','貂蝉']
}

#Color of other words
default_color = 'gray'

#Build a new color rule
grouped_color_func = GroupedColorFunc(color_to_words, default_color)

#Redraw the word cloud color according to the new color rules
w.recolor(color_func=grouped_color_func)

#Export the word cloud picture to the current folder
w.to_file('opforsanguoyanyi.png')