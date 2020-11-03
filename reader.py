from pytesseract import Output
import pytesseract
import argparse
import cv2
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-c", "--min-conf", type=int, default=50,
	help="mininum confidence value to filter weak text detection")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
image2 = image.copy()
(H,W) = image.shape[:2]
#image = cv2.resize(image,(int(W*25/100),int(H*25/100)))
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

# loop over each of the individual text localizations
for i in range(0, len(results["text"])):
	# extract the bounding box coordinates of the text region from
	# the current result
	x = results["left"][i]
	y = results["top"][i]
	w = results["width"][i]
	h = results["height"][i]
	# extract the OCR text itself along with the confidence of the
	# text localization
	text = results["text"][i]
	conf = int(results["conf"][i])


	# filter out weak confidence text localizations
	if conf > args["min_conf"] and w*h < 40000 and text!=" ":
		# display the confidence and text to our terminal
		print("Confidence: {}".format(conf))
		print("Text: {}".format(text))
		print("")
		# strip out non-ASCII text so we can draw the text on the image
		# using OpenCV, then draw a bounding box around the text along
		# with the text itself
		text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
		cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
			1.2, (0, 0, 255), 3)

gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

(T, threshInv) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

for i in range(0, len(results["text"])):
	# extract the bounding box coordinates of the text region from
	# the current result
	x = results["left"][i]
	y = results["top"][i]
	w = results["width"][i]
	h = results["height"][i]
	# extract the OCR text itself along with the confidence of the
	# text localization
	text = results["text"][i]
	conf = int(results["conf"][i])


	# filter out weak confidence text localizations
	if conf > args["min_conf"] and w*h < 40000 and len(text)>1:
		# display the confidence and text to our terminal
		print("Confidence: {}".format(conf))
		print("Text: {}".format(text))
		print("Len: {}".format(len(text)))
		# strip out non-ASCII text so we can draw the text on the image
		# using OpenCV, then draw a bounding box around the text along
		# with the text itself
		text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
		cv2.rectangle(threshInv, (x, y), (x + w, y + h), (0, 0, 0), -1)


threshInv = cv2.resize(threshInv,(int(W*25/100),int(H*25/100)))
dilate = cv2.dilate(threshInv.copy(),(15,1))

for i in range(0,4):
	dilate = cv2.dilate(dilate,(15,1))

cnts,_ = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#cnts = imutils.grab_contours(cnts)

for c in cnts:
	area = cv2.contourArea(c)
	
	if(area > 10000):
		cv2.drawContours(image, [c*4], -1, (255, 0, 0), 2)


# show the output image
#cv2.imshow("Image", image)
cv2.imwrite("test.jpg",image)
#cv2.waitKey(0)
