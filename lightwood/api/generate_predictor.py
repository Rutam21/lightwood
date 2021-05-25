import lightwood
from lightwood.api import LightwoodConfig
from mindsdb_datasources import DataSource
import torch
import numpy as np
import random
import pandas as pd


def override_config(lightwood_config: LightwoodConfig, config_override: dict):
	# TODO: Impl later
	return lightwood_config

def seed():
	torch.manual_seed(66)
	torch.backends.cudnn.deterministic = True
	torch.backends.cudnn.benchmark = False
	np.random.seed(66)
	random.seed(66)

class Predictor():
	def __init__(self, datasource, target):
		seed()
		self.target = target

	def prepare(self, data: DataSource, config_override: dict=None) -> None:
		type_information = lightwood.data.infer_types(data)
		statistical_analysis = lightwood.data.statistical_analysis(data, type_information)
		lightwood_config = lightwood.generate_config(self.target, type_information=type_information, statistical_analysis=statistical_analysis)
		self.lightwood_config = override_config(lightwood_config, config_override)

	def learn(self, data: DataSource) -> None:
		# Build a Graph from the JSON
		# Using eval is a bit ugly and we could replace it with factories, personally I'm against this, as it ads pointless complexity
		self.encoders = {
			(
				col_name,
				col_config['encoder']
			)
			for col_name, col_config in
			self.lightwood_config['features'].items()
		}

		self.model = self.lightwood_config['output']['model']
		self.cleaner = self.lightwood_config['cleaner']
		self.splitter = self.lightwood_config['splitter']
		self.analyzer = self.lightwood_config['analyzer']

		# Do all the trainining and the data cleaning/processing
		data = self.cleaner(data)
		data = self.splitter(data)
		nfolds = len(data)

		for encoder in self.encoders.values():
			self.encoders.fit(data[0:nfolds])

		encoded_data = lightwood.encode(self.encoders, data)
		self.model.fit(encoded_data[0:nfolds], data[0:nfolds])

		self.confidence_model, self.predictor_analysis = self.analyzer(self.model, encoded_data[nfolds], data[nfolds])

	def predict(self, data: DataSource) -> pd.DataFrame:
		encoded_data = lightwood.encode(self.encoders, data)
		df = model(encoded_data)

		return df

def generate_predictor(datasource, target):
    return Predictor(datasource, target)