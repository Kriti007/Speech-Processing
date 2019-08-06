

import  wave
import contextlib
import natsort
import glob
import json
import os
from  ordered_set  import  OrderedSet

def get_config():
    with open('configuration.json', 'r') as f:
        return json.load(f)


def segment(filepath):
    window_size = 320
    window_step = 160
    output = open("segmented_syllables.txt", "w+")
    output1 = open("segmented_syllables_1.txt", "w+")

    for file in natsort.natsorted(glob.glob(filepath+"*/*/*.wav", recursive=True)):

        with contextlib.closing(wave.open(file,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames/float(rate)
        length = duration * 16000

        syl_fname = file.replace("wav","syl")


        frame_info = []
        elem = []
        end = []
        idx = 0
        with open(syl_fname,'r') as f:
            data = f.read().rstrip("\n")
            lines = data.split("\n")
        f.close()
        filename = file[len(filepath): len(file)]+"\t"
        output.write(str(filename))
        for line in lines:
            end.append(int(line.split(" ")[1]))

        for i in range(0, int(length), window_step):
            if(idx < len(end)):
                current_frame = end[idx] / 160
                frame_end = i + window_size - 1

                if (current_frame - int(current_frame) < 0.5 and idx > 1 and end[idx] < frame_end   and end[idx] > i):
                    print(len(frame_info), current_frame,  end[idx])
                    frame_info[len(frame_info) - 1] = [filename, i, frame_end, 2]
                    output.write("2")
                    #print(current_frame)
                    idx = idx+1

                elif(end[idx] < frame_end   and end[idx] > i):
                    elem = [filename, i, frame_end, 2]
                    output.write("2")
                    frame_info.append(elem)
                    idx = idx+1

                else:
                    elem = [filename, i, frame_end, 1]
                    output.write("1")
                    frame_info.append(elem)


        output.write("\n")



        for item in frame_info:
            output1.write("%s\n" % item)
    output1.close()
    output.close()
def  main():
    filepath =  "/Users/path_to_the_wav_files_and_syllable_folder"
    segment(filepath)

if __name__ == '__main__':
    main()


