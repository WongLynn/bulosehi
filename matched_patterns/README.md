this folder contains some matched patterns recognized by bulosehi.py,
each image contains 300 datapoints which, depending on the ticker updating frequency, is about 15-20 minutes of data.
sometimes the images show a large gap between datas, thus not much is visible, this happened when there were no measurements taken over night, these images can be ignored.

on top of the plot there is a float number, this is the predicted time difference between the patterns/exchanges...

if this number is negative, bitfinex is leading
if this number is positive, bitstamp is leading

accuracy:

9/10 correct leader

6/10 correct time difference
