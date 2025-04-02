# Læringsutbytte-uthenting

Dette repoet inneholder kode for å hente ut Læringsutbyttebeskrivelser for studieprogram ved spesifiserte skoler i Norge.

## Slik fungerer det

Uthentning av læringsutbyttebeskrivelser gjøres ved bruk av **Extract** - funksjonen levert av [Firecrawl](https://www.firecrawl.dev/). Firecrawl er laget for å gjøre uthenting av informasjon fra nettsider, såkalt scraping, en lettere prosess. Ved å benytte seg av AI blir dette en nokså sømløst og krever kun definisjon av en *prompt* for å definere hva slags informasjon som skal hentes og hvordan AI modellen skal hente denne.

[Extract](https://www.firecrawl.dev/extract)  funksjonen gir brukeren muligheten til å definere et grensesnitt for hvordan den uthentede informasjon skal fremstilles. Denne modelleringen gjør det lettere å jobbe med og bruke dataen som hentes ut.

## Teknisk beskrivelse

For å se filstrukturen og en beskrivelse av filer, se ______

### Oppsett

Python filen som heter [`firecrawl_app.py`](firecrawl_app.py) er hvor selve firecrawl-innstansen, samt modellen for dataen, defineres.

**OBS!** Firecrawl krever en API-nøkkel. Denne blir ikke pushet til repoet men distribueres til de som forespør. API - nøkkelen hentes fra en `.env` fil, så sørg for å lage denne filen i rotmappen av prosjektet med følgende innhold:

```python
FIRECRAWL_API_KEY = "your_api_key_here"
```

Alle skoler og tilsvarende studieprogram defineres i filen [`config.json`](config.json). For hver skole spesifiseres studieprogram og tilsvarende URL hvor man kan finne læringsutbyttebeskrivelsene for studieprogrammet. Her defineres også en egen *prompt* som skal brukes ved uthenting av læringsutbyttebeskrivelsene.

Grunnen til at hver skole definerer sin egen *prompt* er at skolenes nettsider og fremvisning av læringsutbyttebeskrivelsene varierer. På den måten er det ikke mulig å ha en universell *prompt*, ettersom man vil støte på å måtte gi spesefikke instrukser for hver av skolene/nettsidene for å hente ut riktig informajon på riktig måte.

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
|`firecrawl_app.py`|python|Definering av firecrawl app og modellering for data|
|`config.json`|JSON|Definering av skoler, studieprogram med tilsvarende URL'er og *prompt*|
|`.env`|environment variables|Definering av firecrawl API - nøkkel. NB! Må lages på egenhånd. Se ___|
|`learning_outcomes.ipynb`|Jupyter notebook|Notebook for uthenting av læringsutbyttebeskrivelser|
|`learning_outcomes_single.ipynb`|Jupyter notebook|Notebook for uthenting av læringsutbyttebeskrivelser for én skole|
|`convert_to_excel.ipynb`|Jupyter notebook|Notebook for konverting av CSV til Excel|
|`utils/helpers.py`|Python|Pythonfil som inneholder diverse hjelpefunksjoner|

## Krav for kjøring (Requirements)
