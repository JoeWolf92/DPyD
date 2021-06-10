import numpy as np
import matplotlib.pyplot as plt
from ALP4 import *
import SLMlayout
# Load the Vialux .dll
DMD = ALP4(version = '4.3', libDir= './')#, libDir = 'E:/ALP-4.3/ALP-4.3 API')
# Initialize the device
DMD.Initialize()
# Get the resolution of the DMD
dmd_res = [DMD.nSizeY,DMD.nSizeX]
center = [DMD.nSizeY//2,DMD.nSizeX//2]
layout = SLMlayout.Hexagons(radius = 350,
                         cellSize = 20,
                         resolution = dmd_res,
                         center = center,
                         gap = 3)
# Retrieve the number of segments
npix = layout.nParts
# Display the layout pattern
# layout.showLayout()
nbImg = 10
DMD.SeqAlloc(nbImg = nbImg, bitDepth = 1)
# Very important, we tell the DMD here that we will use bitplanes
DMD.SeqControl(ALP_DATA_FORMAT,ALP_DATA_BINARY_TOPDOWN)
for ind in range(nbImg):
    # Generate a random phase vector of the same size as the number of macropixels.
    vec = np.exp(1j*np.random.rand(npix)*2.*np.pi)
    # Convert to bitplane
    bitPlane = layout.getBitPlaneFromVec(vec, leePeriod=8, angle = np.pi/4, dataFormat = 'C')
    # Send data to the DMD
    DMD.SeqPut(imgData = bitPlane, PicOffset = ind, PicLoad = 1, dataFormat = 'C')
  
# Set image rate to 50 Hz
DMD.SetTiming(pictureTime = 20000)
# Run the sequence once
DMD.Run(loop = False)
DMD.Halt()
DMD.FreeSeq()
DMD.Free()
mask = layout.getMaskFromBitPlane(bitPlane)
plt.figure()
plt.imshow(mask)
plt.show()
