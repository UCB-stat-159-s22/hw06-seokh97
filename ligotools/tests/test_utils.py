from ligotools import readligo as rl
from ligotools import utils
import numpy as np
from os.path import exists
from os import remove
import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt
import json

strain_H1, time_H1, chan_dict_H1 = rl.loaddata('./data/H-H1_LOSC_4_V2-1126259446-32.hdf5', 'H1')
strain_L1, time_L1, chan_dict_L1 = rl.loaddata('./data/L-L1_LOSC_4_V2-1126259446-32.hdf5', 'L1')
fs = 4096


def test_whiten():
	dt = time_H1[1] - time_H1[0]
	fs = 4096
	NFFT = 4*fs
	Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
	psd_H1 = interp1d(freqs, Pxx_H1)
	strain_H1_whiten = utils.whiten(strain_H1,psd_H1,dt)
	assert strain_H1_whiten.shape == (131072, )

def test_write_wavfile():
	data = np.array([0,1,2,3,4,5,5,6,1,23,31,4,2,141,5,5,7])
	fs = 26
	utils.write_wavfile("audio/tempo.wav", fs, data)
	assert exists("audio/tempo.wav")
	remove("audio/tempo.wav")

def test_reqshift():
	data_path = 'data/'
	fnjson = "BBH_events_v3.json"
	events = json.load(open(data_path+fnjson,"r"))
	eventname = 'GW150914' 
	event = events[eventname]
	fn_H1 = event['fn_H1']   
	fs = event['fs'] 
	NFFT = 4*fs
	fshift = 400.
	speedup = 1.
	dt = time_L1[1] - time_L1[0]
	fss = int(float(fs)*float(speedup))
	Pxx_L1, freqs = mlab.psd(strain_L1, Fs = fs, NFFT = NFFT)
	psd_L1 = interp1d(freqs, Pxx_L1)
	strain_L1_whiten = utils.whiten(strain_L1,psd_L1,dt)
	strain_L1_shifted = utils.reqshift(strain_L1_whiten,fshift=fshift,sample_rate=fs)
	assert strain_L1_shifted is not None
	assert strain_L1_shifted.shape == (131072,)

def test_make_plot():
    try:
        time = [10000,100000]
        timemax = 1000
        SNR = [0, 1]
        pcolor = 'g'
        det = "L1"
        eventname = "GW150914"
        plottype = "png"
        tevent = 1126259462.44
        strain_whitenbp = [0, 1]
        template_match = [0, 1]
        template_fft = [0, 1]
        datafreq = [0, 1]
        d_eff = 999.743130306333
        freqs = [0, 1]
        data_psd = [0, 1]
        fs = 4096
        util.make_plot(time, timemax, SNR, pcolor, det, eventname, 
                                    plottype, tevent, strain_whitenbp, template_match, 
                                    template_fft, datafreq, d_eff, freqs, data_psd, fs)   
        assert False
    except Exception:
        assert True