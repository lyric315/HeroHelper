#!/bin/bash

#
#  目前只支持MAC
#

#  安装Android工具
brew  install android-platform-tools

#  安装依赖库
brew install tesseract

sudo pip install pytesseract

sudo pip install tesseract-ocr

#  安装ocr识别资料库
wget https://raw.githubusercontent.com/tesseract-ocr/tessdata/master/chi_sim.traineddata

cp chi_sim.traineddata /usr/local/Cellar/tesseract/3.05.01/share/tessdata

