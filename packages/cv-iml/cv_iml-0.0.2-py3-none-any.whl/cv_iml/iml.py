# //  Created by Qazi Ammar Arshad on 21/10/2019.
# //  Copyright © 2020 Qazi Ammar Arshad. All rights reserved.

import cv2
import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score, plot_confusion_matrix
from sklearn.metrics import confusion_matrix, multilabel_confusion_matrix, roc_auc_score
from sklearn import metrics
import matplotlib.pyplot as plt

def sayhello():
    print("hello world!")


def image_show(img, cmap=None, suptitle=""):
    """
    Version = 1.1
    This is a stable function.
    This function take an image and how it by using matplot function.
    :param map: 'Reds', 'Greens', 'Blues'
    :param img: img to display.
    :return: None
    """
    fig = plt.figure()
    fig.suptitle(suptitle, fontsize=14, fontweight='bold')

    if cmap is not None:
        plt.imshow(img, cmap=cmap, vmin=0, vmax=255)
    else:
        plt.imshow(img)
    plt.show()


def show_train_images(train_data, train_labels):
    """
    This function show 16 random images form train data.
    :param train_data:
    :return: None
    """
    plt.figure(1, figsize=(8, 8))
    n = 0

    for i in range(16):
        n += 1
        # each time random images are loaded
        # r = np.random.randint(0, train_data.shape[0], 1)
        plt.subplot(4, 4, n)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        plt.imshow(train_data[i] / 255.)
        plt.title('{}'.format(train_labels[i]))
        plt.xticks([]), plt.yticks([])
    plt.show()


def show_histogram(img, title=None):
    """
    version: 1.1
    This is a stable function.
    This function shows the histogram of image. It first check if image is gray scale or rgb and then
    plot histogram according to it
    :param img: input image of which histogram is need to plot
    :param title: title of plot
    :return: None
    """
    if len(img.shape) < 3:
        histr = cv2.calcHist([img], [0], None, [256], [0, 256])

        plt.plot(histr, 'black', label='gray')
        plt.title("Grayscale Image Histogram")
    elif len(img.shape) == 3:
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histr = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(histr, color=col, label=col)
            plt.xlim([0, 256])
            plt.title("RGB Image Histogram")
    plt.legend()
    if title is not None:
        plt.title(title)
    plt.show()


def apply_sharpening_on(image):
    """
    Version = 1.0
    This is a stable function.
    Apply sharpening kernel on image.
    :param image:
    :return:
    """
    # Create kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])

    # Sharpen image
    sharp_image = cv2.filter2D(image, -1, kernel)
    return sharp_image


def show_multiple_image_with(row=1, col=1, images=[], titles=[]):
    """
    Version = 1.0
    This not stable function.
    We want to show multiple images side by side using this function.
    :param row:
    :param col:
    :param images:
    :param titles:
    :return:
    """
    fig, ax = plt.subplots(row, col, figsize=(10, 10), sharex=True, sharey=True)
    image_counter = 0
    for i in range(row):
        for j in range(col):
            ax[i, j].imshow(images[image_counter])
            ax[i, j].set_title(titles[image_counter])

    for a in ax.ravel():
        a.set_axis_off()

    plt.tight_layout()
    plt.show()


def removeBlackRegion(img):
    """
    This is a stable function.
    This function remove the black region form image by cropping the largest contours form the image.
    use this function to remove the black region in microscope images, that may cause problems.
    Version = 1.0
    # Link: ?
       :param img: input image
       :return: image with removed black region but not removed black regions completely we need to apply some
       thresholding to rows and col to completely remove the black region.
       """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    # Find all contours form the gray image.
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_area = -1
    best_cnt = None

    # Find contours with largest area.
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    # Get coordinate of largest contours
    x, y, w, h = cv2.boundingRect(best_cnt)

    # Crop original with coordinate of largest contour.
    crop = img[y:y + h, x:x + w]
    return crop


def get_image_patches_by_sliding_window(img, stepSize, window_size, overlapping):
    """
    -> This is not stable function.
    -> Need to through exception when overlapping is 100%
    -> This function take a full image and make patches of that image save them into array and
        return that array.
        # Link: ?
    Version = 1.0
    :param img: full image form where you want to get patches.
    :param stepSize:
    :param window_size:
    :param overlapping: how much overlapping you need in you images.
    :return: array of images extracted by sliding window.
    """
    # read the image and define the stepSize and window size
    # (width,height)
    if overlapping == 100:
        return None
    # generation step size for overlapping
    overlapping = 100 - overlapping
    stepSize = int(stepSize * (overlapping / 100))

    patches = []
    image = img  # your image path
    tmp = image  # for drawing a rectangle
    (w_width, w_height) = (window_size, window_size)  # window size
    for x in range(0, image.shape[1] - w_width, stepSize):
        for y in range(0, image.shape[0] - w_height, stepSize):
            window = image[x:x + w_width, y:y + w_height, :]
            # add the window into your patches array.
            patches.append(window)

    return patches


# demonstration of calculating metrics for a neural network model using sklearn

def get_f1_score(actual_labels, preds_labels, binary_classifcation, pos_label="malaria", confusion_matrix_title=""):
    """
    Calculate the F1 score of CNN prediction.
    This method works for both binary class and multiclass. For binary class you have to
    mention pos_label and for multiclass pass pos_label =1
    # Link: ?
    Version = 1.1
    :param actual_labels: labels of testing images. Y_label
    :param preds_labels: predicted labels by trained CNN
    :param pos_label: The positive label for calculating the precision and recall. For
    the multiclass problem this label is set to 1.
    :return: this function return confusion matrix.
    """
    # demonstration of calculating metrics for a neural network model using sklearn
    if not binary_classifcation:
        # For multiclass classification.
        accuracy = accuracy_score(actual_labels, preds_labels)
        precision = precision_score(actual_labels, preds_labels, average="macro")
        recall = recall_score(actual_labels, preds_labels, average="macro")
        f1 = f1_score(actual_labels, preds_labels, average="macro")
        print('Accuracy: %f' % accuracy)
        print('Precision: %f' % precision)
        print('Recall: %f' % recall)
        print('F1 score: %f' % f1)

    else:
        accuracy = accuracy_score(actual_labels, preds_labels)
        print('Accuracy: %f' % accuracy)
        # # precision tp / (tp + fp)
        precision = precision_score(actual_labels, preds_labels, pos_label=pos_label)
        print('Precision: %f' % precision)
        # recall: tp / (tp + fn)
        recall = recall_score(actual_labels, preds_labels, pos_label=pos_label)
        print('Recall: %f' % recall)
        # f1: 2 tp / (2 tp + fp + fn)
        f1 = f1_score(actual_labels, preds_labels, pos_label=pos_label)
        print('F1 score: %f' % f1)
    # ROC AUC
    # auc = roc_auc_score(test_labels, basic_cnn_preds_labels)
    # print('ROC AUC: %f' % auc)

    # confusion matrix
    disp = plot_confusion_matrix(y_true=actual_labels, y_pred=preds_labels,
                                 display_labels=list(np.unique(actual_labels)),
                                 cmap=plt.cm.Blues,
                                 normalize=None)
    disp.ax_.set_title(confusion_matrix_title)
    plt.show()
    matrix = confusion_matrix(actual_labels, preds_labels)
    print(matrix)
    # if plot_confusion_matrix:
    #     show_confusion_matrix(matrix=matrix, labels=list(np.unique(actual_labels)))


def show_confusion_matrix(matrix, labels: None) -> object:
    """
    This function plot the confusion matrix on plt show().
    Version = 1.1
    :param matrix: matrix which we have to show
    :param labels: labels of classes
    :return: None
    """
    cm = matrix
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(cm)
    plt.title('Confusion matrix of the Segmented Malaria')
    fig.colorbar(cax)
    if labels is not None:
        ax.set_xticklabels([''] + labels)
        ax.set_yticklabels([''] + labels)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()


def ROC_curve_binary(actual_labels, basic_cnn_pred_score, pos_label="malaria"):
    """
     Plot  the the ROC curve for binary classification
     This method works for only binary class

    :param actual_labels: ground truth labels
    :param basic_cnn_pred_score: score generated by CNN
    :return: None
    """
    fpr, tpr, thresholds = metrics.roc_curve(actual_labels, basic_cnn_pred_score, pos_label=pos_label)

    roc_auc = auc(fpr, tpr)

    plt.figure()
    lw = 2
    # colors = ['aqua', 'darkorange', 'cornflowerblue', 'navy', 'deeppink', 'aqua', 'darkorange', 'cornflowerblue']
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.4f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()


# color_constancy cv_iml Start.
# Version 1.0
# This is a simple color balancing algorithm that balance color in the image.
# Link: https://gist.github.com/DavidYKay/9dad6c4ab0d8d7dbf3dc

def apply_mask(matrix, mask, fill_value):
    masked = np.ma.array(matrix, mask=mask, fill_value=fill_value)
    return masked.filled()


def apply_threshold(matrix, low_value, high_value):
    low_mask = matrix < low_value
    matrix = apply_mask(matrix, low_mask, low_value)

    high_mask = matrix > high_value
    matrix = apply_mask(matrix, high_mask, high_value)

    return matrix


def color_constancy(img, percent=1):
    """

    :param img:
    :param percent:
    :return: return image with consistent colors.
    """
    out_channels = []
    cumstops = (
        img.shape[0] * img.shape[1] * percent / 200.0,
        img.shape[0] * img.shape[1] * (1 - percent / 200.0)
    )
    for channel in cv2.split(img):
        cumhist = np.cumsum(cv2.calcHist([channel], [0], None, [256], (0, 256)))
        low_cut, high_cut = np.searchsorted(cumhist, cumstops)
        lut = np.concatenate((
            np.zeros(low_cut),
            np.around(np.linspace(0, 255, high_cut - low_cut + 1)),
            255 * np.ones(255 - high_cut)
        ))
        out_channels.append(cv2.LUT(channel, lut.astype('uint8')))
    return cv2.merge(out_channels)


# color_constancy cv_iml End.

def hist_of_label_count(dataList):
    """
    This function take the list of input data and plot the histogram of count for each unique
    label in dataList
    :param dataList: list for ploting data
    :return: NONE
    """
    # theses import are only required for this function
    import pandas
    from collections import Counter
    # end section of import
    counts = Counter(dataList)
    df = pandas.DataFrame.from_dict(counts, orient='index')
    df.plot(kind='bar')
    plt.show()
