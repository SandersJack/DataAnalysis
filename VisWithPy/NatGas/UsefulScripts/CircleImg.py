import numpy as np 
from PIL import Image, ImageDraw
import pandas as pd 

country_codes = pd.read_csv("codes.csv")

#print(country_codes)

# import required module
import os
# assign directory
directory = '../assets/imgs/Flags/'
 
# iterate over files in
# that directory
files = []

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        files.append(f)
        
for i in range(len(files)):

    country_2code = files[i][-6:-4].upper()
    #print(country_2code)

    country_name = list(country_codes.loc[country_codes['alpha-2'] == country_2code]['name'])
    print(country_name)
    
    if country_name == []:
        continue


    # Open the input image as numpy array, convert to RGB
    img=Image.open(files[i]).convert("RGB")
    npImage=np.array(img)
    h,w=img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    # Add alpha layer to RGB
    npImage=np.dstack((npImage,npAlpha))

    # Save with alpha
    Image.fromarray(npImage).save('../assets/imgs/flagicons_py/{}.png'.format(country_name[0]))