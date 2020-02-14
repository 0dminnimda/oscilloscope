import numpy as np
from scipy import signal
from scipy.io.wavfile import read, write
import pygame
from pygame.locals import *
from pygame_draw import pyg_draw, Grid, mou_pos

def gen(freq, fs, T):
    t = np.linspace(0, T, T * fs, False)
    val = freq * t * 2* np.pi
    nsin = np.sin(val)
    ncos = np.cos(val)
    nsqr = signal.square(val)
    nsth = signal.sawtooth(val/8)
    nsin2 = np.sin(val/8)
    audio = np.zeros(((fs * T), 2))
    audio[:, 0] = nsin# - nsin2
    audio[:, 1] = ncos + np.roll(nsth, 0)
    #np.roll(note2, 25)
    return audio

def comp(audio):
    audiot = audio.copy()
    audiot *= 32767 / np.max(np.abs(audio))
    audiot = audiot.astype(np.int16)
    return audiot

def noi(fs, T, mul, arr=None):
    noise = np.random.normal(0, 1, T  * fs)
    #noise2 = np.random.normal(0, 1, T  * fs)
    if isinstance(arr, type(None)) is True:
        arr = np.zeros(((fs * T), 2))
    arr[:, 0] += noise*mul[0]
    arr[:, 1] += noise*mul[1]
    return arr

freq = 150
fs = 44100
T = 4
it = 0
au = gen(freq, fs, T)
aun = noi(fs, T, (0, 0), au)

mai = au

mu = comp(mai)
n = "randmus.wav"
write(n, fs, mu)

pas = 10

evst = fs
stra = T * fs // evst
pd = pyg_draw(2)
w, h = pd.scr
mul = 100
clock = pygame.time.Clock()
pygame.mixer.music.load(n)
pygame.mixer.music.set_volume(0.1)

while 1:
    pygame.mixer.music.play()
        
    for it in range(stra):
        clock.tick(stra)
        for i in pygame.event.get():
            if i.type == pygame.QUIT or i.type == K_ESCAPE:
                import sys
                sys.exit()

        for j in range(0, evst, pas):
            pos = [mai[j*it, 0]*mul, mai[j*it, 1]*mul]
            pos[0] += w/2
            pos[1] += h/2
            pd.circ(pos, 2)

        pd.upd()
        pd.fill()