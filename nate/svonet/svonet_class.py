"""
This is a MODULE docstring
"""

from .svo import findSVOs
import pandas as pd
from ..utils.mp_helpers import mp
from ..utils.text_helpers import is_ascii
from typing import List, Dict
from .svo_offsets import generate_svo_offsets
from ..edgeburst.burst_mixin import BurstMixin
from ..edgeburst.burst_class import Bursts
from .graph_svo import create_svo_animation, get_giant_component, save_svo_graph
from types import MethodType


def process_svo(sub_tags, obj_tags, doc):
    """
    This is a docstring.
    """
    sentences = [x.string.strip() for x in doc.sents]
    svo_items = [findSVOs(x, sub_tags, obj_tags) for x in doc.sents]

    return (sentences, svo_items)


class SVOnet(BurstMixin):
    """
    This is a docstring.
    """
    def __init__(self, sentences, svo_items, timestamps):
        self.sentences = sentences
        self.svo_items = svo_items
        self.times = timestamps
        self.from_svo = True


    def svo_to_df(self, tidy=True):
        """ 
        This is a docstring.
        """
        df = pd.DataFrame()
        doc_id = []
        sent_id = []
        sent_list_flat = []
        svo_list_flat = []
        time_list_flat = []
        sub_list_flat = []
        verb_list_flat = []
        obj_list_flat = []
        sub_ent_types = []
        obj_ent_types = []
        for i, doc in enumerate(self.sentences):
            for j, sent in enumerate(doc):
                for k, svo_item in enumerate(self.svo_items[i][j][0]):
                    if is_ascii(svo_item[0]) and is_ascii(svo_item[1]) and is_ascii(svo_item[2]):
                        svo_item = (svo_item[0].lower(), svo_item[1].lower(), svo_item[2].lower())                
                        doc_id.append(i)
                        sent_id.append(j)
                        sent_list_flat.append(sent)
                        time_list_flat.append(self.times[i])
                        svo_list_flat.append(svo_item)
                        sub_list_flat.append(svo_item[0])
                        verb_list_flat.append(svo_item[1])
                        obj_list_flat.append(svo_item[2])
                        sub_ent_types.append(self.svo_items[i][j][1][k])
                        obj_ent_types.append(self.svo_items[i][j][2][k])

        df['doc_id'], df['sent_id'], df ['sentence'], df['svo'], df['timestamp'] = doc_id, sent_id, sent_list_flat, svo_list_flat, time_list_flat
        df['subject'], df['sub_type'], df['verb'], df['object'], df['obj_type'] = sub_list_flat, sub_ent_types, verb_list_flat, obj_list_flat, obj_ent_types
        
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        
        if tidy == False:
            #df = df.groupby('svo').agg(lambda x: list(x))
            df = df.groupby('svo')['doc_id', 'timestamp', 'datetime'].agg(list)

        return df
        

    def svo_to_burst(self, minimum_offsets = 20, s = 2, gamma = 1): 
            
        self.offset_dict, self.lookup = generate_svo_offsets(self.svo_items, self.times, minimum_offsets)

        burst_instance = self.burst_detection(s, gamma)

        burst_instance.save_svo_graph = MethodType(save_svo_graph, burst_instance)
        burst_instance.create_svo_animation = MethodType(create_svo_animation, burst_instance)
        burst_instance.get_giant_component = MethodType(get_giant_component, burst_instance)
        
        return burst_instance
