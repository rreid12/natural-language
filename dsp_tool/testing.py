import numpy as np 
import scipy.io

import matlab.engine

if __name__ == '__main__':
	eng = matlab.engine.start_matlab()
	args_out = 0
	eng.AudioTimeFilter("ily1.wav", nargout=args_out)

	loader = scipy.io.loadmat('/home/reidr/senior_design/natural-language/dsp_tool/testing.mat')
	print(loader)
	'''print(loader['keyPressTimeLog'])
	print(loader['timeLog'])
	'''

	'''
	-Change .m to accept a filename/path as its input argument
	-iterate through all .wav files in folder, running matlab script on each
	-adjust matlab output
		-.mat files?
		-return arguments directly from matlab?
	-organize data
	'''

	'''
	for all files in ily:
		call matlab script to analyze and return data

	'''

'''
hate:0
love:1

{
	ily1.wav: {
		phrase_typing_time:
		typing_time_per_word:
		avg_time_between_keypress:
		keypress_timelog:
		isLove:
	}

}
'''