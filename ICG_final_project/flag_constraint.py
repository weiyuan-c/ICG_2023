import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.widgets import RadioButtons
from utils import bgr2hsv, hsv2rgb, SimpleShift

parser = argparse.ArgumentParser()
parser.add_argument('--source_img', type=str, default='Brazil.png')
parser.add_argument('--target_img', type=str, default='billboard.png')
args = parser.parse_args()

harmonicTemplate = {
    'i': [(-9., 9.)],
    'V': [(-46.8, 46.8)],
    'L': [(-9., 9.),   (50.4, 129.6)],
    'I': [(-9., 9.), (171., 189.)],
    'T': [(0., 180.)],
    'Y': [(-46.8, 46.8), (171., 189.)],
    'X': [(-46.8, 46.8), (133.2, 226.8)]
}

template_options = ['best', 'i', 'V', 'L', 'I', 'T', 'Y', 'X']
current_template_option = 0

# img = cv2.imread('Ukraine.png')
img = cv2.imread(args.source_img)

fig = plt.figure(figsize=(10, 5))

# raw image
ax1 = fig.add_subplot(131)
ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
ax1.axis('off')
ax1.set_title('Flag')

hsv_img = bgr2hsv(img)
flatten_img = hsv_img.reshape((-1, 3))
num_bins = 360

color_hist = np.histogram(
    a=flatten_img[:, 0],
    bins=num_bins,
    density=True,
    range=(0, 360)
)

sorted_indices = np.argsort(-color_hist[0])  
early_stop = 0
idx = 0
centers =[]
while color_hist[0][sorted_indices[idx]].item() > 0.08: 
    centers.append(color_hist[1][sorted_indices[idx]].item())
    idx += 1

target = cv2.imread(args.target_img)
ax2 = fig.add_subplot(132)
ax2.imshow(cv2.cvtColor(target, cv2.COLOR_BGR2RGB))
ax2.axis('off')
ax2.set_title('Original image')

tfm_img = SimpleShift(bgr2hsv(target), centers)
tfm_img = hsv2rgb(tfm_img)

ax3 = fig.add_subplot(133)
ax3.axis('off')
plt.imshow(tfm_img)

plt.show()