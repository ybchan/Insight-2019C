import cv2
import random
import os

# list of movies
mov_list = os.listdir("mov/")
count = 0

# scan through the list of movie
for m in mov_list:
    vidcap = cv2.VideoCapture("mov/" + m)

    # extract frames from movie and save them
    for i in range(20):
        frame = random.randint(1,450)

        vidcap.set(cv2.CAP_PROP_POS_FRAMES,frame)      # just cue to 20 sec. position
        success,image = vidcap.read()
        offset = random.randint(1,200)
        
        fname = "jpg/candy-" + str(count) + ".jpg"
        cv2.imwrite(fname, image[0:720, (0+offset):(960+offset)])
        count+=1    