from __future__ import annotations

import math, re
from collections import Counter
from acia.models.schemas import CodeChunk

TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]+")

def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN.findall(text)]


def bm25_search(query: str, chunks: list[CodeChunk], limit: int = 8) -> list[CodeChunk]:
    q = tokenize(query)
    docs = [tokenize(c.content + " " + c.file_path + " " + (c.symbol or "")) for c in chunks]
    df = Counter(t for doc in docs for t in set(doc)); avgdl = sum(map(len, docs)) / max(len(docs), 1)
    scores = []
    for chunk, doc in zip(chunks, docs):
        counts = Counter(doc); score = 0.0
        for term in q:
            if not counts[term]: continue
            idf = math.log(1 + (len(docs) - df[term] + 0.5) / (df[term] + 0.5))
            score += idf * counts[term] * 2.2 / (counts[term] + 1.2 * (1 - 0.75 + 0.75 * len(doc) / max(avgdl, 1)))
        scores.append((score, chunk))
    return [c for score, c in sorted(scores, key=lambda x: x[0], reverse=True)[:limit] if score > 0]
