import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
from scipy.ndimage import binary_opening,binary_closing
import cv2
im=cv2.imread('ign25-1.png');hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
h=hsv[...,0].astype(int)*2;s=hsv[...,1].astype(int);v=hsv[...,2].astype(int)
sea=(h>=180)&(h<=215)&(s>=18)&(v>150)
sea=binary_closing(sea,iterations=4);sea=binary_opening(sea,iterations=5)
np.save('ign25_sea.npy',sea)
Image.fromarray((sea*255).astype(np.uint8)).resize((sea.shape[1]//6,sea.shape[0]//6)).save('sea25.png')
