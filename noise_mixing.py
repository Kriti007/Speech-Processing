from scipy.io import wavfile
import os

from ..libs import resampy as resampy
import random, numpy, math

def PreProcessing(filename):

    fs, s = wavfile.read(filename)

    # convert to monochannel
    if len(s.shape) > 1:
        temp = numpy.argmin(s.shape)
        #print(temp)
        s = numpy.mean(s, axis=temp)
        #print(s.shape)

    # resample
    #print(s.shape)
    s = resampy.resample(s, fs, 8000)
    fs = 8000
    # magnitude normalization
    s = s/numpy.amax(s)

    return s, fs


def mix_noise(aug_path, processed_file, out_dir, SNRValue, NoiseFile):
        print(processed_file)
        s, fs = PreProcessing(processed_file)
        print(NoiseFile)

        s_n, fs_n = PreProcessing(NoiseFile)
        print("in mixing")
        if len(s_n) < len(s):
            print('Error: Noise file is shorter than Speech file. Cannont mix \n')
            print('Skipping mixing of %s and %s \n' % (NoiseFile, processed_file))
        else:
            print(s, fs, s_n, fs_n)

            nbeg = int(random.uniform(0, 1) * (len(s_n) - len(s)))
            noi = s_n[0 + nbeg: len(s) + nbeg]  # select a random portion from noise file

            M_n = math.sqrt(numpy.mean(noi ** 2))  # RMS of noise
            M_s = math.sqrt(numpy.mean(s ** 2))  # RMS of signal

            noi = noi * (M_s / M_n) * (10 ** (-SNRValue / 20))

            spn = s + noi

            head1, tail1 = os.path.split(processed_file)
            head2, tail2 = os.path.split(NoiseFile)
            SaveName = tail1[0:-4] + '_' + tail2[0:-4] + str(SNRValue) + 'dB' + '.wav'
            wavfile.write(aug_path + out_dir+ SaveName, fs, spn)
