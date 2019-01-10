import re
from nltk import tokenize

from orangecontrib.text.misc import wait_nltk_data

import jieba
import jieba.analyse

__all__ = ['BaseTokenizer', 'WordPunctTokenizer', 'PunktSentenceTokenizer',
           'RegexpTokenizer', 'WhitespaceTokenizer', 'TweetTokenizer']


class BaseTokenizer:
    """ Breaks a string into sequence of tokens. """
    tokenizer = NotImplemented
    name = 'Tokenizer'

    def __call__(self, sent):
        if isinstance(sent, str):
            return self.tokenize(sent)
        return self.tokenize_sents(sent)

    def tokenize(self, string):
        return list(filter(lambda x: x != '', self.tokenizer.tokenize(string)))

    def tokenize_sents(self, strings):
        return [self.tokenize(string) for string in strings]

    def __str__(self):
        return self.name

    def on_change(self):
        pass

    def set_up(self):
        """ A method for setting filters up before every __call__. """
        pass

    def tear_down(self):
        """ A method for cleaning up after every __call__. """
        pass


class WordPunctTokenizer(BaseTokenizer):
    """ Split by words and (keep) punctuation. """
    tokenizer = tokenize.WordPunctTokenizer()
    name = '分词'

class ChineseWordSegmenter(BaseTokenizer):
    """ 郝佳添加中文分词模块 """
    def tokenize(self, string):
        print("执行：ChineseWordSegmenter")
        
        print(list(filter(lambda x: x != '', jieba.cut(string))))
        return list(filter(lambda x: x != '', jieba.cut(string)))
    name = '中文分词'

class PunktSentenceTokenizer(BaseTokenizer):
    """ Split by full-stop, keeping entire sentences. """
    tokenizer = tokenize.PunktSentenceTokenizer()
    name = '分句'

    @wait_nltk_data
    def __init__(self):
        super().__init__()


class WhitespaceTokenizer(BaseTokenizer):
    """ Split only by whitespace. """
    tokenizer = tokenize.WhitespaceTokenizer()
    name = '空格'


class RegexpTokenizer(BaseTokenizer):
    """ Split by regular expression, default keeps only words. """
    name = '正则表达式'

    def __init__(self, pattern=r'\w+'):
        self._pattern = pattern
        # Compiled Regexes are NOT deepcopy-able and hence to make Corpus deepcopy-able
        # we cannot store then (due to Corpus also storing used_preprocessor for BoW compute values).
        # To bypass the problem regex is compiled before every __call__ and discarded right after.
        self.tokenizer = None
        self.set_up()

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value
        self.set_up()
        self.on_change()

    def __str__(self):
        return '{} ({})'.format(self.name, self.pattern)

    @staticmethod
    def validate_regexp(regexp):
        try:
            re.compile(regexp)
            return True
        except re.error:
            return False

    def set_up(self):
        self.tokenizer = tokenize.RegexpTokenizer(self.pattern)

    def tear_down(self):
        self.tokenizer = None


class TweetTokenizer(BaseTokenizer):
    """ Pre-trained tokenizer for tweets. """
    tokenizer = tokenize.TweetTokenizer()
    name = 'Tweet'
