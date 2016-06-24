YFCC_ROOT=/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m

all:

demo:
	python read_video.py $(YFCC_ROOT)/park_1_5_split_selected-webm-mp4/2956592867-1.mp4 out.avi --gid 7 
