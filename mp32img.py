import pydub 
import numpy as np
from skimage.io import imread, imsave
import png

def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    smpls = a.get_array_of_samples()
    y = np.array(smpls)
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y

def write(f, sr, x, normalized=False):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    song.export(f, format="mp3", bitrate="320k")

sr, x = read('br.mp3', normalized=False)
#write('br-out.mp3', sr, x, normalized=False)

xlarge = x.astype(np.int32)
xlarge = (xlarge + 255) / 2
img = xlarge.astype(np.uint16).reshape((4096, 4497))
imsave('test.png', img)


out = imread('test.png')
outlarge = out.astype(np.int32)
outlarge = (outlarge * 2) - 255
y = outlarge.astype(np.int16).reshape((9209856, 2))
write('br-out.mp3', sr, y)
