# Architecture – ORBIT Beraterprofil Automation

## Agent & Connector Design

| Layer | Name | Count | LLM | Description |
|-------|------|-------|-----|-------------|
| **UI** | Web Upload / REST API | 1 | No | User uploads CV (+ optional photo) |
| **Connector** | CV Parser | 1 | No | PDF/DOCX → plain text, optional image |
| **Agent** | Profil-Extraktions-Agent | 1 | **Yes** | Text → JSON (German, ORBIT rules) |
| **Connector** | PPTX Builder | 1 | No | JSON → fixed `.pptx` template |
| **Orchestrator** | Pipeline (FastAPI) | 1 | No | Chains steps, handles errors |

**Total: 1 Agent + 2 Connectors + 1 Orchestrator** (minimal, production-ready).

Optional future agents (not required for v1):
- **QA-Agent** – checks overflow/alignment before download
- **Translation-only Agent** – if CV is already structured JSON

## Why LLM is required

| Task | Rule-based? | LLM? |
|------|-------------|------|
| PDF/DOCX text extraction | Yes | No |
| EN → DE translation | Hard | **Yes** |
| Domain detection (Telecom/IT/Sales) | Partial | **Yes** |
| Summary in ORBIT tone | No | **Yes** |
| Map skills → 5 tool categories | Partial | **Yes** |
| Fill PPTX placeholders | Yes | No |

**Recommended:** DeepSeek (`deepseek-chat`) for cost; Mistral as fallback.

## Data Flow

```
[CV PDF/DOCX] ──► CV Parser ──► raw text
                                    │
                                    ▼
                          Profil-Agent (LLM)
                          + EXTRACTION_PROMPT.md
                          + BERATERPROFIL_RULES.md
                                    │
                                    ▼
                              JSON schema
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
            PPTX Builder                    API preview JSON
            + template.pptx                 (for review)
                    │
                    ▼
            Beraterprofil.pptx
```

## Template Field Mapping

| JSON field | PPT region |
|------------|------------|
| `title_domain` | Title: `Beraterprofil – {domain}` |
| `position` | Header position box |
| `schwerpunkte` | Header focus line |
| `summary` | Summary paragraph |
| `kompetenzen[]` | Left column bullets |
| `relevante_erfahrungen[]` | Middle column `Label: text` |
| `ausbildung_karriere[]` | Right top bullets |
| `abschluss_zertifikate[]` | Right bottom bullets |
| `tool_kenntnisse.*` | Bottom left categories |
| photo bytes | Left photo placeholder |

## Deployment Path

1. **Localhost** – `uvicorn app.main:app --port 8000`
2. **Docker** – single container with template + env secrets
3. **Azure / VM** – behind HTTPS, optional Entra ID auth

## Security Notes

- API keys in `.env` only (never commit)
- CVs stored temporarily in `uploads/` – add retention policy for production
- LLM receives CV text only; no PII logging in production
