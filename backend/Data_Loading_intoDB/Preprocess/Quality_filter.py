#counting tokens, calculating perplexity, and removing 乱码, checking out image clearness(later)

#token control to control cost

import torch
import tiktoken
#需要用到模型api

class PerplexityFilter:
    def __init__(self, model_name = ""):
        a = 4
    
    def compute_perplexity(self, text:str) ->float:
        encodings = self.tokenizer(text, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model(**encodings, labels = encodings["input_ids"])
            loss = outputs.loss
        return torch.exp(loss).item()
    
    def is_gibberish(self, text: str, threshold=100) -> bool:
        ppl = self.compute_perplexity(text)
        return ppl > threshold


class TokenCounter:
    def __init__(self, model_name=""):
        self.encoder = tiktoken.encoding_for_model(model_name)

    def count_tokens(self, text: str) -> int:
        tokens = self.encoder.encode(text)
        return len(tokens)

    def is_valid_length(self, text: str, min_tokens=5, max_tokens=2048) -> bool:
        n = self.count_tokens(text)
        return min_tokens <= n <= max_tokens