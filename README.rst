============
PyMorphoDiTa
============

A slightly more (newbie) user friendly but also probably somewhat less efficient
wrapper around the default Swig-generated Python bindings for the
`MorphoDiTa<https://github.com/ufal/morphodita>`_. morphological tagging and
lemmatization framework.

The target audience are:

- beginner programmers interested in NLP
- seasoned programmers who want to use MorphoDiTa through a more Pythonic
  interface, without having to dig into the `API
  reference<http://ufal.mff.cuni.cz/morphodita/api-reference>`_ and the
  `examples<https://github.com/ufal/morphodita/tree/master/bindings/python/examples>`_,
  and who are not too worried about a possible performance hit as compared with
  full manual control

Pre-trained tagging models which can be used with (Py)MorphoDiTa can be found
`here<http://ufal.mff.cuni.cz/morphodita#language_models>`_. Currently, Czech
and English models are available. **Please respect their CC BY-NC-SA 3.0
license!**

At the moment, only a subset of the functionality offered by the MorphoDiTa API
is available through PyMorphoDiTa (tagging features).

Installation
============

.. code-block:: bash

   $ pip3 install git+https://github.com/dlukes/pymorphodita

Usage
=====

Initialize a new tagger::

   >>> from pymorphodita import Tagger
   >>> t = Tagger("path/to/czech-morfflex-pdt-160310.tagger")

Sentence split, tokenize, tag and lemmatize a text represented as a string::

   >>> list(t.tag("Je zima. Bude sněžit."))
   [Token(word='Je', lemma='být', tag='VB-S---3P-AA---'),
     Token(word='zima', lemma='zima-1', tag='NNFS1-----A----'),
     Token(word='.', lemma='.', tag='Z:-------------'),
     Token(word='Bude', lemma='být', tag='VB-S---3F-AA---'),
     Token(word='sněžit', lemma='sněžit_:T', tag='Vf--------A----'),
     Token(word='.', lemma='.', tag='Z:-------------')]
   >>> list(t.tag("Je zima. Bude sněžit.", sents=True))
   [[Token(word='Je', lemma='být', tag='VB-S---3P-AA---'),
     Token(word='zima', lemma='zima-1', tag='NNFS1-----A----'),
     Token(word='.', lemma='.', tag='Z:-------------')],
   [Token(word='Bude', lemma='být', tag='VB-S---3F-AA---'),
     Token(word='sněžit', lemma='sněžit_:T', tag='Vf--------A----'),
     Token(word='.', lemma='.', tag='Z:-------------')]]

Tag and lemmatize an already sentence-split and tokenized piece of text,
represented as a sequence of sequences of strings::

   >>> list(t.tag([['Je', 'zima', '.'], ['Bude', 'sněžit', '.']]))
   [Token(word='Je', lemma='být', tag='VB-S---3P-AA---'),
     Token(word='zima', lemma='zima-1', tag='NNFS1-----A----'),
     Token(word='.', lemma='.', tag='Z:-------------'),
     Token(word='Bude', lemma='být', tag='VB-S---3F-AA---'),
     Token(word='sněžit', lemma='sněžit_:T', tag='Vf--------A----'),
     Token(word='.', lemma='.', tag='Z:-------------')]

Head over to the `API docs<>`_ for more details.

Requirements
============

Dependencies are automatically satisfied using ``setuptools``. Built and tested
under Python 3.5.2. Prior versions of Python3 might also work.

License
=======

Copyright © 2016 `ÚČNK <http://korpus.cz>`_/David Lukeš

Distributed under the `GNU General Public License v3
<http://www.gnu.org/licenses/gpl-3.0.en.html>`_.
