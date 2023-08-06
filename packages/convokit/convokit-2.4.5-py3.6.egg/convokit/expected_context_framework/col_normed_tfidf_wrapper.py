from .col_normed_tfidf import ColNormedTfidf
from convokit.transformer import Transformer

import numpy as np

class ColNormedTfidfWrapper(Transformer):
	
	def __init__(self, input_field, output_field='col_normed_tfidf', **kwargs):
		self.tfidf_obj = ColNormedTfidf(**kwargs)
		self.input_field = input_field
		self.output_field = output_field
		if self.input_field == 'text':
			self.text_func = lambda x: x.text
		else:
			self.text_func = lambda x: x.meta[self.input_field]
	
	def fit(self, corpus, y=None, selector=lambda x: True):
		docs = [self.text_func(ut) for ut in corpus.iter_utterances(selector=selector)]
		self.tfidf_obj.fit(docs)
		return self
	
	def transform(self, corpus, selector=lambda x: True): 
		ids = []
		docs = []
		for ut in corpus.iter_utterances(selector=selector):
			ids.append(ut.id)
			docs.append(self.text_func(ut))
			ut.add_vector(self.output_field)
		vects = self.tfidf_obj.transform(docs)
		column_names = self.tfidf_obj.get_feature_names()
		corpus.set_vector_matrix(self.output_field, matrix=vects, ids=ids, columns=column_names)
		n_feats = np.array((vects>0).sum(axis=1)).flatten()
		for id, n in zip(ids, n_feats):
			corpus.get_utterance(id).meta[self.output_field + '__n_feats'] = n
		return corpus
	
	def fit_transform(self, corpus, y=None, selector=lambda x: True):
		self.fit(corpus, y, selector)
		return self.transform(corpus, selector)
	
	def get_vocabulary(self):
		return self.tfidf_obj.get_feature_names()
	
	def load_model(self, dirname):
		self.tfidf_obj.load(dirname)
	
	def dump_model(self, dirname):
		self.tfidf_obj.dump(dirname)