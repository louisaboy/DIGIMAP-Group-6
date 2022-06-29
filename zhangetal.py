import matplotlib.pyplot as plt
from colorizers import *
from PIL import Image
from io import BytesIO
import numpy as np
import base64

def generate_images(img_path="", use_gpu=False):
	# load colorizers
	colorizer_eccv16 = eccv16(pretrained=True).eval()
	colorizer_siggraph17 = siggraph17(pretrained=True).eval()
	if(use_gpu):
		colorizer_eccv16.cuda()
		colorizer_siggraph17.cuda()

	# default size to process images is 256x256
	# grab L channel in both original ("orig") and resized ("rs") resolutions
	img = load_img(img_path)
	(tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256,256))
	if(use_gpu):
		tens_l_rs = tens_l_rs.cuda()

	# colorizer outputs 256x256 ab map
	# resize and concatenate to original L channel
	img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
	out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
	# print(out_img_eccv16[0, 0, :])
	# print(out_img_eccv16[0, 0, :] * 255)

	output = Image.fromarray((out_img_eccv16*255).astype(np.uint8))
	# print(output.getpixel((0, 0)))
	buffered = BytesIO()
	output.save(buffered, 'PNG')

	buffered.seek(0)
	im_64 = base64.b64encode(buffered.read()).decode()

	return im_64