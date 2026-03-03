# 好像似乎MinHash并不是很好的选择？

#提供both exact match and min hash

from datasketch import MinHash, MinHashLSH
import jieba # support chinese


class DedupAlgo:
    
    def __init__(self, threshold = 0.8, num_perm = 128, ngram = 3):
        self.seen_exact = set()
        self.lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
        self.num_perm = num_perm
        self.counter = 0       # threshold: 相似度阈值（0~1） num_perm: hash函数数量（越大越准但越慢）

        #exact dedup
    
    def exact_duplicate(self, text: str)-> bool:
        if text in self.seen_exact:
            return True
        self.seen_exact.add(text)
        return False
    
    def _get_ngrams(self, text: str):
        text = text.strip()

        if len(text) < self.ngram:
            return [text]   # fallback

        return [text[i:i+self.ngram] for i in range(len(text)-self.ngram+1)]

    # Near duplicate
    def minHash_dedup(self, text: str) -> bool:
        m = MinHash(num_perm=self.num_perm)

        for gram in self._get_ngrams(text):
            m.update(gram.encode("utf8"))

        result = self.lsh.query(m)
        if result:
            return True

        self.lsh.insert(str(self.counter), m)
        self.counter += 1
        return False
    
    def exact_and_minhash_dedup(self, text: str) -> bool:
        if self.exact_duplicate(text):
            return True
        return self.minHash_dedup(text)