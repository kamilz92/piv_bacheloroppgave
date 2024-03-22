# piv_bacheloroppgave

# Hvordan man skal sette opp EMPAIA Test Suite (EATS) for første gang

Hopp mellom steg ved hjelp av ![image](https://github.com/kamilz92/piv_bacheloroppgave/assets/148437004/88afce22-8e84-4f27-98f1-0b0b2ade61e6) ikonet oppe i høyre hjørne


## Steg 1: Laste ned det man trenger
Om ubuntu ikke allerede er lastet ned, gå til  microsoft store for å laste ned denne
![image](https://github.com/kamilz92/piv_bacheloroppgave/assets/148437004/2a99bf37-533d-4c77-b5f7-0b72637da29b)

Deretter gå til terminalen på datamaskinen og skriv "ubuntu", dette åpner Windows Subsystem for Linux (WSL) hvor EATS må kjøres gjennom. Første gangen dette åpnes må det opprettes brukernavn og passord.

Her pleier Python allerede å være lastet ned, om ikke må den lastes ned ved bruk av:
```sudo apt-get install python3.10```.
Dette er den nyeste versjonen av python i denne versjonen av Ubuntu.

Deretter må "pip" lastes ned, dette gjørs ved å kjøre:
```sudo apt install python3-pip```

Om man får feilmelding må man først kjøre ```sudo apt-get update``` og prøve igjen.

## Steg 2: klarkjøring til bruk av EATS
Nå er det på tide å laste ned EATS, dette kan gjøres ved bruk av: ```pip install empaia-app-test-suite``` La dette gjøre seg ferdig, kan ta litt tid.

Når det er lastet ned må man bevege seg til et passende sted i filsystemet på maskinen, og oprette en mappe. Her kan man bruke kommandoen cd for å bevege seg inn i en mappe. Vær obs på at filstier ser annerledes ut i linux enn i windows, så hos meg ble dette:
```
cd /mnt/c/Users/sande/OneDrive/Desktop/Fag/BachelorDAT191/code
```
Istedenfor:
```
cd C:\Users\sande\OneDrive\Desktop\Fag\BachelorDAT191\code
```

Når man er i en passende mappe må man oprette en ny mappe ("eats") og bevege seg inn i denne før man opretter enda en mappe ("images"). Dette gjøres slik:
```
mkdir eats
cd eats
mkdir images
```
Husk å bare bruke en linje om gangen. "images" er mappen vi skal legge inn bildene som skal behandles av eventuelle algoritmer.

Nå skla vi oprette en json fil som inneholder lokasjonen til bildene i "images" mappen, det er også denne filen som skal kalles når man åpner EATS. Denne filen skla ligge i mappen "eats", den skal hete ```wsi-mount-points.json```, og den skal se slik ut:
```
{
    "{din filsti til eats mappen}/eats/images": "/data"
}
```
Med min filsti vil den dermed se slik ut:
```
{
    "/mnt/c/Users/sande/OneDrive/Desktop/Fag/BachelorDAT191/code/eats/images": "/data"
}
```

Om man vil slippe å laste opp et notat til en .json converter på nett for å oprette filen, er det enkleste å gå inn i et prosjekt i en valgfri IDE og oprette en ny fil, og gi denne riktig navn. Legg inn det jeg viste ovenfor, IDE-en vil automatisk formatere dette riktig som en .json fil: 
 
![image](https://github.com/kamilz92/piv_bacheloroppgave/assets/148437004/7134b1cf-3fb3-4a2e-9fd7-1169b4fe817c)

![image](https://github.com/kamilz92/piv_bacheloroppgave/assets/148437004/bf52be6f-b27c-46d1-bf96-370279f6367c)

Deretter kan man bruke ```ctrl + x``` for å klippe denne ut, og lime den inn direkte inn i "eats" mappen gjennom filutforskeren ![image](https://github.com/kamilz92/piv_bacheloroppgave/assets/148437004/8b47a2b8-8950-4d3d-b6f0-8ecb02ee61c7)
 på din datamaskin:

## Steg 3: kjøring av EATS
Nå er vi egentlig klare til å kjøre EATS.

Før man fortsetter er det viktig å ha lastet ned docker desktop via linken: ```https://www.docker.com/products/docker-desktop/```, eller annen valgfri versjon.

Deretter må man være sikker på at den har blitt godkjent for bruk i WSL(Windows Subsystem for Linux), dette kan man gjøre i selve innstillingene i docker desktop, slik(i vist rekkefølge):

![image](https://github.com/kamilz92/piv_bacheloroppgave/assets/148437004/d04f5291-c264-47f4-8094-bfd303becb3e)


Når man er sikker på at docker desktop kjører og at alt er i orden kan man starte EATS, dette gjøres ved bruk av:
```
eats services up ./wsi-mount-points.json
```
Pass på at du fremdeles ligger i "eats" mappen på datamaskinen.

Dette kan ta litt lang tid første gang ettersom at det er en del docker containere som skal lastes ned.

når denne har kjørt seg ferdig, kan man åpne EATS i nettleser ved hjelp av følgende URL
[http://localhost:8888/wbc3/](http://localhost:8888/wbc3/)

Nå skal EATS kjøre som det skal.


## Steg 4: Legge bilder inn i EATS portalen
Selv om man har laget "image" mappen og til og med lagt inn noen WSI-bilder, må man gjøre noen steg for at disse skal dukke opp i EATS

Først pass på at de har lagt noen WSI-bilder i mappen "images" som ble opprettet tidligere, deretter må vi oprette enda en ```.json``` fil
Denne kan hete hva man vil, men om man har et bilde ```slide1.png``` vil det være passende å kalle den ```slide1.json```.

Denne kan oprettes på samme måte som tidligere, og skal også ligge i "eats" mappen

Filen skal se slik ut:
```
{
    "type": "wsi",
    "path": "/data/<navn-på-bilde>",
    "id": "<id>"
}
```
Her skal ```<navn-på-bilde>``` være navnet på bildet i "image" mappen, feks. ```slide1.png```
Og ```<id>``` skal være en tilfeldig UUID, et eksempel på dette ser slik ut: ```0ceb2040-3d63-4968-9603-80dd89822608```
En slik UUID kan enkelt genereres i terminalen ved hjelp av komandoen ```uuidgen```

![image](https://github.com/kamilz92/piv_bacheloroppgave/assets/148437004/7b2ad257-1fb1-4ef2-bc4e-cce05fdeb59c)

Når denne filen er oprettet og lagt i "eats" mappen, så er det klart og man kan kjøre:
```
eats slides register slide1.json
```
Her må filnavnet endres utifra hva navnet på .json filen er


## Steg 5: legge inn apper i portalen

Her bruker jeg til å begynne med et eksempel program fra EMPAIA sin egen tutorial, fra denne linken:
[https://gitlab.com/empaia/integration/sample-apps/-/tree/master/sample_apps/tutorial](https://gitlab.com/empaia/integration/sample-apps/-/tree/master/sample_apps/tutorial)

Jeg fikk det til å fungere med eksempel TA05

Først må denne dockeriseres, dette kan gjøres endten i IDE eller direkte i terminal, men synes det er lettere i IDE ettersom at det er greit å ha tilgang til alle .json filene man skal bruke. Da må man først bevege seg inn i v3 filen og deretter dockerisere programmet, slik:

```
cd v3
```
```
docker build -t ta05 .
```

Når dette er gjort er det på tide å flytte på alt vi trenger til en ny "input" mappe man lager i "eats" mappen. 
Først av alt er det vært å legge mere til ```ead.json``` filen som ligger i programmet, denne må kopieres og limes inn i "eats" mappen på din datamaskin.
Deretter må man kopiere den ```slide1.json``` man brukte tidligere inn i inputs mappen og gi den samme navn som er navngitt i ```ead.json``` filen. I dette tilfellet skal den hete ```my_wsi.json```:
![image](https://github.com/kamilz92/piv_bacheloroppgave/assets/148437004/7ff09c05-cbf3-48ef-9dab-8ce9c138f4bb)

Deretter må man kopiere både ```my_rectangles.json``` og ```rois.json``` inn i samme "inputs" mappe. Før vi går videre må vi endre litt på ```my_rectangles.json```, vi må endre på "reference_id"-ene slik at de matcher id'en til ```my_wsi.json```(foreløpig er "reference_id" lik id'en til tilsvarende wsi i eksempel programmet, men denne kan ikke vi bruke), for å gjøre dette er det enkleste bare å åpne begge to i en IDE og bare kopiere over id'en fra ```my_wsi.json``` til ```my_rectangles.json```. "reference_id" blir brukt 3 ganger i denne filen, og må derfor byttes ut for alle 3.

```rois.json``` har også en "reference_id" men denne refererer til id'en til ```my_rectangles.json``` så denne kan vi bare la være slik den er.

### Da var vi klar for legge programmet inn i EATS:

Først kan vi begynne slik:

```
eats apps register ead.json ta05 > app.env
```
dette gjør at vi får en .env fil som inneholder viktig innformasjon som APP_ID, denne kan vi gjøre om til en variabel som kan brukes senere, slik:

```
export $(xargs < app.env)
```
Vi kan deretter se verdien til variabelen APP_ID slik:
```
echo $APP_ID
```
og vi kan liste ut alle appene som er registrert:
```
eats apps list
```
Nå kan vi registrere dette som en jobb, her må vi referere til "inputs" mappen vår slik:
```
eats jobs register $APP_ID ./inputs > job.env
```
Her får vi også en slik .env fil, og igjen kan vi får ut viktige variabler slik:
```
export $(xargs < job.env)
```
Den vi skal bruke mest er EMPAIA_JOB_ID som vi kan se her:
```
echo $EMPAIA_JOB_ID
```
Vi kan også se alle lagrede variabler ved å bare skrive:
```
export
```
Nå kan vi endelig kjøre programmet, dette gjøres ved hjelp av:
```
eats jobs run ./job.env
```
Den skal nå kjøre, hvis man får feilmeldinger pleier det endten å være fordi man mangler en fil i "inputs" mappen, eller at man har en feil i "reference_id", men dette står ganske tydelig om dette skjer. Vi kan nå skjekke statusen til denne jobben ved å bruke EMPAIA_JOB_ID, slik:
```
eats jobs status $EMPAIA_JOB_ID 
```
Resultatene kan være en av følgende: SCHEDULED, RUNNING eller COMPLETED, hvis den viser error se hvordan dette kan debugges her: [https://developer.empaia.org/app_developer_docs/v3/#/eats/advanced?id=debugging](https://developer.empaia.org/app_developer_docs/v3/#/eats/advanced?id=debugging)
Hvis man skjekker status før jobben har begynt å kjøre vil man få opp: ASSEMBLY

### Venting
Før man kan laste ned resultatet må jobben være ferdig, men for å slippe å skjekke status manuelt hele tiden hvis prosessen tar litt lengre tid, kan man bruke:
```
eats jobs wait $EMPAIA_JOB_ID
```
Da skjekker programmet automatisk og gir beskjed om den er ferdig. da kan den returnere en av følgende:
![image](https://github.com/kamilz92/piv_bacheloroppgave/assets/148437004/79fac11f-6db8-41e0-9b45-5aa9f6183381)

### Se og laste ned resultat
For å raskt se resultat i terminal, kan man bruke:
```
eats jobs inspect $EMPAIA_JOB_ID
```
for å laste ned .json fil til ny mappe, kan man bruke:
```
eats jobs export $EMPAIA_JOB_ID ./job-outputs
```

### Hvordan se resultat i nettleser
se linken nedenfor for bilder av dette:
[https://developer.empaia.org/app_developer_docs/v3/#/eats/running_apps?id=results-workbench-client](https://developer.empaia.org/app_developer_docs/v3/#/eats/running_apps?id=results-workbench-client)


### mer info
Mer detaljert informasjon om dette kan finnes her:
[https://developer.empaia.org/app_developer_docs/v3/#/eats/running_apps](https://developer.empaia.org/app_developer_docs/v3/#/eats/running_apps)

## Steg 6: Lage egne programmer som fungerer i EATS
For å lage egne programmer som fungerer med my_rectangle er det en del steg man må gjennom, resulterende kode ser slik ut:

### Glue code
```
import os
import requests
import numpy as np
from PIL import Image
from io import BytesIO


APP_URL = "http://host.docker.internal:8888/app-api"
JOB_ID = os.environ.get('EMPAIA_JOB_ID')
TOKEN = os.environ.get('EMPAIA_TOKEN')
HEADER = {"Authorization": f"Bearer {TOKEN}"}

print(TOKEN)
print(HEADER)

# Retrieve meta-data
input_url = f"{APP_URL}/v3/{JOB_ID}/inputs/my_wsi"
print(input_url)

r = requests.get(input_url, headers=HEADER)
r.raise_for_status()
wsi_meta = r.json()
wsi_id = wsi_meta['id']

# Download tile (7,1) at level 2
tile_url = f"{APP_URL}/v3/{JOB_ID}/tiles/{wsi_id}/level/2/position/7/1"
r = requests.get(tile_url, headers=HEADER)
r.raise_for_status()
i = Image.open(BytesIO(r.content))
a = np.array(i)
print(a.shape)
print("Hello World")


# Do something cool with your multi-dimensional array of pixel-color values, like put it in a Neural Network or so...


def put_finalize():
    """
    finalize job, such that no more data can be added and to inform EMPAIA infrastructure about job state
    """
    url = f"{APP_URL}/v3/{JOB_ID}/finalize"
    f = requests.put(url, headers=HEADER)
    f.raise_for_status()


def get_input(key: str):
    """
    get input data by key as defined in EAD
    """
    url = f"{APP_URL}/v3/{JOB_ID}/inputs/{key}"
    f = requests.get(url, headers=HEADER)
    f.raise_for_status()
    return f.json()


def get_wsi_tile(my_wsi2: dict, my_rectangle2: dict):
    """
    get a WSI tile on level 0

    Parameters:
        my_wsi2: contains WSI id (and meta data)
        my_rectangle2: tile position on level 0
    """
    x, y = my_rectangle2["upper_left"]
    width = my_rectangle2["width"]
    height = my_rectangle2["height"]

    wsi_id2 = my_wsi2["id"]
    level = 0

    tile_url2 = f"{APP_URL}/v3/{JOB_ID}/regions/{wsi_id2}/level/{level}/start/{x}/{y}/size/{width}/{height}"
    f = requests.get(tile_url2, headers=HEADER)
    f.raise_for_status()

    return Image.open(BytesIO(f.content))


def post_output(key: str, data: dict):
    """
    post output data by key as defined in EAD
    """
    url = f"{APP_URL}/v3/{JOB_ID}/outputs/{key}"
    f = requests.post(url, json=data, headers=HEADER)
    f.raise_for_status()
    return f.json()


def my_function(wsi_tile2: Image):
    """
    Din ønskede kode må skrives i denne metoden i dette eksempelet
    """
    return 42


my_wsi = get_input("my_wsi")
my_rectangle = get_input("my_rectangle")

wsi_tile = get_wsi_tile(my_wsi, my_rectangle)

my_quantification_result = {
    "name": "fibrosis score",  # choose name freely
    "type": "float",
    "value": my_function(wsi_tile),
    "creator_type": "job",  # NEW required in v3 apps
    "creator_id": JOB_ID,  # NEW required in v3 apps
}


post_output("my_quantification_result", my_quantification_result)

put_finalize()
```

Det er mye ekstra som må legges inn for å kunne hente verdier og bilder via EMPAIA hvor i dette tilfellet bare my_function metoden inneholder hva man ønsker å gjøre med dette bildet.

Må også si ifra om at i dette tilfellet så bruker jeg ikke en rois.json fil. Men her er tilhørende ```ead```, ```my_rectangle``` og ```my_wsi``` fil. Vær obs på at my rectangles skal ligge i ```inputs``` mappen og ```ead``` skal ligge direkte i ```eats``` mappen

### ead.json
```
{
    "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
    "name": "My Cool Medical AI Algorithm",
    "name_short": "Cool App",
    "namespace": "org.empaia.helse_vest_piv.cool_app.v3.1",
    "description": "Does super advanced AI stuff, you know...",
    "io": {
        "my_wsi": {
            "type": "wsi"
        },
        "my_rectangle": {
            "type": "rectangle",
            "reference": "io.my_wsi"
        },
        "my_quantification_result": {
            "type": "float"
        }
    },
    "modes": {
        "standalone": {
            "inputs": [
                "my_wsi",
                "my_rectangle"
            ],
            "outputs": [
                "my_quantification_result"
            ]
        }
    }
}
```


### my_rectangle.json
```
{
    "name": "my_rectangle",
    "type": "rectangle",
    "upper_left": [
        1000,
        2000
    ],
    "width": 300,
    "height": 500,
    "reference_id": "b104a16c-a239-49be-aec1-e9e94966484d",
    "reference_type": "wsi",
    "npp_created": 499,
    "npp_viewing": [
        1,
        499123
    ]
}
```

### my_wsi.json
```
{
    "type": "wsi",
    "path": "/data/Sirius1.svs",
    "id": "b104a16c-a239-49be-aec1-e9e94966484d"
}
```

Vær oppmerksom på at spessielt glue koden må endres på om man for eksempel ønsker å iterere gjennom tiles. Denne koden fungerer bare ved å spesifisere en rektangel på forhånd.



## Steg ?: Lukke EATS på forkjellige måter
Om man har gjort seg ferdig og har lyst til å avslutte kjøringen av EATS er det 2 måter å gjøre dette på:
For å lukke det uten å slette det som ligger bak:
```
eats services down
```
Om man vil slette alt(inkøludert WSI-bilder, apper, og andre jobber) bruk -v:
```
eats services down -v
```

