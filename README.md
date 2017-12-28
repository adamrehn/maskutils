Mask Utilities
==============

This is a simple little Python library for working with 2D image masks. Functionality is provided for ...


Installation
------------

To install, run:

```
pip install maskutils
```


Usage Example
-------------

```
import maskutils
import cv2

# Load our input image
image = cv2.imread('image.png', cv2.IMREAD_UNCHANGED)

# Split the mask (alpha channel) from the other image channels
channels, mask = maskutils.splitAlphaMask(image)

# Extract the subset of the image with mask value zero, blanking all other pixels
zeroOnly = maskutils.isolatePixels(channels, mask, 0)
cv2.imwrite('zero_only.png', zeroOnly)

# Use the OpenCV "connected components" algorithm to extract each segment of contiguous
# mask values, for each unique value in the mask, ignoring mask value zero
instancesForValues = maskutils.extractConnectedComponents(channels, mask, ignoreZero=True)

# Save each segment as an individual image
for maskValue, instances in instancesForValues.items():
	for instanceNum, instance in enumerate(instances):
		subset = maskutils.extract(channels, instance)
		cv2.imwrite('{}_{}.png'.format(maskValue, instanceNum), subset)

```
