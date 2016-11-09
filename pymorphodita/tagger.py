from . import log

from collections import namedtuple
from collections.abc import Sequence
import ufal.morphodita as ufal

Token = namedtuple("Token", "word lemma tag")


class Tagger:
    """A MorphoDiTa morphological tagger and lemmatizer associated with particular
    set of tagging models.

    """
    _NO_TOKENIZER = ("No tokenizer defined for tagger {!r}! Please provide "
                     "pre-tokenized and sentence-split input.")

    def __init__(self, tagger, guesser=False):
        """Create a ``Tagger`` object.

        :param tagger: Path to the pre-compiled tagging models.
        :type tagger: str
        :param guesser: Whether or not to use a guesser with this tagger.
        :type guesser: bool

        """
        self._tpath = tagger
        log.info("Loading tagger.")
        self._tagger = ufal.Tagger.load(tagger)
        if self._tagger is None:
            raise RuntimeError("Unable to load tagger from {!r}!".format(tagger))
        self._forms = ufal.Forms()
        self._lemmas = ufal.TaggedLemmas()
        self._tokens = ufal.TokenRanges()
        self._tokenizer = self._tagger.newTokenizer()
        if self._tokenizer is None:
            log.warn(self._NO_TOKENIZER.format(tagger))
        self._vtokenizer = ufal.Tokenizer_newVerticalTokenizer()

    def tag(self, text, sents=False, guesser=False):
        """Tag text.

        If ``text`` is a string, sentence-split, tokenize and tag that string.
        If it's a sequence of sequences (typically a list of lists, and with
        the exception of a list of strings), then take each nested sequence as
        a separate sentence and tag it, honoring the provided sentence
        boundaries and tokenization.

        :param text: Input text.
        :type text: Either str (tokenization is left to the tagger) or sequence
        of sequences (not strings!) of str, representing individual sentences.
        :param sents: Whether to signal sentence boundaries by outputting a
        sequence of lists (sentences).
        :type sents: bool
        :param guesser: Whether to use the morphological guesser provided with
        the tagger (if available).
        :type guesser: bool

        >>> list(t.tag("Je zima. Bude sněžit."))
        [Token(word='Je', lemma='být', tag='VB-S---3P-AA---'),
         Token(word='zima', lemma='zima-1', tag='NNFS1-----A----'),
         Token(word='.', lemma='.', tag='Z:-------------'),
         Token(word='Bude', lemma='být', tag='VB-S---3F-AA---'),
         Token(word='sněžit', lemma='sněžit_:T', tag='Vf--------A----'),
         Token(word='.', lemma='.', tag='Z:-------------')]

        >>> list(t.tag([['Je', 'zima', '.'], ['Bude', 'sněžit', '.']]))
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

        """
        if isinstance(text, str):
            yield from self._tag_untokenized(text, sents, guesser)
        elif (isinstance(text, Sequence)
              and len(text) > 0
              and isinstance(text[0], Sequence)
              and not isinstance(text[0], str)):
            yield from self._tag_tokenized(text, sents, guesser)
        else:
            raise TypeError(
                "Please provide a str or a sequence of sequences (not "
                "strings!) of str as the ``text`` parameter.")

    def _tag_untokenized(self, text, sents, guesser):
        if self._tokenizer is None:
            raise RuntimeError(self._NO_TOKENIZER.format(self._tpath))
        yield from self._tag(text, self._tokenizer, sents, guesser)

    def _tag_tokenized(self, text, sents, guesser):
        for sent in text:
            yield from self._tag(
                "\n".join(sent), self._vtokenizer, sents, guesser)

    def _tag(self, text, tokenizer, sents, guesser):
        tagger, forms, lemmas, tokens = (self._tagger, self._forms,
                                         self._lemmas, self._tokens)
        tokenizer.setText(text)
        while tokenizer.nextSentence(forms, tokens):
            tagger.tag(forms, lemmas, guesser)
            s = []
            for i in range(len(lemmas)):
                lemma = lemmas[i]
                t = tokens[i]
                word = text[t.start : t.start + t.length]
                token = Token(word, lemma.lemma, lemma.tag)
                if sents:
                    s.append(token)
                else:
                    yield token
            if sents:
                yield s
