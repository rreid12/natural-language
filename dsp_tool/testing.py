import numpy as np 
import scipy.io
import os

import matlab.engine

if __name__ == '__main__':
	eng = matlab.engine.start_matlab()
	args_out = 0
	data_dict = {}

	for file in os.listdir('recordings/ily'):
		if file.endswith('.wav'):
			filename = os.path.join('recordings/ily', file)
			eng.AudioTimeFilter(filename, nargout=args_out)

			loader = scipy.io.loadmat('/home/reidr/senior_design/natural-language/dsp_tool/to_language_model.mat')

			data_dict[filename] = {}

			data_dict[filename]['avg_time_between_keypress'] = np.average(loader['keyPressTimeLog'])

	print(data_dict)