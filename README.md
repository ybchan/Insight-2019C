# Insight-2019C.HD
## Sugar Fairy - a candy allergen detector
### Author: Bun Chan

## Background
In US, food allergy is a serious problem. Over 5 million children have food allergy and the number of cases increase year by year. Among different food items, candy is the most problematic one. It is especially true for Halloween candy where ingredient list is quite often missing on individual package. To solve this issue, I develop a web app that uses computer vision to identify candy and warns users for any potential food allergens.

## Vision 
**Sugar Fairy** - a web app that allows users to take candy images using computer camera. Then users can drag the images to a drop box in the app. Program can identify the brand and type of candy and warn users for any potential food allergens.  
[Sugar Fairy](http://insightproject.me)  
[Youtube Demo](https://www.youtube.com/watch?v=TNoblZZ64sk)

## Technical Backend
Images of 10 different types of Halloween Candy (i.e. Kitkat, M&Ms (chocolate, peanut, peanut butter), Snicker (original, peanut, almond), Heath, Whooper, Reese. There are about 200 images for each type of candy. Image data are augmented including rotation, zooming, shifting, shearing and brightness adjustment to generate the training dataset. Next, I test 2 modern convolutional neural networks, InceptionV3 and ResNet50, to see which one performs better. Several hyperparameter such as learning rate, epoches, layers are explored at the exploration stage. The final version achieve over 99% accuracy is presented here.  
**Sugar_Fairy.ipynb** - jupyter notebook of final training model  
**app.py** - dash app  

### Exploration directory  
**Exploration.ipynb** - jupyter notebook of exploration stage  
**get_frame.py** - python script to obtain random frame from video to generate image data  
**google_img.py** -  python script to grap image from google image
