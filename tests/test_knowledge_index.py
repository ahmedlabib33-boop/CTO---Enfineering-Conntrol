\
from pathlib import Path
from app.services.ml.knowledge_index import EngineeringKnowledgeIndex

def test_knowledge_index(tmp_path):
    src=tmp_path/'kb.md'
    src.write_text('# Plumbing\nMaintain drainage slope and invert.\n\n# Structural\nOpenings require structural review.',encoding='utf-8')
    idx=EngineeringKnowledgeIndex(tmp_path/'idx')
    b=idx.build([src])
    assert b['chunks'] >= 2
    r=idx.search('drainage slope plumbing',3)
    assert r and 'Plumbing' in r[0]['text']
