# 🚀🚀 Læringsutbytte-uthenting 🚀🚀

[🇮🇸 Click here for English version](README.en.md)

Denne mappen inneholder kode for å hente ut Læringsutbyttebeskrivelser for studieprogram ved spesifiserte skoler i Norge.



## Innholdsfortegnelse 📑

- [🔍 Slik fungerer det](#slik-fungerer-det)
- [⚙️ Oppsett](#oppsett)
- [📤 Uthenting av læringsutbyttebeskrivelser og output](#uthenting-av-læringsutbyttebeskrivelser-og-output)
- [🔄 Sammenligning av læringsutbyttebeskrivelser](#sammenligning-av-læringsutbyttebeskrivelser)
- [🔗 Hjelp med URL'er som inneholder år](#hjelp-med-urler-som-inneholder-år)
- [📁 Filstruktur](#filstruktur)
- [📋 Krav for kjøring (Requirements)](#krav-for-kjøring-requirements)
- [📝 Notater](#notater)

## Slik fungerer det

Uthentning av læringsutbyttebeskrivelser gjøres ved bruk av **Extract** - funksjonen levert av [Firecrawl](https://www.firecrawl.dev/). Firecrawl er laget for å gjøre uthenting av informasjon fra nettsider, såkalt scraping, en lettere prosess. Ved å benytte seg av AI blir dette en nokså sømløst og krever kun definisjon av en *prompt* for å definere hva slags informasjon som skal hentes og hvordan AI modellen skal hente denne.

[Extract](https://www.firecrawl.dev/extract)  funksjonen gir brukeren muligheten til å definere et grensesnitt for hvordan den uthentede informasjon skal fremstilles. Denne modelleringen gjør det lettere å jobbe med og bruke dataen som hentes ut.

Det er mulig å endre hvordan dataen som scrapes representeres. Dette gjøres ved å modifisere `NestedModel(BaseModel)` i `firecrawl_app.py`. Her kan man definere en annen struktur for hvordan dataen skal organiseres og lagres.

For å se filstrukturen og en beskrivelse av filer, se [Filstruktur](#filstruktur)

## Oppsett

Python filen som heter [`firecrawl_app.py`](firecrawl_app.py) er hvor selve firecrawl-innstansen, samt modellen for dataen, defineres.

**OBS!** Firecrawl krever en API-nøkkel. Denne blir ikke pushet til repoet men distribueres til de som forespør. API - nøkkelen hentes fra en `.env` fil, så sørg for å lage denne filen i rotmappen av prosjektet med følgende innhold:

```python
FIRECRAWL_API_KEY = "your_api_key_here"
```

Alle skoler og tilsvarende studieprogram defineres i filen [`config.json`](config.json). For hver skole spesifiseres studieprogram og tilsvarende URL hvor man kan finne læringsutbyttebeskrivelsene for studieprogrammet. Her defineres også en egen *prompt* som skal brukes ved uthenting av læringsutbyttebeskrivelsene.

Grunnen til at hver skole definerer sin egen *prompt* er at skolenes nettsider og fremvisning av læringsutbyttebeskrivelsene varierer. På den måten er det ikke mulig å ha en universell *prompt*, ettersom man vil støte på å måtte gi spesefikke instrukser for hver av skolene/nettsidene for å hente ut riktig informajon på riktig måte. Husk at prompten som brukes for hver skole ikke nødvendigvis er den beste. Denne er alltids mulig å endre!

Dersom en ønsker å legge til flere skoler eller studieprogram er det bare å legge til i [`config.json`](config.json) filen. Oppsettet i filen er lett å forstå seg på.

## Uthenting av læringsutbyttebeskrivelser og output

For å hente ut læringsutbyttebeskrivelser for alle studieprogram og skoler, kjører du jupyter notebooken [`learning_outcomes.ipynb`](learning_outcomes.ipynb). Denne vil basere seg på `config.json`

Det vil også være mulig å hente ut læringsutbyttebeskrivelser for kun en skole. Da kjører du filen som heter [`learning_outcomes_single.ipynb`](learning_outcomes_single.ipynb). Sørg for å definere nødvendige parametre i filen.

Ved å kjøre scriptene vil det lages en CSV - fil som inneholder:

- *skole*
- *studie_program*
- *læringsutbytte type (kunnskap, ferdighet eller generell_kompetanse)*
- *læringsutbytte*.

Eks:

| Skole | Studieprogram | Læringsutbytte type | Læringsutbytte |
|-------|--------------|---------------------|----------------|
|   UiO   |     Informatikk        |  Kunnskap                   |   kandidaten ...             |

### Excel format

Etter å ha kjørt scriptet som lager CSV-filer, vil det i tillegg lages en excel fil. Denne følger med litt formateringer for å gjøre excel filen lettere å lese. Filen vil hete det samme som CSV-filen som lages, bare ha endingen `.xlx`.

## Sammenligning av læringsutbyttebeskrivelser

Det er også laget et script for å kunne sammenligne to csv filer. Hensikten er å kunne se læringsutbyttebeskrivelsene har endret seg i løpet av en periode. For at sammenligningen skal fungere riktig, er det viktig at CSV-filene som skal sammenlignes er hentet med scriptene beskrevet i "Uthenting av læringsutbyttebeskrivelser og output", slik at formatet og kolonnene er de samme.

For å kunne sammenlinge læringsutbyttebeskrivelser for alle studieprogram og skoler, kjører du jupyter notebooken [`learning_outcomes_differences.ipynb`](learning_outcomes.ipynb). Sørg for å definere nødvendige parametre i filen. Her skal du legge til de to csv filene du ønsker å sammenligne.

Ved å kjøre scriptet og det er noen forskjeller vil det lages en CSV: "learning_outcome_differences.csv"- fil som inneholder:

- *skole*
- *studie_program*
- *læringsutbytte type (kunnskap, ferdighet eller generell_kompetanse)*
- *læringsutbytte*
- *læringsutbytte first file*
- *læringsutbytte second file*
- *Differences*

## Hjelp med URL'er som inneholder år

Noen URL'er inneholder årstall (for ulike kull), som betyr at ettersom året endres seg, vil læringsutbytter for dette kullet få en ny URL.

Dette betyr at for å hente ut de nyeste læringsutbyttebeskrivelsene, må URL'en som scrapes fra endres.  

**Eksempelvis:**

- for kull 2024:
    <https://www.uia.no/studier/program/data-ingeniorutdanning-bachelor/studieplaner/2024h.html>

- for kull 2025:
    <https://www.uia.no/studier/program/data-ingeniorutdanning-bachelor/studieplaner/2025h.html>

Derfor er det laget et script i [`url_helper.ipynb`](url_helper.ipynb) som scanner `config.json` filen og henter ut de URL'ene som inneholder årstall på en naturlig måte. Deretter vil scriptet forsøke å "pinge" den samme URL'en for studieprogrammet, men med det nåværende år. Scriptet gir tilbakemeldinger for hver aktuelle skole og studieprogram.  

Dette er ment som et verktøy for å sjekke om man er oppdatert med nyeste informasjon for hvert studieprogram.

<span style="color:red">NB!</span> Selvom scriptet sier at det finnes en nyere URL enn den som finnes i `config.json`, kan det hende at denne siden ikke inneholder innhold. Alltid sjekk den nyere siden før du eventuelt endrer URL!

#### <span style="color:red">**UIT** og **KRISTIANIA** inneholder årstall, men disse fungerer noe forskjellig. Begge disse skolene presenterer læringsutbyttebeskrivelser i en PDF. Disse URL'ene er vanskelig å få oppdatert, da man henter PDF'er over nett fra URL'er som er ulikt formatert. </span>

## Filstruktur

| Fil | type | Beskrivelse |
|-------|--------------|---------------------|
|[`requirements.txt`](requirements.txt)|txt|Pythonfil som inneholder diverse hjelpefunksjoner|
|[`.env`](.env)|Environment Variables|Definering av firecrawl API - nøkkel. NB! Må lages på egenhånd. Se [Oppsett](#oppsett)|
|[`config.json`](config.json)|JSON|Definering av skoler, studieprogram med tilsvarende URL'er og *prompt*|
|[`firecrawl_app.py`](firecrawl_app.py)|Python|Definering av firecrawl app og modellering for data|
|[`utils/helpers.py`](utils/helpers.py)|Python|Pythonfil som inneholder diverse hjelpefunksjoner|
|[`learning_outcomes.ipynb`](learning_outcomes.ipynb)|Jupyter Notebook|Notebook for uthenting av læringsutbyttebeskrivelser for alle definerte skoler|
|[`learning_outcomes_single.ipynb`](learning_outcomes_single.ipynb)|Jupyter Notebook|Notebook for uthenting av læringsutbyttebeskrivelser for én skole|
|[`learning_outcomes_differences.ipynb`](learning_outcomes_differences.ipynb)|Jupyter Notebook|Notebook for sammenligning av læringsutbyttebeskrivelser|
|[`url_helper.ipynb`](url_helper.ipynb)|Jupyter Notebook|Notebook for hjelp med URL adresser for studieprogram som inneholder årstall|
|[`scraping/USN`](scraping/USN/README.md)|Mappe|Inneholder kode for å scrape læringsutbyttebeskrivelser fra USN|

## Krav for kjøring (Requirements)

For å kjøre prosjektet kreves følgende Python-pakker:

- `firecrawl` - Brukes i `firecrawl_app.py` for web scraping funksjonalitet
- `pydantic` - Brukes for data modellering og validering i `firecrawl_app.py`
- `python-dotenv` - Brukes for å laste inn miljøvariabler fra `.env` fil
- `pandas` - Brukes i `utils/helpers.py` for data manipulering og CSV/Excel operasjoner
- `openpyxl` - Brukes for Excel fil formatering og styling
- `beautifulsoup4` - Brukes i `usn_lub_class.py` for HTML parsing
- `selenium` - Brukes for web automatisering og nettleserkontroll
- `pyshadow` - Brukes for håndtering av shadow DOM elementer i web scraping

For å installere disse avhengighetene, kjør følgende kommando:

```bash
pip install -r requirements.txt
```

Merk: For at Selenium skal fungere optimalt, må du også ha den aktuelle nettleserdriveren installert (ChromeDriver i dette tilfellet, som sett i koden). Dette installeres typisk separat fra Python-pakkene.

# Notater

### Om Prompter

Husk at prompten som brukes for hver skole ikke nødvendigvis er den beste. Den som følger med denne kodebasen er blitt brukt til testing og beholdt grunnet gode resultater. <span style="color:green">**Denne prompten er alltids mulig å endre!**</span>

### Begrensninger i Scraping

Grunnet vanskeligheter med nettsidene til USN (benytter seg av shadow-root), klarer ikke firecrawl å scrape læringsutbyttebeskrivelsene. Dette er fordi måten koden til nettsiden er lagt opp på ikke tilgjengeligjør ønsket informasjon med en gang. Derfor er det, for nå, ikke mulig å scrape USN sine nettsider med firecrawl. I mappen [`scraping/USN`](scraping/USN) ligger derfor gammel kode for scraping som håndterer shadow-root, men selve koden har forbedringspotensial. Denne er midlertidig mulig å bruke. Dette vil produsere tekstfiler som inneholder læringsutbyttebeskrivelsene. Les `README.md` for instruksjoner.

UIT fremstiller læringsutbyttebeskrivelser i form av PDF. Firecrawl klarer å scrape PDF'er, men strukturen på denne PDF'en er så kronglete at den av en eller annen grunn ikke får det til (selvom den klarer Kristiania som også har det i PDF). Dette kan man se videre på.

#### <span style="color:red">**Pga. dette, er det ikke foreløpig mulig å hente ut læringsutbyttebeskrivelse for UIT og USN med den eksisterende løsningen!** </span>

### Andre ting

Som nevnt presenterer Kristiania læringsutbyttebeskrivelser gjennom PDF'er. I senere tid har det blitt oppdaget at disse oppdaterer seg, men ikke ligger tilgjengelig direkte på nettsiden til Kristiania, men heller er mulig å laste ned. Siden man kan åpne nedlastede PDF'er direkte i nettleseren, er det mulig å endre URL'en til studieprogrammene til Kristiania til å peke direkte mot PDF'ens lokasjon lokalt på PC'en. Vi annerkjenner at dette fører til mer jobb enn vi skulle ønske
