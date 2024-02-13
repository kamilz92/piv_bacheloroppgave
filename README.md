# piv_bacheloroppgave

## Hvordan man skal sette oppp EMPAIA Test Suite (EATS)
Om ubuntu ikke allerede er lastet ned, gå til  microsoft store for å laste ned denne
![image](https://github.com/kamilz92/piv_bacheloroppgave/assets/148437004/2a99bf37-533d-4c77-b5f7-0b72637da29b)

Deretter gå til terminalen på datamaskinen og skriv "ubuntu", dette åpner Windows Subsystem for Linux (WSL) hvor EATS må kjøres gjennom. Første gangen dette åpnes må det opprettes brukernavn og passord.

Her pleier Python allerede å være lastet ned, om ikke må den lastes ned ved bruk av:
```sudo apt-get install python3.10```.
Dette er den nyeste versjonen av python i denne versjonen av Ubuntu.

Deretter må "pip" lastes ned, dette gjørs ved å kjøre:
```sudo apt install python3-pip```

Om man får feilmelding må man først kjøre ```sudo apt-get update``` og prøve igjen.

Nå er det på tide å laste ned EATS, dette kan gjøres ved bruk av: ```pip install empaia-app-test-suite``` La dette gjøre seg ferdig, kan ta litt tid.

Når det er lastet ned må man bevege seg til et passende sted i filsystemet på maskinen, og oprette en mappe. Her kan man bruke kommandoen cd for å bevege seg inn i en mappe. Vær obs på at filstier ser annerledes ut i linux enn i windows, så hos meg ble dette:
```
cd /mnt/c/Users/sande/OneDrive/Desktop/Fag/BachelorDAT191/code
```
istedenfor:
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





