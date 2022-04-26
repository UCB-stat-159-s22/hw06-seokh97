from ligotools import readligo as rl
from ligotools import utils as u
import numpy as np
from os.path import exists
from os import remove
import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt

def test_whiten():
	strain_H1, time_H1, chan_dict_H1 = rl.loaddata("data/H-H1_LOSC_4_V2-1126259446-32.hdf5", 'H1')
	fs = 4096
	NFFT = 4*fs
	time = time_H1
	Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
	psd_H1 = interp1d(freqs, Pxx_H1)
	dt = time[1] - time[0]
	strain_H1_whiten = u.whiten(strain_H1,psd_H1,dt)
	assert (starin_H1_whiten is not None)

def test_write_wavfile():
	data = np.array([0,1,2,3,4,5,5,6,1,23,31,4,2,141,5,5,7])
	fs = 26
	utils.write_wavfile("audio/tempo.wav", fs, data)
	assert exists("audio/tempo.wav")
	remove("audio/tempo.wav")

def test_reqshift():
	data = np.linspace(0,1000,100)
	assert sum(utils.reqshift(data,fshift=204,sample_rate=2048))== -2.2737367544323206e-13

def test_plot_whitened():
	strain_H1, time_H1, chan_dict_H1 = rl.loaddata("data/H-H1_LOSC_4_V2-1126259446-32.hdf5", 'H1')
	fs = 4096
	NFFT = 4*fs
	fband = [43.0, 300.0]
	time = time_H1
	Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
	psd_H1 = interp1d(freqs, Pxx_H1)
	dt = time[1] - time[0]
	strain_H1_whiten = u.whiten(strain_H1,psd_H1,dt)
	bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
	normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
	strain_H1_whitenbp = filtfilt(bb, ab, strain_H1_whiten) / normalization
	timemax = time[6]
	u.plot_whitened(time = time, tevent = 1126259462.44, strain_H1_whitenbp, 'g', dets = 'H1',
					timemax = timemax, template_match = strain_H1_whitenbp, eventname = 'GW150914', plottype = "png")
	assert exists('figures/'+'GW150914'+"_"+"H1"+"_matchtime."+"png")
	remove('figures/'+'GW150914'+"_"+"H1"+"_matchtime."+"png")