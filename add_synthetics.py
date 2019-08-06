import os
from src.data_augmentation import config_reader
import src.data_augmentation.ffmpy as ffmpy


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


def synthetics(out_path,audio_filename, volume, tempo, pitch,out_file):
    config = config_reader.get_config()
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    # change pitch
    calc_pitch = str(int(16000 * pitch))
    cmd_concat = 'asetrate=' + calc_pitch

    if pitch > 1 :

        ffmpeg_cmd(audio_filename,out_path + out_file + "_pitch_high" + ".wav", ['-af',cmd_concat])

    elif pitch <= 1:

        ffmpeg_cmd(audio_filename,out_path + out_file + "_pitch_low" + ".wav", ['-af',cmd_concat])



    # change volume
    cmd_vol = str('volume=' + str(volume))
    if volume > 1 :

        ffmpeg_cmd(audio_filename,out_path + out_file + "_volume_high" + ".wav", ['-filter:a',cmd_vol])


    elif volume <= 1 :

        ffmpeg_cmd(audio_filename,out_path + out_file + "_volume_high" + ".wav", ['-filter:a',cmd_vol])


    # change tempo
    cmd_tempo = str("atempo="+str(tempo))
    if tempo > 1 :

        ffmpeg_cmd(audio_filename,out_path + out_file + "_tempo_high" + ".wav", ['-filter:a',cmd_tempo])


    elif tempo <= 1:

        ffmpeg_cmd(audio_filename,out_path + out_file + "_tempo_low" + ".wav", ['-filter:a',cmd_tempo])



