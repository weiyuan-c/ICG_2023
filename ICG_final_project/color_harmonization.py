import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.widgets import RadioButtons
from utils import shiftColor, findOptimalAlpha, hsv2bgr, bgr2hsv

parser = argparse.ArgumentParser()
parser.add_argument('--img_dir', type=str, default='test.png')
# parser.add_argument('--method', type=str, default='Brent', choices=['Brent', 'bounded'])
# parser.add_argument('--graph_cut', action='store_true')
args = parser.parse_args()

img_dir = args.img_dir

harmonicTemplate = {
    'i': [(-9., 9.)],
    'V': [(-46.8, 46.8)],
    'L': [(-9., 9.),   (50.4, 129.6)],
    'I': [(-9., 9.), (171., 189.)],
    'T': [(0., 180.)],
    'Y': [(-46.8, 46.8), (171., 189.)],
    'X': [(-46.8, 46.8), (133.2, 226.8)]
}


def select_template(label):

    global current_template_idx, fig, template_options, img_dir
    current_template_idx = template_options.index(label)
    plt.close(fig)  # close previous fig
    fig = plt.figure(figsize=(10, 5))  # create new fig
    visualize(template_options[current_template_idx], img_dir)

def visualize(render_mode, img_dir):

    global fig, current_template_idx, optimal_setting

    fig.clf() 
    ax_menu = plt.axes([0.63, 0.55, 0.2, 0.35])
    menu = RadioButtons(ax_menu, template_options)
    menu.set_active(current_template_idx)
    menu.on_clicked(select_template)

    img = cv2.imread(img_dir)
    # raw image
    ax_raw = fig.add_subplot(221)
    ax_raw.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax_raw.axis('off')
    ax_raw.set_title('Original image')
    img = bgr2hsv(img)


    # _, OptimalAlpha = findOptimalAlpha(img, template) # optimal angle
    OptimalAlpha = optimal_setting[render_mode]['angle']
    template = optimal_setting[render_mode]['template']
    tfm_img = shiftColor(img, template, OptimalAlpha) # img: hsv image
    tfm_img = hsv2bgr(tfm_img)

    ax1 = fig.add_subplot(223)
    # show the harmonized image first
    ax1.imshow(cv2.cvtColor(tfm_img, cv2.COLOR_BGR2RGB)) # since in openCV, order is BGR, in maplotlib, order is RGB
    ax1.set_title('Harmonized image')
    ax1.axis('off')

    hsv_img = bgr2hsv(tfm_img)
    flatten_img = hsv_img.reshape((-1, 3))
    num_bins = 360

    color_hist = np.histogram(
        a=flatten_img[:, 0],
        bins=num_bins,
        density=True,
        range=(0, 360)
    )

    ax2 = fig.add_subplot(224, projection='polar')
    hsv = colormaps['hsv']

    ax2.set_theta_zero_location('N')
    ax2.set_theta_direction(-1)
    ax2.set_yticklabels('')
    colors = hsv(np.linspace(0, 1, num_bins))
    bars = ax2.bar(x=np.linspace(0, 2*np.pi, num_bins), 
                    height=-color_hist[0], 
                    width= 2*np.pi / num_bins, 
                    color=colors)

    y_max = ax2.get_ylim()[0]
    ax2.set_ylim([y_max, 0])
    ax2.grid(False)

    def on_key_press(event):
        nonlocal OptimalAlpha, template
        # confine angle to [0, 360)
        if event.key == 'up':
            OptimalAlpha = (OptimalAlpha+1) % 360
        elif event.key == 'down':
            OptimalAlpha = (OptimalAlpha-1) % 360
        elif event.key == 'right':
            OptimalAlpha = (OptimalAlpha+10) % 360
        elif event.key == 'left':
            OptimalAlpha = (OptimalAlpha-10) % 360

        transformed_img = shiftColor(img.copy(), template, OptimalAlpha) # img: hsv image
        transformed_img = hsv2bgr(transformed_img)

        ax1.imshow(cv2.cvtColor(transformed_img, cv2.COLOR_BGR2RGB)) # replace current image by transformed image
        ax1.set_title('Harmonized image')
        ax1.axis('off') 

        hsv_img = bgr2hsv(transformed_img)
        flatten_img = hsv_img.reshape((-1, 3))
        num_bins = 360

        color_hist = np.histogram(
            a=flatten_img[:, 0],
            bins=num_bins,
            density=True,
            range=(0, 360)
        )

        ax2 = fig.add_subplot(224, projection='polar')
        hsv = colormaps['hsv']

        ax2.set_theta_zero_location('N')
        ax2.set_theta_direction(-1)
        ax2.set_yticklabels('')
        colors = hsv(np.linspace(0, 1, num_bins))
        bars = ax2.bar(x=np.linspace(0, 2*np.pi, num_bins), 
                    height=-color_hist[0], 
                    width= 2*np.pi / num_bins, 
                    color=colors)

        y_max = ax2.get_ylim()[0]
        ax2.set_ylim([y_max, 0])
        ax2.grid(False)
        plt.draw()
    
    fig.canvas.mpl_connect('key_press_event', on_key_press)
    plt.show()

template_options = ['best', 'i', 'V', 'L', 'I', 'T', 'Y', 'X']
fig = plt.figure(figsize=(10, 5))
current_template_idx = 0

optimal_setting = {}
fmin = np.inf
img = bgr2hsv(cv2.imread(img_dir))
for k, v in harmonicTemplate.items():
    fValue, alpha = findOptimalAlpha(img, harmonicTemplate[k])
    if fValue < fmin:
        fmin = fValue
        template = harmonicTemplate[k]
        mode = k
        optimal_setting['best'] = {'angle':alpha, 'template': v}
    optimal_setting[k] = {'angle':alpha, 'template': v}

tmp_value = optimal_setting['best']
optimal_setting.pop('best')
name = f'best setting: {mode}'
optimal_setting[name] = tmp_value
template_options[0] = name

visualize(name, img_dir)