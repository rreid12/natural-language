import os

import matlab.engine
import scipy.io

class MatlabClient:

	def __init__(self, dir_locations, var_names):
		self.dirs = dir_locations
		self.eng = matlab.engine.start_matlab()
		self.vars_to_extract = var_names

		self.run_dsp_tool()

	def run_dsp_tool(self):
		args_out = 0
		data_dict = {}

		for d in self.dirs:
			for file in os.listdir(d):
				if file.endswith('.wav'):
					filename = os.path.join(d, file)

					self.eng.AudioTimeFilter(filename, nargout=args_out)


if __name__ == '__main__':
	locations = ['recordings/ily_combo', 'recordings/ihy_combo']
	interested_vars = ['keypressTimeLog', 'wordTimeArray']
	client = MatlabClient(locations, interested_vars)

