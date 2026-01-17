import cv2
assert cv2.__version__[0] >= '3', 'The fisheye module requires opencv version >= 3.0.0'

import numpy as np
import os
import glob
import sys

DIM=(2592, 1944)
K=np.array([[547.7254929821366, 0.0, 1295.217682317216], [0.0, 545.5174811169118, 961.6482016456428], [0.0, 0.0, 1.0]])
D=np.array([[0.15712663412107852], [-0.19210364585092243], [0.11098079160690723], [-0.03084254189404991]])

def undistort(img_path, out_dir = "fisheye/undistorted"):
	
	img = cv2.imread(img_path)
	h,w = img.shape[:2]
	
	new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, (w, h), np.eye(3), balance=0.0)
	
	map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, DIM, cv2.CV_32FC1)
	undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
	
	os.makedirs(out_dir, exist_ok=True)
	
	filename = os.path.basename(img_path)
	out_path = os.path.join(out_dir, filename)
	
	cv2.imwrite(out_path, undistorted_img)
	print("Saved: ", out_path)
	
	print("K =\n ", K)
	print("D = ", D.ravel())
	print("cx, cy: ", K[0,2], K[1,2])
	print("calibration DIM: ", DIM)
	print("Current image size: ", (w, h))
	print("fx, fy: ", K[0,0], K[1,1])
	
if __name__ == '__main__':
	for p in sys.argv[1:]:
		undistort(p)
	
