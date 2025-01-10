# https://github.com/Roemer/ut99-server
FROM roemer/ut99-server

# Install unzip
RUN apt-get update && apt-get install -y unzip

COPY Maps-Music-Sounds-Textures.zip /ut-data/Maps-Music-Sounds-Textures.zip
RUN unzip -o -n /ut-data/Maps-Music-Sounds-Textures.zip -d /ut-data/ \
    && rm /ut-data/Maps-Music-Sounds-Textures.zip
