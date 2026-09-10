\
from __future__ import annotations
from pathlib import Path
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class EngineeringKnowledgeIndex:
    """Persistent local knowledge retrieval. Generic knowledge is advisory, never project authority."""
    def __init__(self, index_dir: str | Path):
        self.index_dir=Path(index_dir); self.index_dir.mkdir(parents=True, exist_ok=True)
        self.bundle_path=self.index_dir/'engineering_knowledge_tfidf.joblib'
        self.vectorizer=None; self.matrix=None; self.chunks=[]
        if self.bundle_path.exists():
            b=joblib.load(self.bundle_path)
            self.vectorizer=b['vectorizer']; self.matrix=b['matrix']; self.chunks=b['chunks']

    @staticmethod
    def _chunks(text: str, source: str) -> list[dict]:
        lines=text.splitlines(); chunks=[]; heading=''; buf=[]; start=1
        def flush(end_line):
            nonlocal buf,start
            body='\n'.join(buf).strip()
            if body:
                chunks.append({'source':source,'heading':heading,'start_line':start,'end_line':end_line,'text':body})
            buf=[]
        for i,line in enumerate(lines,1):
            if re.match(r'^#{1,6}\s+',line):
                flush(i-1); heading=line.lstrip('#').strip(); start=i
                buf=[line]
            else:
                if not buf: start=i
                buf.append(line)
                if sum(len(x) for x in buf) > 2200:
                    flush(i); start=i+1
        flush(len(lines))
        return chunks

    def build(self, paths: list[str | Path]) -> dict:
        chunks=[]
        for p0 in paths:
            p=Path(p0)
            chunks.extend(self._chunks(p.read_text(encoding='utf-8', errors='ignore'), p.name))
        corpus=[c['text'] for c in chunks]
        self.vectorizer=TfidfVectorizer(lowercase=True, ngram_range=(1,2), min_df=1, sublinear_tf=True, max_features=80000)
        self.matrix=self.vectorizer.fit_transform(corpus)
        self.chunks=chunks
        joblib.dump({'vectorizer':self.vectorizer,'matrix':self.matrix,'chunks':self.chunks},self.bundle_path)
        return {'status':'BUILT','chunks':len(chunks),'sources':sorted({c['source'] for c in chunks})}

    def search(self, query: str, k: int = 8) -> list[dict]:
        if self.vectorizer is None or self.matrix is None:
            return []
        q=self.vectorizer.transform([query])
        scores=cosine_similarity(q,self.matrix)[0]
        order=scores.argsort()[::-1][:max(1,k)]
        out=[]
        for idx in order:
            if scores[idx] <= 0: continue
            c=dict(self.chunks[int(idx)]); c['score']=float(scores[idx]); out.append(c)
        return out
