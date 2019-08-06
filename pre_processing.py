import wave
import os
import src.data_augmentation.config_reader as config_reader
from ..libs.ffmpy import ffmpy as ffmpy

def remove(path):
    if os.path.exists(path):
        os.remove(path)
    return

def ffmpeg_cmd(input, output, cmd):
    remove(output)
    ff = ffmpy.FFmpeg(
        inputs={input : None},
        outputs={output : cmd}
    )
    ff.run()
    return

def pre_process(in_path, audio_file, out_file, processed):
    # convert to wav
    ext = audio_file.split(".")[1]
    filename_1 = in_path+"/"+audio_file
    config = config_reader.get_config()
    if ext != '.wav':

            ffmpeg_cmd(filename_1, processed+out_file, None)
            filename_1 = processed+out_file


    # check frame rate and convert frame rate
    with wave.open(filename_1, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channel_count = wave_file.getnchannels()

        if frame_rate != 16000 and channel_count > 1 :

            ffmpeg_cmd(filename_1, processed+ config["FRAME_ADJUSTED"] + out_file ,['-y','-r','16'])
            filename = processed + config["FRAME_ADJUSTED"] + out_file

            ffmpeg_cmd(filename, processed+out_file,['-ac',  '1'] )
            filename_1 = processed + out_file

        elif frame_rate != 16000 and channel_count == 1 :

                ffmpeg_cmd(filename_1, processed+ config["FRAME_ADJUSTED"] + out_file,['-y','-r','16'] )
                remove(processed + out_file)
                filename_1 = processed + out_file

        elif channel_count > 1 and frame_rate == 16000:

            ffmpeg_cmd(filename_1, processed + out_file, ['-ac', '1'] )
            filename_1 = processed + out_file

    return filename_1
