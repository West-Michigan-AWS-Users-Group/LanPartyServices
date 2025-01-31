# https://github.com/Roemer/ut99-server
FROM roemer/ut99-server

# Install unzip
RUN apt-get update && apt-get install -y unzip

# Download Maps-Music-Sounds-Textures.zip from the specified URL
RUN curl -o /ut-data/Maps-Music-Sounds-Textures.zip https://grlanparty.info/assets/Maps-Music-Sounds-Textures.zip

RUN unzip -o -n /ut-data/Maps-Music-Sounds-Textures.zip -d /ut-data/ \
    && rm /ut-data/Maps-Music-Sounds-Textures.zip
