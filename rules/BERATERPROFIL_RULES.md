# Beraterprofil – Extrahierte Regeln (ORBIT IT-Solutions)

Diese Regeln wurden aus der Vorlage `Beraterprofil – Funknetzplanung.pptx` und Beispiel-Outputs abgeleitet.

## 1. Dokumentformat

| Eigenschaft | Wert |
|---|---|
| Format | PowerPoint (.pptx), **eine Folie** |
| Sprache | **Deutsch** (Fachbegriffe/Produktnamen dürfen Englisch bleiben) |
| Layout | Festes ORBIT-Template – **keine** Layout-, Positions- oder Schriftänderungen |
| Ausrichtung | Linksbündig in Inhaltsfeldern; Überschriften wie im Template |

## 2. Folienstruktur (strikt)

```
┌─────────────────────────────────────────────────────────────────┐
│ Beraterprofil – {Domäne}                                        │
├──────────┬──────────────────────────────────────────────────────┤
│  Foto    │ Position: {Rolle}                                    │
│          │ Schwerpunkte: {kommagetrennt, max. 3–5 Themen}       │
│          │ Summary: {2–4 Sätze Fließtext}                       │
├──────────┴──────────────────────────────────────────────────────┤
│ Kompetenzen │ Relevante Erfahrungen/Projekte │ Ausbildung/Karriere│
│ (Bullets)   │ (Label: Beschreibung)          │ (Bullets)          │
├─────────────┴────────────────────────────────┴───────────────────┤
│ Tool-Kenntnisse (Kategorien mit fettem Label + Wert) │ Abschluss/Zertifikate│
└─────────────────────────────────────────────────────────────────┘
```

## 3. Feldregeln

### 3.1 Titel
- Format: `Beraterprofil – {Domäne}`
- Domäne = **ein** prägnanter Fachbereich auf Deutsch, **aus dem CV abgeleitet** (nicht immer Funknetzplanung):
  - Telecom/RF → `Funknetzplanung`, `Mobilfunk`, `Telekommunikation`
  - IT/Cloud → `Cloud & Infrastruktur`, `IT-Security`, `Modern Workplace`
  - Software → `Software-Entwicklung`, `Business Applications`
  - Sales/CRM → `Vertrieb`, `CRM`
  - Dokumentation → `Technische Dokumentation`
  - PM → `Projektmanagement`

### 3.2 Position
- Kurze Rollenbezeichnung (1–4 Wörter), z. B. `Consultant`, `Senior Consultant`, `Solution Architect`
- Kein Firmenname in der Position

### 3.3 Schwerpunkte
- Kommagetrennte Liste, **3–5** Schwerpunkte
- Substantiv/Verb-Phrasen, kein Satz
- Beispiel: `Funknetzplanung, Optimierung und Deployment`

### 3.4 Summary
- **2–4 Sätze** professioneller Fließtext auf Deutsch
- Fokus: Erfahrung, Domäne, Mehrwert für ORBIT-Kunden (Mittelstand, Projekte, Hands-on)
- Keine Ich-Form; unpersönlich/professionell („Erfahrener … mit …“)
- Länge: ca. 350–600 Zeichen

### 3.5 Kompetenzen (linke Spalte, Bullets)
- **5–8** kurze Bullet-Punkte (Level 1)
- Je Punkt: max. 8–10 Wörter
- Oberbegriffe der Fähigkeiten, keine langen Erklärungen
- Beispiele: `RAN-Planung und Optimierung`, `Projektmanagement`, `Kunden- und Stakeholder-Management`

### 3.6 Relevante Erfahrungen / Projekte (Mitte)
- **4–6** Einträge im Format: `{Fett-Label}: {Beschreibung}`
- Label = Themenblock (z. B. `Netzwerkplanung und Kapazitätsmanagement`)
- Beschreibung = 1 Satz mit konkreten Tätigkeiten
- ORBIT-/Kundenkontext bevorzugen, wenn im CV vorhanden

### 3.7 Ausbildung / Karriere (rechts oben)
- **Beruflicher Werdegang** – keine Abschlüsse!
- **3–4** Bullets zu internationalen Einsätzen, Projekten, Kunden, Ländern, Vendor-Erfahrung
- Beispiele aus Vorlage:
  - „Internationale Einsätze als Regional Lead …“
  - „Projekterfahrung in Pakistan, Südafrika, UAE …“
  - „Zusammenarbeit mit internationalen Kunden wie MTN, Telenor …“
- **NICHT:** Bachelor, Master, SSC, University, Jahreszahlen von Abschlüssen

### 3.8 Abschluss / Zertifikate (rechts unten)
- Format: `{Jahr}, {Abschluss/Zertifikat}, {Institution}`
- Neueste zuerst
- **3–8** Einträge (Abschlüsse, Zertifikate, relevante Schulungen)
- Beispiel: `2018, Master of Science in Telekommunikationstechnik, Universität Bonn`

### 3.9 Tool-Kenntnisse (unten links)
Feste Kategorien (Labels **fett**, Werte normal):
1. `OSS / Command Management`
2. `Statistik und Analyse`
3. `Planung und Optimierung`
4. `Drive Test und Post-Processing`
5. `Mapping`

- Pro Kategorie: kommagetrennte Tools/Technologien aus dem CV
- Wenn Kategorie nicht zutrifft (z. B. Sales-CV): passende Tools/Plattformen eintragen oder Feld leer lassen (`: `)
- Bei IT-CVs: Kategorien beibehalten, Inhalt anpassen (z. B. Planung → `Azure, Terraform, …`)

### 3.10 Foto
- Profilbild links oben, wenn im CV/Upload vorhanden
- Sonst Platzhalter im Template belassen

## 4. Domänen-agnostische Anpassung (ORBIT-Kontext)

ORBIT deckt ab: KI, Security, Zero Trust, ERP, CRM, BI, Software-Entwicklung, Modern Workplace, Cloud, Backup, IT-Support, Telekom/Funknetz.

**Regel:** Section-Überschriften im Template **nie ändern** – nur Inhalte domänenspezifisch füllen.

| CV-Typ | Titel-Domäne | Kompetenzen-Fokus | Tool-Kategorien füllen mit |
|---|---|---|---|
| RF/Telecom | Funknetzplanung | RAN, KPI, Rollout | OSS, ATOLL, TEMS, … |
| IT/Cloud | Cloud & Infrastruktur | Azure, Migration, Betrieb | Azure, M365, Terraform, … |
| Security | IT-Security | NIS2, MDR, Zero Trust | SIEM, Defender, … |
| Software | Software-Entwicklung | .NET, APIs, Agile | IDE, Git, CI/CD, … |
| Sales/CRM | CRM / Vertrieb | Pipeline, Akquise | Salesforce, Dynamics, … |
| Dokumentation | Technische Dokumentation | Redaktion, Standards | Confluence, MadCap, … |

## 5. Qualitätsregeln

- Alles auf **Deutsch** (Übersetzung aus englischen CVs)
- **One-Pager:** Feste Zeichenlimits pro Feld (siehe `app/services/content_fit.py`)
- Keine erfundenen Fakten – nur aus CV ableiten
- Duplikate vermeiden zwischen Kompetenzen und Schwerpunkten
- Konsistente Groß-/Kleinschreibung bei Produktnamen
- `relevante_erfahrungen.label` = **Thema**, nicht Jobtitel
- `relevante_erfahrungen.beschreibung` = **Stichworte** (wie Vorlage), kein langer Satz

### One-Pager Zeichenlimits (gemessen aus Vorlage)

| Feld | Max |
|------|-----|
| title_domain | 28 Zeichen |
| position | 22 Zeichen |
| schwerpunkte | 50 Zeichen (max 3 Themen) |
| summary | 400 Zeichen (2–3 Sätze) |
| kompetenzen | 7 Bullets × 48 Zeichen |
| relevante_erfahrungen | 5 × (Label 40 + Beschreibung 58) |
| ausbildung_karriere | 4 × 72 Zeichen |
| abschluss_zertifikate | 5 × 78 Zeichen |
| tool_kenntnisse | 52 Zeichen pro Kategorie |

### Foto
- **Separater Upload** über UI/API – wird nicht aus CV extrahiert

## 6. JSON-Schema für LLM-Output

Siehe `app/schemas/profile.py` – das LLM muss exakt dieses Schema liefern.
