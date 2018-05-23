import numpy as np 
import scipy.io
import os

import matlab.engine

if __name__ == '__main__':
	#filename = 'ily1.wav'
	eng = matlab.engine.start_matlab()
	args_out = 0
	#eng.AudioTimeFilter(filename, nargout=args_out)
	data_dict = {}

	for file in os.listdir('recordings/ily'):
		if file.endswith('.wav'):
			filename = os.path.join('recordings/ily', file)
			eng.AudioTimeFilter(filename, nargout=args_out)

			loader = scipy.io.loadmat('/home/reidr/senior_design/natural-language/dsp_tool/taco.mat')

			data_dict[filename] = {}

			data_dict[filename]['avg_time_between_keypress'] = np.average(loader['keyPressTimeLog'])

	print(data_dict)


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