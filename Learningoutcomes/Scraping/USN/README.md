# USN LUB Scraping

Denne mappen inneholder logikken for å skrape USN-nettstedene for å hente ut læringsutbyttebeskrivelser (LUB) fra ulike studieretninger.

## Oversikt

Hovedklassen som er ansvarlig for skrapelogikken er `usn_lub`, som er implementert i filen [usn_lub_class.py](../USN/usn_lub_class.py). Denne klassen håndterer følgende oppgaver:

- Hente HTML-innhold fra USN-studieretningssidene.
- Analysere HTML-en for å finne relevante tagger som inneholder læringsutbyttebeskrivelser.
- Trekke ut og rense innholdet under disse taggene.
- Eksportere det uttrukne innholdet til `.txt`-filer.

## Bruk

For å kjøre skriptet og generere `.txt`-filene som inneholder læringsutbyttebeskrivelsene, kjør filen [script.py](../USN/script.py). Dette skriptet initialiserer `USN_lub`-klassen med de nødvendige parameterne og kaller hovedmetoden for å starte skrapeprosessen.

For å legge til flere studieretninger og relevante tagger for å trekke ut tekst fra, besøk [script.py](../USN/script.py)

## Krav

Kravene (nødvendige moduler) for å kjøre skriptet er definert i [`Requirements.txt`](../USN/requirements.txt)

```bash
pip install -r requirements.txt
```
