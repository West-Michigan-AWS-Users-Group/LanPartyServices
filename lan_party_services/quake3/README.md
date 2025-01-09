## Quake 3.
Using the https://github.com/InAnimaTe/docker-quake3 image, we can run a Quake 3 server in a container.
`server.cfg` takes the following parameters: http://www.joz3d.net/html/q3console.html

The pak files are not free, you must own a copy of those.

The mod pk3 files must also be copied into the `baseq3` directory.


## Building locally
```bash
docker build -t quake3 lan_party_services/quake3/
docker run -d -p 27960:27960/udp quake3
```


## Client download
https://ioquake3.org/get-it/
