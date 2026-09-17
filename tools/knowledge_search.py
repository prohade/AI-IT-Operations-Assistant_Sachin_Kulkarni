import re
from database.database import get_connection

def _tokens(text):
    return set(re.findall(r"[a-zA-Z0-9]+", (text or "").lower()))

def search_knowledge(query: str, limit: int = 3) -> dict:
    if not query or not query.strip():
        return {"success": False, "error": "Search query is required."}
    q = _tokens(query)
    matches = []
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM knowledge_articles").fetchall()
        for row in rows:
            a = dict(row)
            all_text = " ".join([a["category"], a["title"], a["content"], a["keywords"]])
            score = len(q & _tokens(all_text)) + 2 * len(q & _tokens(a["title"] + " " + a["category"]))
            if score > 0:
                a["relevance_score"] = score
                matches.append(a)
        matches.sort(key=lambda x: x["relevance_score"], reverse=True)
        matches = matches[:max(1, limit)]
        return {"success": True, "found": bool(matches), "results": matches}
    except Exception as exc:
        return {"success": False, "error": f"Knowledge search failed: {exc}"}
