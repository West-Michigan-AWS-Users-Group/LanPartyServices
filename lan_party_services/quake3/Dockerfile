# https://github.com/LacledesLAN/gamesvr-ioquake3
FROM lacledeslan/gamesvr-ioquake3

RUN apt-get update && apt-get install -y curl
# Download pak0.pk3 from the specified URL
RUN curl -o /app/baseq3/pak0.pk3 https://grlanparty.info/assets/pak0.pk3
