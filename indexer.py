# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:38:58 2014

@author: zzhang
"""
from util import *
import string

#%%
class WordFreq:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

    def __str__(self):
        return self.word + ":" + str(self.freq)

#%%    
class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = [];
        self.index = {}
        self.sect_index = {}
        self.wd_freq_list = []
        self.total_words = 0
        self.num_sections = 0

    def add_msg(self, m):
        self.msgs.append(m)
        
    def get_msg_size(self):
        return len(self.msgs)
        
    def set_sect_begin_end(self, i, start, end):
        self.sect_index[i] = (start, end)
        
    def get_sect(self, i):
        rt = ''
        if i <= len(self.sect_index):
            start = self.sect_index[i][0]
            end = self.sect_index[i][1]
            for i in range(start, end):
                rt += self.msgs[i] + '\n'
        return rt
        
    def add_msg_and_index(self, m):
        self.msgs.append(m)
        self.index_msg(m, len(self.msgs)-1)
        
    def get_msg(self, n):
        return self.msgs[n]
    
    def index_msg(self, m, l):
        words = m.split()
        # remove the following two lines when run real
        if len(words) == 1:
            self.num_sections += 1
        else:
            self.total_words += len(words)
            for wd in words:
                wd = wd.strip()
                wd = word_cleanup(wd)      
                if wd not in self.index:
                    self.index[wd] = [l,]
                else:
                    self.index[wd].append(l)
            
    def build_wf_list(self):
            wf_list = []
            for wd in self.index.keys():
                wf = WordFreq(wd, len(self.index[wd]))
                wf_list.append(wf)
                self.wd_freq_list = sorted(wf_list, \
                    key=lambda wf: wf.freq, \
                    reverse=True)
        
    def print_msg_with_key(self, key):
        if key not in self.index.keys():
            print(key, ': not found!')
            return
        print('KEY: [', key, ']')
        # add logic to change fonts
        for msg_num in self.index[key]:
            msg2 = proc_message(key, self.get_msg(msg_num))
            print (msg_num, ': ', msg2)
        print('+++++++++++++++++++++++++++++++++++\n')
        
    def print_top_freq_word(self, num_tops, msg_too):
        print('+++ top', num_tops, 'words+++++++++++++++')
        for i in range(num_tops):
            wf = self.wd_freq_list[i]
            print(i, '->\t', wf)
            if msg_too == True:
                self.print_msg_with_key(wf.word)
    
    def print_stats(self):
        print('\n+++++++++ stats ++++++++++++')
        print('there are', self.num_sections, 'sections')
        print('a total of', self.total_words, 'unique words')
        print('out of a total of', len(self.index), 'words')
        print('\n')
  
    def search(self, term):
        if (term in self.index.keys()):
            indices = self.index[term]
            msgs = [self.msgs[i] for i in indices]
            ret_msg = ''
            for m in msgs:
                ret_msg = ret_msg + m + '\n'
            return ret_msg
            #return (string.join(msgs,'\n'))
        else:
            return ('')
