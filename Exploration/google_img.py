# download images from google image

from google_images_download import google_images_download
response = google_images_download.googleimagesdownload()

# query items list from google image
search_queries = ['m&ms milk chocolate', 'm&ms peanut', 'skittles',
    'kitkat', 'snicker', 'snicker peanut', 'snicker almond'] 

def downloadimages(query): 
    # keywords is the search query 
    # format is the image file format 
    # limit is the number of images to be downloaded 
    # print urs is to print the image file url 
    # size is the image size which can 
    # be specified manually ("large, medium, icon") 
    # aspect ratio denotes the height width ratio 
    # of images to download. ("tall, square, wide, panoramic") 
    arguments = {"keywords": query, 
                 "format": "jpg", 
                 "limit":200, 
                 "print_urls":False,
                 "thumbnail_only":True 
                } 
    response.download(arguments) 
  
# Driver Code 
for query in search_queries: 
    downloadimages(query)  
    print()  