import os
import wget
import sys
import commands
import string
import random
import os.path
import urllib

def resize(old_file, new_file):    
    
    tmp_dir = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/tmp'
    #tmp_dir = '/tmp/plsang/resize'
    tmp_file = os.path.join(tmp_dir, os.path.basename(new_file))
        
    command = 'ffmpeg -i ' + old_file
    line = commands.getoutput(command)
    tokens = line.split()
    found = 0;
    print command
    for token in tokens:
        if 'x' in token and 'Header' not in token:
            #print 'Found token: ' + token
            tks = token.strip(',').split('x') # bugs: must strip ',' before spliting
            if tks[0].isdigit() and tks[1].isdigit():
                w = eval(tks[0])
                h = eval(tks[1])
                print 'Found token: ' + token
                found = 1;
                break

    line = commands.getoutput(command)
    tokens = line.split(',')
    found_fps = 0;
    for token in tokens:
        if 'fps' in token and 'Header' not in token:
            #print 'Found token: ' + token
            tks = token.strip().split(' ') # bugs: must strip ',' before spliting    
            if tks[0].replace('.', '').isdigit():
                fps = eval(tks[0])
                print 'Found fps: ' + str(fps)
                found_fps = 1;
                break

    if not found:
        print "Video size not found for video " + old_file
        
        with open(log_file, "a+") as f:
            f.write("Video size not found for video " + old_file + "\n") # python will convert \n to os.linesep
        
        return
    
    if not found_fps:
        print "FPS not found for video " + old_file
        with open(log_file, "a+") as f:
           
            f.write(("FPS not found for video <%s>. Used default fps %f instead! \n") % (old_file, 25) ) # python will convert \n to os.linesep
            f.close()
            fps = 25

        
    #command = 'ffmpeg -i ' + old_file + ' -s '+str(int(w*float(size)))+'x'+str(int(h*float(size))) + ' ' + new_file
    new_h = int(round(320*h/w));
    if new_h % 2 != 0:
        new_h = new_h - 1 
    print w, h, 320, new_h
    #command = 'ffmpeg -i ' + old_file + ' -sameq -f mp4 -ab 16k -s 320x' + str(new_h) + ' -aspect ' + str(w) + ':' + str(h) + ' ' + new_file
        
    if fps <= 60:
        #update Aug 17th: some time the resized video may have very high fps, says up to 1000fps. so consider about force using the original frame-rate
        
        command = 'ffmpeg -i ' + old_file + ' -y -loglevel quiet -c:v libx264 -crf 19 -preset slow -c:a libfdk_aac -ac 2 -r ' + str(fps) + ' -s 320x' + str(new_h) + ' -aspect ' + str(w) + ':' + str(h) + ' ' + tmp_file
        
    else:
        command = 'ffmpeg -i ' + old_file + ' -y -loglevel quiet -c:v libx264 -crf 19 -preset slow -c:a libfdk_aac -b:a 192k -ac 2 -r 25 -s 320x' + str(new_h) + ' -aspect ' + str(w) + ':' + str(h) + ' ' + tmp_file
        
        with open(log_file, "a+") as f:
            f.write(("FPS too high %f. Used default fps %f instead! " + old_file + "\n") % (fps, 25) ) # python will convert \n to os.linesep
        
    print command
    #commands.getoutput(command)
    exit_status = os.system(command)
    if not exit_status:
        #moving tmp_file to new_file
        command = 'mv -f ' + tmp_file + ' ' + new_file
        os.system(command);
    else:
        with open(log_file, "a+") as f:
            f.write( "Failed to resize video: %s - Exit code: %d - Command: %s \n" % (old_file, exit_status, command) ) # python will convert \n to os.linesep
    
            
if __name__ == '__main__':

    parts = ['yfcc100m_dataset-'+str(i) for i in range(0,10)]
    
    if (len(sys.argv) < 2):
        print sys.argv[0] + " <part name>", parts
        exit()

    part = sys.argv[1]
    
    input_dir = '/net/per610a/export/das11f/plsang/dataset/YFCC100M'
    output_dir = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m'
    #download_dir = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/tmp/download'
    download_dir = '/tmp'
    log_dir = '/net/per920a/export/das14a/satoh-lab/plsang/yfcc100m/log'
    
    log_file = os.path.join(log_dir, part + '.txt')
    
    count = 0
     
    meta_file = os.path.join(input_dir, part)
    
    output_part_dir = os.path.join(output_dir, part)
    
    if not os.path.exists(output_part_dir):
        os.makedirs(output_part_dir)
    
    with open(meta_file) as f:
        for line in f:
            info = line.rstrip('\n').split('\t');
            if info[-1] == '1':
                video_id = info[0]
                output_file = os.path.join(output_part_dir, video_id + '.mp4')
                if os.path.exists(output_file):
                    print 'File existed', output_file
                    count = count + 1
                    continue
                
                print '---- ', count, 'Downloading video', video_id, info[14]
                
                try:
                    os.chdir(download_dir)
                    downloaded_file = wget.download(info[14], out=download_dir)
                except:
                    print "Could not download file <%s>\n" % (info[14])
                    with open(log_file, "a+") as f:
                        f.write( "Could not download file <%s> \n" % (info[14]) )
                    continue
                
                filename = os.path.basename(downloaded_file)
                
                if os.path.splitext(filename)[1] == '.mp4':
                    resized_file = os.path.join(output_part_dir, filename)
                else:
                    resized_file = os.path.join(output_part_dir, os.path.splitext(filename)[0] + '.mp4')
                
                if not os.path.exists(resized_file):
                    print '----- Resizing video', filename
                    try:
                        resize(downloaded_file, resized_file)
                        count = count + 1
                    except:
                        print "Could not resize file <%s>\n" % (downloaded_file)
                        with open(log_file, "a+") as f:
                            f.write( "Could not resize file <%s> \n" % (downloaded_file) )
                
                os.remove(downloaded_file)
    
    print '*** Total downloaded videos:', count
    
    with open(log_file, "a+") as f:
        f.write( "Total downloaded videos: %d \n" % (count) )
