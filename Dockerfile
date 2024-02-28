FROM python:3.12.2
# Setter den aktuelle katalogen i containeren
WORKDIR .

# Denne kommandosekvensen sikrer at nødvendige biblioteker for OpenCV er
#installert: apt-get update oppdaterer pakkelisten, apt-get install -y installerer
#de nødvendige bibliotekene, apt-get clean fjerner overflødige installasjonsfiler for å spare plass
#og rm -rf /var/lib/apt/lists/* reduserer bildets størrelse ved å fjerne pakkelistene.
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Her installeres nødvendige Python-pakker som applikasjonen avhenger av
RUN pip install numpy opencv-python matplotlib
# Disse linjene kopierer filer og mapper.
# Først hva som skal kopiers og hvor.
# sørg for å oppdatere filnavnene om nødvendig før bygging
COPY Images/ ./Images
COPY main.py algorithm2.py  ./
# Bygg og kjør Docker-bildet:

# Bygg bildet: docker build -t mitt-bilde .
# Kjør interaktivt(input) og fjern etter bruk: docker run -it --rm mitt-bilde
CMD ["python", "main.py"]