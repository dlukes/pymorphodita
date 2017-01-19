"""An interface to MorphoDiTa tokenizers.

In addition to tokenization, the MorphoDiTa tokenizers perform sentence splitting at the same time.

The easiest way to get started is to import one of the following callables: ``vertical``, ``czech``,
``english`` or ``generic``, and use it like so:

>>> from pymorphodita import tokenizer
>>> for sentence in tokenizer.generic("foo bar baz"):
...     print(sentence)
...
['foo', 'bar', 'baz']

"""
import ufal.morphodita as ufal


class Tokenizer:
    """A wrapper API around the tokenizers offered by MorphoDiTa.

    Usage:

    >>> t = Tokenizer("generic")
    >>> for sentence in t("foo bar baz"):
    ...     print(sentence)
    ...
    ['foo', 'bar', 'baz']

    Available tokenizers (specified by the first parameter to the ``Tokenizer()`` constructor):
    "vertical", "czech", "english", "generic". See the ``new*`` static methods on the MorphoDiTa
    ``tokenizer`` class described at https://ufal.mff.cuni.cz/morphodita/api-reference#tokenizer for
    details.

    """
    def __init__(self, tokenizer_type):
        """Create a new tokenizer instance.

        :param tokenizer_type: Type of the requested tokenizer, depends on the tokenizer
        constructors made available on the ``tokenizer`` class in MorphoDiTa. Typically one of
        "vertical", "czech", "english" and "generic".
        :type tokenizer_constructor_name: str

        """
        constructor = "new" + tokenizer_type.capitalize() + "Tokenizer"
        self._tokenizer = getattr(ufal.Tokenizer, constructor)()
        self._forms = ufal.Forms()
        self._tokens = ufal.TokenRanges()

    def __call__(self, text):
        self._tokenizer.setText(text)
        return self

    def __iter__(self):
        while self._tokenizer.nextSentence(self._forms, self._tokens):
            yield list(self._forms)


vertical = Tokenizer("vertical")
czech = Tokenizer("czech")
english = Tokenizer("english")
generic = Tokenizer("generic")
