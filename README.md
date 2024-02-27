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

