import slidingwindow as sw
import numpy as np
import cv2

def splitAlphaMask(image):
	"""
	Splits the last channel of an image from the rest of the channels.
	Useful for splitting away the alpha channel of an image and treating
	it as the image mask.
	
	The input image should be a NumPy array of shape [h,w,c].
	
	The return value is a tuple of the image channels and the mask.
	"""
	channels = image[:, :, 0 : image.shape[2]-1]
	mask = image[:, :, image.shape[2]-1]
	return channels, mask


def isolatePixels(image, mask, maskValue):
	"""
	Creates a copy of the supplied image where all pixels whose mask
	value does not match the specified value are set to zero.
	"""
	pixelsToIgnore = np.nonzero(mask != maskValue)
	isolated = image.copy()
	isolated[pixelsToIgnore] = 0
	return isolated


def extractConnectedComponents(image, mask, ignoreZero = False, preciseBounds = False):
	"""
	Uses the OpenCV "connected components" algorithm to extract individual
	image segments that are represented by contiguous areas of identical
	values in the image mask.
	
	The return value is a dictionary whose keys are the unique values in the
	mask, and whose values are the list of bounds representing each of the
	contiguous areas for each key.
	
	If `preciseBounds` is False then each list item is a simple rectangle,
	represented by tuple of (x,y,w,h).
	
	If `preciseBounds` is True then each list item is a rotated rectangle,
	represented by a tuple of (centre, size, rotation).
	"""
	
	# Create the dictionary to hold the mappings from mask value to list of bounds
	instancesForValues = {}
	
	# Iterate over each unique value in the mask
	maskValues = np.unique(mask)
	
	for maskValue in maskValues:
		
		# If we have been asked to ignore mask value zero, do so
		if maskValue == 0 and ignoreZero == True:
			continue
		
		# Zero-out the pixels for all of the other mask values
		valueInstances = isolatePixels(mask, mask, maskValue)
		
		# Use the "connected components" algorithm to extract the subsets for each contiguous area of the current mask value
		ret, markers, stats, centroids = cv2.connectedComponentsWithStats(valueInstances)
		
		# Add the bounds for each identified instance to our mappings
		instancesForValues[maskValue] = []
		instances = np.unique(markers)
		for instance in instances:
			
			# Ignore instance zero, which contains the entire image
			if instance != 0:
				
				# Determine if we are retrieving simple bounds or precise bounds for each instance
				if preciseBounds == True:
					
					# Compute the precise bounds of the instance
					contiguous = np.ascontiguousarray(isolatePixels(mask, markers, instance), dtype=np.uint8)
					_, contours, hierarchy = cv2.findContours(contiguous, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
					instancesForValues[maskValue].append(cv2.minAreaRect(contours[0]))
					
				else:
					
					# Extract the simple bounds of the instance
					x = stats[instance, cv2.CC_STAT_LEFT]
					y = stats[instance, cv2.CC_STAT_TOP]
					w = stats[instance, cv2.CC_STAT_WIDTH]
					h = stats[instance, cv2.CC_STAT_HEIGHT]
					instancesForValues[maskValue].append( (x,y,w,h) )
	
	return instancesForValues


def extract(image, bounds):
	"""
	Extracts a subset of an image, given a tuple of (x,y,w,h).
	"""
	x,y,w,h = bounds
	return sw.SlidingWindow(x, y, w, h, sw.DimOrder.HeightWidthChannel).apply(image)
