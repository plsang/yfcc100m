YFCC_ROOT=/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m

all:

create_table:
	python yfcc100m_create_table.py /net/per610a/export/das11f/plsang/dataset/YFCC100M --dbname yfcc100m --collection metadata
demo:
	python read_video.py $(YFCC_ROOT)/park_1_5_split_selected-webm-mp4/2956592867-1.mp4 out.avi --gid 7
detect_person:
	python yfcc100m_person_detection.py --gid=3 2>&1 | tee log/yfcc100m_person_detection.log
cut_videos:
	python yfcc100m_cut_videos.py --min_person 3 --max_person 5 --num_cpu 1 \
		--duration 5 --output_dir /net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/yfcc10k \
		2>&1 | tee log/yfcc100m_cut_videos.log
