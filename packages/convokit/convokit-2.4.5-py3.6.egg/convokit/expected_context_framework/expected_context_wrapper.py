from .expected_context_model import ExpectedContextModel

from convokit.transformer import Transformer
import numpy as np 
import pandas as pd



class ExpectedContextModelWrapper(Transformer):
	
	def __init__(self, context_field,output_prefix,
				 vect_field, context_vect_field=None,
				n_svd_dims=25, snip_first_dim=True, n_clusters=8, cluster_on='utts',
				model=None, random_state=None, cluster_random_state=None):
		if model is not None:
			in_model = model.ec_model
		else:
			in_model = None
		self.ec_model = ExpectedContextModel(model=in_model,
			n_svd_dims=n_svd_dims, snip_first_dim=snip_first_dim, n_clusters=n_clusters, cluster_on=cluster_on,
			random_state=random_state, cluster_random_state=cluster_random_state)
		self.context_field = context_field
		if context_field == 'reply_to':
			self.context_func = lambda x: x.reply_to
		else:
			self.context_func = lambda x: x.meta.get(context_field, None)
		self.output_prefix = output_prefix
		self.vect_field = vect_field
		self.context_vect_field = context_vect_field
		if self.context_vect_field is None:
			self.context_vect_field = vect_field
	
	def fit(self, corpus, y=None, selector=lambda x: True, context_selector=lambda x: True):
	
		id_to_idx = corpus.get_vector_matrix(self.vect_field).ids_to_idx
		context_id_to_idx = corpus.get_vector_matrix(self.context_vect_field).ids_to_idx
		
		
		ids = []
		context_ids = []
		mapping_ids = []
		context_mapping_ids = []
		for ut in corpus.iter_utterances(selector=selector):
			ids.append(ut.id)
			context_id = self.context_func(ut)
			if context_id is not None:
				try:
					if context_selector(corpus.get_utterance(context_id)):
						try:
							mapping_ids.append(ut.id)
							context_mapping_ids.append(context_id)
						except: continue
				except:
					print(context_id)
					break
					
		for ut in corpus.iter_utterances(selector=context_selector):
			context_ids.append(ut.id)

		id_to_idx = {id: i for i, id in enumerate(ids)}
		context_id_to_idx = {id: i for i, id in enumerate(context_ids)}
		mapping_idxes = [id_to_idx[x] for x in mapping_ids]
		context_mapping_idxes = [context_id_to_idx[x] for x in context_mapping_ids]
		
		utt_vects = corpus.get_vectors(self.vect_field, ids)
		context_utt_vects = corpus.get_vectors(self.context_vect_field, context_ids)
		mapping_table = np.vstack([mapping_idxes, context_mapping_idxes]).T
		self.mapping_table = mapping_table
		terms = corpus.get_vector_matrix(self.vect_field).columns
		context_terms = corpus.get_vector_matrix(self.context_vect_field).columns
		self.ec_model.fit(utt_vects, context_utt_vects, mapping_table,
						 terms, context_terms, utt_ids=ids, context_utt_ids=context_ids)
			
	def _get_matrix(self, corpus, field, selector):
		ids = [ut.id for ut in corpus.iter_utterances(selector=selector)
			  if field in ut.vectors]
		utt_vects = corpus.get_vectors(field, ids)
		return ids, utt_vects
	
	def _add_vector(self, corpus, field, ids):
		for id in ids:
			corpus.get_utterance(id).add_vector(field)
	
	def transform(self, corpus, selector=lambda x: True):

		ids, utt_vects = self._get_matrix(corpus, self.vect_field, selector)
		utt_reprs = self.ec_model.transform(utt_vects)
		corpus.set_vector_matrix(self.output_prefix + '_repr', matrix=utt_reprs,
								ids=ids)
		self._add_vector(corpus, self.output_prefix + '_repr', ids)
		self.compute_utt_ranges(corpus, selector)
		self.compute_clusters(corpus, selector)
		return corpus
	
	def compute_utt_ranges(self, corpus, selector=lambda x: True):
		
		ids, utt_vects = self._get_matrix(corpus, self.vect_field, selector)
		ranges = self.ec_model.compute_utt_ranges(utt_vects)
		for id, r in zip(ids, ranges):
			corpus.get_utterance(id).meta[self.output_prefix + '_range'] = r
		return ranges
	
	def transform_context_utts(self, corpus, selector=lambda x: True):
		ids, context_utt_vects = self._get_matrix(corpus, self.context_vect_field, selector)
		context_utt_reprs = self.ec_model.transform_context_utts(context_utt_vects)
		corpus.set_vector_matrix(self.output_prefix + '_context_repr', matrix=context_utt_reprs,
								ids=ids)
		self._add_vector(corpus, self.output_prefix + '_context_repr', ids)
		self.compute_clusters(corpus, selector, is_context=True)
		return corpus
	
	def fit_clusters(self, n_clusters, random_state='default'):
		if random_state == 'default':
			random_state = self.ec_model.random_state
		self.ec_model.fit_clusters(n_clusters, random_state)
	
	def compute_clusters(self, corpus, selector=lambda x: True, is_context=False, cluster_suffix=''):
		if is_context:
			ids, reprs = self._get_matrix(corpus, self.output_prefix + '_context_repr', selector)
		else:
			ids, reprs = self._get_matrix(corpus, self.output_prefix + '_repr', selector)
		cluster_df = self.ec_model.transform_clusters(reprs, ids)
		if is_context:
			cluster_field = self.output_prefix + '_context_clustering'
		else:
			cluster_field = self.output_prefix + '_clustering'
		cluster_field += cluster_suffix
		for id, entry in cluster_df.iterrows():
			for k, v in entry.to_dict().items():
				corpus.get_utterance(id).meta[cluster_field + '.' + k] = v
		return cluster_df
	
	def set_cluster_names(self, cluster_names):
		self.ec_model.set_cluster_names(cluster_names)
	
	def get_cluster_names(self):
		return self.ec_model.get_cluster_names()
	
	def print_clusters(self, k=10, max_chars=1000, corpus=None):
		n_clusters = self.ec_model.n_clusters
		cluster_obj = self.ec_model.clustering
		for i in range(n_clusters):
			print('CLUSTER', i, self.ec_model.get_cluster_names()[i])
			print('---')
			print('terms')
			term_subset = cluster_obj['terms'][cluster_obj['terms'].cluster_id_ == i].sort_values('cluster_dist').head(k)
			print(term_subset[['cluster_dist']])
			print()
			print('context terms')
			context_term_subset = cluster_obj['context_terms'][cluster_obj['context_terms'].cluster_id_ == i].sort_values('cluster_dist').head(k)
			print(context_term_subset[['cluster_dist']])
			print()
			if corpus is None: continue
			print()
			print('utterances')
			utt_subset = cluster_obj['utts'][cluster_obj['utts'].cluster_id_ == i].drop_duplicates('cluster_dist').sort_values('cluster_dist').head(k)
			for id, row in utt_subset.iterrows():
				print('>', id, '%.3f' % row.cluster_dist, corpus.get_utterance(id).text[:max_chars])
			print()
			print('context utterances')
			context_utt_subset = cluster_obj['context_utts'][cluster_obj['context_utts'].cluster_id_ == i].drop_duplicates('cluster_dist').sort_values('cluster_dist').head(k)
			for id, row in context_utt_subset.iterrows():
				print('>>', id, '%.3f' % row.cluster_dist, corpus.get_utterance(id).text[:max_chars])
			print('\n====\n')
	
	def print_cluster_stats(self):
		cluster_obj = self.ec_model.clustering
		return pd.concat([
			cluster_obj[k].cluster.value_counts(normalize=True).rename(k).sort_index()
			for k in ['utts', 'terms', 'context_utts', 'context_terms']
		], axis=1)
	
	def get_terms(self):
		return self.ec_model.terms 

	def get_term_ranges(self):
		return self.ec_model.term_ranges

	def get_term_reprs(self):
		return self.ec_model.term_reprs

	def get_context_terms(self):
		return self.ec_model.context_terms

	def get_context_term_reprs(self):
		return self.ec_model.context_term_reprs

	def get_clustering(self):
		return self.ec_model.clustering

	def get_cluster_names(self):
		return self.ec_model.get_cluster_names()

	def load(self, dirname):
		self.ec_model.load(dirname)
	
	def dump(self, dirname, dump_clustering=True):
		self.ec_model.dump(dirname, dump_clustering)
