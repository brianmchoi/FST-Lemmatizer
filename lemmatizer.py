"""

F20 11-411 NLP Assignment 2
Lemmatizer Starter Code
Kinjal Jain - 1 Sept 20

The framework for the lemmatizer is provided. Your task is to create the FSTs
that this code uses to construct the final lemmatizer FST. After you build the FST, you
can uncomment the code that reads the FST from the file.

You should create the FSTs as text files, but feel free to use python scripts
to generate text files in order to handle cases like vowels and consonants. Feel
free to change any of the given code for your FST.

We have provided helper functions to use compose on FSTs, read FSTs from files,
and run the FST on words.

When you submit to Gradescope, be sure you have no print statements inside the Lemmatizer class.

"""

import pywrapfst as fst
from fststr import fststr
import copy

class Lemmatizer():
  
  # TODO: Implement the in vocab FST
  def get_in_vocab_fst(self):
    raise NotImplementedError

  def __init__(self):
    
    # TODO: Implement the OOV FSTs in the text files
    # Reading a FST from an empty file will throw an error

    # Pre Process: Add <#> to end of word
    pre_process_fst = self.get_compiler_from_file_name('fsts/pre-process.txt')

    # Get in vocabulary FST
    in_vocab_fst = self.get_in_vocab_fst()

    # Get out of vocabulary FST
    # General FST to add morpheme boundary to: ed, s, en, ing
    general_fst = self.get_compiler_from_file_name('fsts/general-morph.txt')
    general_fst = general_fst.invert()

    # Allomorphic rules:
    # Feel free to implement rules in reverse and then call .invert() on the FST
    e_insertion_fst = self.get_compiler_from_file_name('fsts/e-insertion.txt')
    consonant_doubling_fst = self.get_compiler_from_file_name('fsts/consonant-doubling.txt')
    e_deletion_fst = self.get_compiler_from_file_name('fsts/silent-e-deletion.txt')
    y_replacement_fst = self.get_compiler_from_file_name('fsts/y-replacement.txt')
    k_insertion_fst = self.get_compiler_from_file_name('fsts/k-insertion.txt')
    
    # OPTIONAL: If you implemented the rules for some FSTs in reverse, call .invert() on them by uncommenting below.
    # consonant_doubling_fst = consonant_doubling_fst.invert()
    # e_deletion_fst = e_deletion_fst.invert()
    # e_insertion_fst = e_insertion_fst.invert()
    # y_replacement_fst = y_replacement_fst.invert()
    # k_insertion_fst = k_insertion_fst.invert()

    # Post Process: Remove suffixes
    post_process_fst = self.get_compiler_from_file_name('fsts/post-process.txt')

    # Assemble final FST
    # use FST operations on your FSTs to create the result FST
    allomorphic_fst = consonant_doubling_fst.union(e_deletion_fst).union(e_insertion_fst).union(y_replacement_fst).union(k_insertion_fst)
    oov_fst = self.compose_fst(general_fst, allomorphic_fst)
    oov_fst = self.compose_fst(oov_fst, post_process_fst)

    in_vocab_fst.union(oov_fst)
    self.res_fst = in_vocab_fst
    self.res_fst = self.compose_fst(pre_process_fst, self.res_fst)

    # self.res_fst = e_insertion_fst
    self.inverted_res_fst = copy.deepcopy(self.res_fst).invert()
  
  # Get FST from file_name
  def get_compiler_from_file_name(self, file_name):
    st = fststr.symbols_table_from_alphabet(fststr.EN_SYMB)
    compiler = fst.Compiler(isymbols=st, osymbols=st, keep_isymbols=True, keep_osymbols=True)
    in_file = open(file_name)
    fst_file = in_file.read()
    print(fst_file, file=compiler)
    c = compiler.compile()
    fststr.expand_other_symbols(c)
    in_file.close()
    return c
  
  # Composes fsts such that fst_a is executed first, and output is used as input for fst_b
  # output = fst_b(fst_a(input))
  def compose_fst(self, fst_a, fst_b):
    return fst.compose(fst_a.arcsort(sort_type="olabel"), fst_b.arcsort(sort_type="ilabel"))

  # Run FST on input word
  def run_fst(self, in_word, compiler):
    return fststr.apply(in_word, compiler)

  def lemmatize(self, input_word):
    out = list(set(self.run_fst(input_word, self.res_fst)))
    return out
    
  def delemmatize(self, input_word):
    return list(set(self.run_fst(input_word, self.inverted_res_fst)))


if __name__ == '__main__':
  L = Lemmatizer()
  print(L.lemmatize('squigging'))
  print(L.delemmatize('squig+Guess'))

  # test e-insertion only
  e_insertion_fst = L.get_compiler_from_file_name('fsts/e-insertion.txt')
  # e_insertion_fst.invert()  # uncomment this if you implemented the inverted FST
  print(L.run_fst('foxe<^>s<#>', e_insertion_fst))
