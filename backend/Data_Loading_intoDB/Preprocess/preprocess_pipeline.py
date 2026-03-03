# going through all the methods defined in this folder in order

from Data_Cleaner import TextCleaner
from Dedup_Algo import DedupAlgo
from PII import PIIRemover
from Quality_filter import TokenCounter, PerplexityFilter


class PreprocessPipeline:

    def __init__(self):
        self.cleaner = TextCleaner()
        self.dedup = DedupAlgo()
        self.pii_filter = PIIRemover()
        self.token_filter = TokenCounter()
        #self.ppl_filter = PerplexityFilter() very expensive

    def process(self, text: str):

        text = self.cleaner.clean(text)
        if not text:
            return None

        text = self.pii_filter.remove(text)

        if not self.token_filter.is_valid_length(text):
            return None

        if self.dedup.exact_and_minhash_dedup(text):
            return None

        #if self.ppl_filter.is_gibberish(text):
           # return None

        return text