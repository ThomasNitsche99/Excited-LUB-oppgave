# 🎓📊 Uthenting av Obligatoriske Emner

Denne mappen inneholder kode for å hente ut **obligatoriske emner** fra nettsider for ulike norske universiteter ved hjelp av [Firecrawl](https://firecrawl.dev).

## Innholdsfortegnelse

- [📌 Hva gjør denne koden?](#hva-gjør-denne-koden)
- [⚙️ Oppsett](#oppsett)
- [🚀 Hvordan bruke skriptene](#hvordan-bruke-skriptene)
- [🔍 Evaluering av prompts](#evaluering-av-prompts)
- [📁 Filstruktur](#filstruktur)
- [🧾 Krav til avhengigheter](#krav-til-avhengigheter)
- [⚠️ Begrensninger og kjente problemer](#begrensninger-og-kjente-problemer)

---

## Hva gjør denne koden?

- Leser `config_mandatory.json` som inneholder universiteter, studieprogram og lenker.
- For hvert studieprogram:
  - Tester alle definerte prompts én og én.
  - Lager én "superprompt" som kombinerer alle.
  - Henter ut flest mulig _obligatoriske emner_ ved å sammenligne alle resultatene.
- Skriver resultatet til CSV og Excel.

---

## Oppsett

1. Sørg for at du har en `.env`-fil i rotmappen:

```env
FIRECRAWL_API_KEY=din_api_nøkkel
```

2. Installer nødvendige avhengigheter:

```bash
pip install -r requirements.txt
```

---

## Hvordan bruke skriptene

### For alle skoler

Kjør `subjects_outcomes.ipynb` for å hente ut obligatoriske emner fra alle definerte skoler og studieprogram.

### For én skole

Kjør `subjects_outcomes_single.ipynb` for å hente ut obligatoriske emner fra én spesifikk skole. Endre parametrene i notebooken for å velge skole og studieprogram.

### Spesielle tilfeller

- For NTNU: Bruk `ntnu_subjects_selenium.ipynb`
- For USN: Bruk `usn_subjects_selenium.ipynb` eller `new_usn_subjects_playwright.ipynb`

---

## Evaluering av prompts

Koden evaluerer automatisk ulike prompts for hvert studieprogram og velger den som gir best resultat. Dette gjøres ved å:

1. Teste hver prompt individuelt
2. Kombinere alle prompts til én "superprompt"
3. Velge den strategien som gir flest obligatoriske emner

Resultatene lagres i `Mandatory_subjects_best_prompts.csv` med informasjon om hvilken prompt-strategi som ga best resultat.

---

## Filstruktur

| Fil                                 | Beskrivelse                                            |
| ----------------------------------- | ------------------------------------------------------ |
| `config_mandatory.json`             | Konfigurasjonsfil med skoler, studieprogram og prompts |
| `subjects_outcomes.ipynb`           | Hovednotebook for uthenting fra alle skoler            |
| `subjects_outcomes_single.ipynb`    | Notebook for uthenting fra én skole                    |
| `ntnu_subjects_selenium.ipynb`      | Spesialhåndtering for NTNU                             |
| `usn_subjects_selenium.ipynb`       | Spesialhåndtering for USN (Selenium)                   |
| `new_usn_subjects_playwright.ipynb` | Spesialhåndtering for USN (Playwright)                 |
| `firecrawl_app.py`                  | Firecrawl applikasjonskode                             |
| `utils/`                            | Hjelpefunksjoner                                       |

---

## Krav til avhengigheter

- Python 3.8+
- firecrawl
- pandas
- selenium (for NTNU og USN)
- playwright (for USN)
- python-dotenv

---

## Begrensninger og kjente problemer

- Noen skoler (f.eks. NTNU og USN) krever spesialhåndtering på grunn av deres nettsidestruktur
- PDF-baserte studieplaner (f.eks. fra UIT og Kristiania) kan være vanskelige å parse
- Noen skoler oppdaterer sine nettsider regelmessig, som kan påvirke uthentingen
- Shadow DOM elementer (spesielt hos USN) kan være utfordrende å håndtere

For å håndtere disse utfordringene, bruker vi ulike strategier for ulike skoler og har implementert flere fallback-mekanismer.
