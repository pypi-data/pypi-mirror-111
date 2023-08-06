from abc import abstractmethod


class BaseTokenizer:

    """
    The abstract Tokenizer class.
    """

    NAME = 'BaseTokenizer'

    @staticmethod
    @abstractmethod
    def tokenize(s):
        """
        Splits a string into tokens.

        Parameters
        ----------
        s : str
            The string to tokenize

        Returns
        -------
        list(str)
            A list of tokens
        """
        pass
