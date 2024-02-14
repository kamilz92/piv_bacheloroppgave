# piv_bacheloroppgave

# Hvordan man skal sette oppp EMPAIA Test Suite (EATS) for første gang

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

