from convokit.expected_context_framework import ColNormedTfidfTransformer, ExpectedContextModelTransformer, DualContextWrapper

from convokit.transformer import Transformer
from convokit.convokitPipeline import ConvokitPipeline
from convokit.text_processing import TextProcessor
from convokit import Utterance, Speaker

import os

class ExpectedContextModelPipeline(Transformer):
    
    def __init__(self, 
        context_field, output_prefix, 
        text_field, context_text_field=None,
        text_pipe=None, context_text_pipe=None,
        tfidf_params={}, context_tfidf_params=None, share_tfidf_models=True,
        min_terms=0, context_min_terms=None,
        n_svd_dims=25, snip_first_dim=True, n_clusters=8, cluster_on='utts',
        ec_model=None,
        random_state=None, cluster_random_state=None):

        self.context_field = context_field
        self.output_prefix = output_prefix
        
        self.vect_field = 'col_normed_tfidf'
        self.share_tfidf_models = share_tfidf_models
        
        if share_tfidf_models:
            self.context_vect_field = self.vect_field
        else:
            self.context_vect_field = 'context_col_normed_tfidf'
        
        
        self.text_field = text_field
        if context_text_field is None:
            self.context_text_field = text_field
        else:
            self.context_text_field = context_text_field
        
        if text_pipe is None:
            self.text_pipe = ConvokitPipeline([
                ('text_pipe', TextProcessor(output_field=self.text_field,
                               proc_fn=lambda x: x))
            ])
        else:
            self.text_pipe = text_pipe
        
        if context_text_pipe is None:
            self.context_text_pipe = self.text_pipe
        else:
            self.context_text_pipe = context_text_pipe
        
        self.tfidf_params = tfidf_params
        if context_tfidf_params is None:
            self.context_tfidf_params = tfidf_params
        else:
            self.context_tfidf_params = context_tfidf_params
        
        self.min_terms = min_terms
        if context_min_terms is None:
            self.context_min_terms = min_terms
        else:
            self.context_min_terms = context_min_terms
        
        if ec_model is not None:
            in_model = ec_model.ec_model
        else:
            in_model = None
        self.ec_model = ExpectedContextModelTransformer(
            context_field=context_field, output_prefix=output_prefix,
            vect_field=self.vect_field,
            context_vect_field=self.context_vect_field,
            model=in_model,
            n_svd_dims=n_svd_dims, snip_first_dim=snip_first_dim, n_clusters=n_clusters, cluster_on=cluster_on,
            random_state=random_state, cluster_random_state=cluster_random_state)
        
        
        self.tfidf_model = ColNormedTfidfTransformer(
            input_field=self.text_field,
            output_field=self.vect_field, **self.tfidf_params
        )
        if not share_tfidf_models:
            self.context_tfidf_model = ColNormedTfidfTransformer(
                input_field=self.context_text_field,
                output_field=self.context_vect_field,
                **self.context_tfidf_params
            )
        else:
            self.context_tfidf_model = self.tfidf_model
        
        
    def fit(self, corpus, y=None, selector=lambda x: True, context_selector=lambda x: True):
        self.text_pipe.fit_transform(corpus)
        if not self.share_tfidf_models:
            self.context_text_pipe.fit_transform(corpus)
        self.tfidf_model.fit_transform(corpus, selector=selector)
        if not self.share_tfidf_models:
            self.context_tfidf_model.fit_transform(corpus, selector=context_selector)
        self.ec_model.fit(corpus, 
            selector=lambda x: selector(x)
             and (x.meta.get(self.vect_field + '__n_feats',0) >= self.min_terms),
            context_selector=lambda x: context_selector(x)
             and (x.meta.get(self.context_vect_field + '__n_feats',0) >= self.context_min_terms))
    
    def transform(self, corpus, y=None, selector=lambda x: True):
        _ = self.text_pipe.transform(corpus)
        _ = self.tfidf_model.transform(corpus, selector=selector)
        _ = self.ec_model.transform(corpus, selector=lambda x: selector(x)
             and (x.meta.get(self.vect_field + '__n_feats',0) >= self.min_terms))
        return corpus
    
    def transform_utterance(self, utt):
        if isinstance(utt, str):
            utt = Utterance(text=utt, speaker=Speaker()) 
        self.text_pipe.transform_utterance(utt)
        self.tfidf_model.transform_utterance(utt)
        return self.ec_model.transform_utterance(utt)
    
    def summarize(self, k=10, max_chars=1000, corpus=None):
        self.ec_model.summarize(k, max_chars, corpus)
    
    def set_cluster_names(self, names):
        self.ec_model.set_cluster_names(names)

    def get_terms(self):
        return self.ec_model.get_terms()
    
    def load(self, dirname, model_dirs=None):
        if model_dirs is None:
            model_dirs = ['tfidf_model', 'ec_model']
        
        self.tfidf_model.load(os.path.join(dirname, model_dirs[0]))
        self.ec_model.load(os.path.join(dirname, model_dirs[1]))
        
    def dump(self, dirname):
        
        try:
            os.mkdir(dirname)
        except:
            pass
        self.tfidf_model.dump(os.path.join(dirname, 'tfidf_model'))
        self.ec_model.dump(os.path.join(dirname, 'ec_model'))
        
class DualContextPipeline(Transformer):
    
    def __init__(self, 
        context_fields, output_prefixes, 
        text_field, context_text_field=None,
        wrapper_output_prefix='',
        text_pipe=None, context_text_pipe=None,
        tfidf_params={}, context_tfidf_params=None, share_tfidf_models=True,
        min_terms=0, context_min_terms=None,
        n_svd_dims=25, snip_first_dim=True, n_clusters=8, cluster_on='utts',
        random_state=None, cluster_random_state=None):

        
        self.vect_field = 'col_normed_tfidf'
        self.share_tfidf_models = share_tfidf_models
        
        if share_tfidf_models:
            self.context_vect_field = self.vect_field
        else:
            self.context_vect_field = 'context_col_normed_tfidf'
        
        
        self.text_field = text_field
        if context_text_field is None:
            self.context_text_field = text_field
        else:
            self.context_text_field = context_text_field
        
        if text_pipe is None:
            self.text_pipe = ConvokitPipeline([
                ('text_pipe', TextProcessor(output_field=self.text_field,
                               proc_fn=lambda x: x))
            ])
        self.text_pipe = text_pipe
        self.text_pipe.steps[-1][1].output_field = self.text_field
        
        if context_text_pipe is None:
            self.context_text_pipe = self.text_pipe
        else:
            self.context_text_pipe = context_text_pipe
            self.context_text_pipe.steps[-1][1].output_field = self.context_text_field
        
        self.tfidf_params = tfidf_params
        if context_tfidf_params is None:
            self.context_tfidf_params = tfidf_params
        else:
            self.context_tfidf_params = context_tfidf_params
        
        self.min_terms = min_terms
        if context_min_terms is None:
            self.context_min_terms = min_terms
        else:
            self.context_min_terms = context_min_terms
        
        
        self.dualmodel = DualContextWrapper(
            context_fields=context_fields, output_prefixes=output_prefixes,
            vect_field=self.vect_field,
            context_vect_field=self.context_vect_field,
            wrapper_output_prefix=wrapper_output_prefix,
            n_svd_dims=n_svd_dims, snip_first_dim=snip_first_dim, n_clusters=n_clusters, cluster_on=cluster_on,
            random_state=random_state, cluster_random_state=cluster_random_state)
        
        
        self.tfidf_model = ColNormedTfidfTransformer(
            input_field=self.text_field,
            output_field=self.vect_field, **self.tfidf_params
        )
        if not share_tfidf_models:
            self.context_tfidf_model = ColNormedTfidfTransformer(
                input_field=self.context_text_field,
                output_field=self.context_vect_field,
                **self.context_tfidf_params
            )
        else:
            self.context_tfidf_model = self.tfidf_model
        
        
    def fit(self, corpus, y=None, selector=lambda x: True, context_selector=lambda x: True):
        self.text_pipe.fit_transform(corpus)
        if not self.share_tfidf_models:
            self.context_text_pipe.fit_transform(corpus)
        self.tfidf_model.fit_transform(corpus, selector=selector)
        if not self.share_tfidf_models:
            self.context_tfidf_model.fit_transform(corpus, selector=context_selector)
        self.dualmodel.fit(corpus, 
            selector=lambda x: selector(x)
             and (x.meta.get(self.vect_field + '__n_feats',0) >= self.min_terms),
            context_selector=lambda x: context_selector(x)
             and (x.meta.get(self.context_vect_field + '__n_feats',0) >= self.context_min_terms))
    
    def transform(self, corpus, y=None, selector=lambda x: True):
        _ = self.text_pipe.transform(corpus)
        _ = self.tfidf_model.transform(corpus, selector=selector)
        _ = self.dualmodel.transform(corpus, 
            selector=lambda x: selector(x) 
            and (x.meta.get(self.vect_field + '__n_feats',0) >= self.min_terms))
        return corpus
    
    def transform_utterance(self, utt):
        if isinstance(utt, str):
            utt = Utterance(text=utt, speaker=Speaker()) 
        self.text_pipe.transform_utterance(utt)
        self.tfidf_model.transform_utterance(utt)
        return self.dualmodel.transform_utterance(utt)
    
    def summarize(self, k=10, max_chars=1000, corpus=None):
        self.dualmodel.summarize(k, max_chars, corpus)

    def get_terms(self):
        return self.dualmodel.get_terms()
    
    def load(self, dirname, model_dirs=None):
        if model_dirs is None:
            model_dirs = ['tfidf_model'] + self.dualmodel.output_prefixes
        
        self.tfidf_model.load(os.path.join(dirname, model_dirs[0]))
        self.dualmodel.load(dirname, model_dirs[1:])
    
    def dump(self, dirname):
        self.dualmodel.dump(dirname)
        try:
            os.mkdir(os.path.join(dirname, 'tfidf_model'))
        except:
            pass
        self.tfidf_model.dump(os.path.join(dirname, 'tfidf_model'))