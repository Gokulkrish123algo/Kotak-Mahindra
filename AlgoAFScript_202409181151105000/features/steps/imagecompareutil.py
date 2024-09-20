# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=no-member
# pylint: disable=line-too-long
import os
import time
import cv2
import numpy as np
from numpy import diff
from pixelmatch.contrib.PIL import pixelmatch
from PIL import Image
import common


def save_image(context, imagename, compareimage):
    directory = '%s/' % os.getcwd()
    # print(directory)
    common.delete_files(directory + '/steps/images/temp')
    tempimage = '/steps/images/temp/' + imagename + '.png'
    context.driver.save_screenshot(directory + tempimage)
    file_name = ''
    try:
        if eval(compareimage):
            file_name = '/steps/images/compare/' + imagename + '.png'
            common.rename_file(directory + '/steps/images/compare', imagename)
        else:
            file_name = '/steps/images/baseline/' + imagename + '.png'
            common.rename_file(directory + '/steps/images/baseline', imagename)
    except:
        pass
    img = cv2.imread(directory + tempimage)
    height, width, channels = img.shape
    crop_img = img[200:(height - 100), 0:width]
    cv2.imwrite(directory + file_name, crop_img)


def crop_image(context):
    directory = '%s/' % os.getcwd()
    file_name = '/steps/images/compare/screenshot.png'
    img = cv2.imread(directory + file_name)
    height, width, channels = img.shape
    crop_img = img[200:(height - 100), 0:width]
    cv2.imwrite(directory + '/steps/images/compare/screenshot1.png', crop_img)


def mse(imagea, imageb):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imagea.astype("float") - imageb.astype("float")) ** 2)
    err /= float(imagea.shape[0] * imageb.shape[1])
    # return the MSE, the lower the error, the more "similar"
    # the two images are


def diff_remove_bg(img0, img, img1):
    d1 = diff(img0, img)
    d2 = diff(img, img1)
    return cv2.bitwise_and(d1, d2)


def compare_images(context, imagename, comparenimage=True):
    time.sleep(10)
    save_image(context, imagename, comparenimage)
    directory = '%s/' % os.getcwd()
    if eval(comparenimage):
        imagea = Image.open(directory + '/steps/images/baseline/' + imagename + '.png')
        imageb = Image.open(directory + '/steps/images/compare/' + imagename + '.png')
        img_diff = Image.new("RGBA", imagea.size)
        mismatch = pixelmatch(imagea, imageb, img_diff, includeAA=True)
        if mismatch <= 150:
            print("The images are the same")
            context.eachStepMessage.append("The images are same. Mismatch count is " + str(mismatch))
            return True
        else:
            img_diff.save(directory + '/steps/images/difference/' + imagename + '.png')
            print("The images are different")
            context.eachStepMessage.append("The images are different. Mismatch count is " + str(mismatch))
            return False
    else:
        return True
