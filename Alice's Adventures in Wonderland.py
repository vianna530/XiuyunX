# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator

#Save the text contained in the external file in the text variable
text = open('alice.txt').read()

#Import the imread function in the imageio library, and use this function to read the map queen2. jfif as a word cloud shape image
import imageio
mk = imageio.imread("alice_color.png")

#Building Word Cloud Object w
wc = WordCloud(background_color="white", mask=mk,)

#Pass the text string variable into w's generate() method, and input text to the word cloud
wc.generate(text)

#Call the ImageColorGenerator() function in the wordcloud library to extract the color of each part of the template image
image_colors = ImageColorGenerator(mk)

#Display native word cloud map, word cloud map by template image color, and template image by left, middle, and right
fig, axes = plt.subplots(1, 3)
#The leftmost picture shows the cloud picture of native words
axes[0].imshow(wc)
#The image in the middle shows the word cloud image generated according to the color of the template image, and the color is displayed by using the bilinear interpolation method
axes[1].imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
#The picture on the right shows the template picture
axes[2].imshow(mk, cmap=plt.cm.gray)
for ax in axes:
    ax.set_axis_off()
plt.show()

#Re-color the word cloud object according to the color of the template image
wc_color = wc.recolor(color_func=image_colors)
#Export the word cloud picture to the current folder
wc_color.to_file('opforalice.png')
