# Læringsutbytte-uthenting

Dette repoet inneholder kode for å hente ut Læringsutbyttebeskrivelser for studieprogram ved spesifiserte skoler i Norge.

## Slik fungerer det

Uthentning av læringsutbyttebeskrivelser gjøres ved bruk av **Extract** - funksjonen levert av [Firecrawl](https://www.firecrawl.dev/). Firecrawl er laget for å gjøre uthenting av informasjon fra nettsider, såkalt scraping, en lettere prosess. Ved å benytte seg av AI blir dette en nokså sømløst og krever kun definisjon av en *prompt* for å definere hva slags informasjon som skal hentes og hvordan AI modellen skal hente denne.

[Extract](https://www.firecrawl.dev/extract)  funksjonen gir brukeren muligheten til å definere et grensesnitt for hvordan den uthentede informasjon skal fremstilles. Denne modelleringen gjør det lettere å jobbe med og bruke dataen som hentes ut.

Det er mulig å endre hvordan dataen som scrapes representeres. Dette gjøres ved å modifisere `NestedModel(BaseModel)` i `firecrawl_app.py`. Her kan man definere en annen struktur for hvordan dataen skal organiseres og lagres.

## Teknisk beskrivelse

For å se filstrukturen og en beskrivelse av filer, se [Filstruktur](#filstruktur)

### Oppsett

Python filen som heter [`firecrawl_app.py`](firecrawl_app.py) er hvor selve firecrawl-innstansen, samt modellen for dataen, defineres.

**OBS!** Firecrawl krever en API-nøkkel. Denne blir ikke pushet til repoet men distribueres til de som forespør. API - nøkkelen hentes fra en `.env` fil, så sørg for å lage denne filen i rotmappen av prosjektet med følgende innhold:

```python
FIRECRAWL_API_KEY = "your_api_key_here"
```

Alle skoler og tilsvarende studieprogram defineres i filen [`config.json`](config.json). For hver skole spesifiseres studieprogram og tilsvarende URL hvor man kan finne læringsutbyttebeskrivelsene for studieprogrammet. Her defineres også en egen *prompt* som skal brukes ved uthenting av læringsutbyttebeskrivelsene.

Grunnen til at hver skole definerer sin egen *prompt* er at skolenes nettsider og fremvisning av læringsutbyttebeskrivelsene varierer. På den måten er det ikke mulig å ha en universell *prompt*, ettersom man vil støte på å måtte gi spesefikke instrukser for hver av skolene/nettsidene for å hente ut riktig informajon på riktig måte. Husk at prompten som brukes for hver skole ikke nødvendigvis er den beste. Denne er alltids mulig å endre!

Dersom en ønsker å legge til flere skoler eller studieprogram er det bare å legge til i [`config.json`](config.json) filen. Oppsettet i filen er lett å forstå seg på.

### Uthenting av læringsutbyttebeskrivelser og output

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

#### Excel format

Etter å ha kjørt scriptet som lager CSV-filer, vil det i tillegg lages en excel fil. Denne følger med litt formateringer for å gjøre excel filen lettere å lese. Filen vil hete det samme som CSV-filen som lages, bare ha endingen `.xlx`.

## Filstruktur

| Fil | type | Beskrivelse |
|-------|--------------|---------------------|
|`firecrawl_app.py`|Python|Definering av firecrawl app og modellering for data|
|`config.json`|JSON|Definering av skoler, studieprogram med tilsvarende URL'er og *prompt*|
|`.env`|Environment Variables|Definering av firecrawl API - nøkkel. NB! Må lages på egenhånd. Se [Oppsett](#oppsett)|
|`learning_outcomes.ipynb`|Jupyter Notebook|Notebook for uthenting av læringsutbyttebeskrivelser for alle definerte skoler|
|`learning_outcomes_single.ipynb`|Jupyter Notebook|Notebook for uthenting av læringsutbyttebeskrivelser for én skole|
|`utils/helpers.py`|Python|Pythonfil som inneholder diverse hjelpefunksjoner|

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

## Notater

### Om Prompter

Husk at prompten som brukes for hver skole ikke nødvendigvis er den beste. Den som følger med denne kodebasen er blitt brukt til testing og beholdt grunnet gode resultater. <span style="color:green">Denne prompten er alltids mulig å endre!</span>

### Begrensninger i Scraping

Grunnet vanskeligheter med nettsidene til USN (benytter seg av shadow-root), klarer ikke firecrawl å scrape læringsutbyttebeskrivelsene. Dette er fordi måten koden til nettsiden er lagt opp på ikke tilgjengeligjør ønsket informasjon med en gang. Derfor er det, for nå, ikke mulig å scrape USN sine nettsider med firecrawl. I mappen `Scraping/USN` ligger derfor gammel kode for scraping som håndterer shadow-root, men selve koden har forbedringspotensial. Denne er midlertidig mulig å bruke.

UIT fremstiller læringsutbyttebeskrivelser i form av PDF. Firecrawl klarer å scrape PDF'er, men strukturen på denne PDF'en er så kronglete at den av en eller annen grunn ikke får det til (selvom den klarer Kristiania som også har det i PDF). Dette kan man se videre på.

<span style="color:red">**Pga. dette, er det ikke foreløpig mulig å hente ut læringsutbyttebeskrivelse for disse skolene med den eksisterende løsningen!** </span>
