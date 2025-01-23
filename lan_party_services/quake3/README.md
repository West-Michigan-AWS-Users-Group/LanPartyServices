# Quake 3
<a href="javascript:history.back()" style="text-decoration: none; color: black;">&#8592; Back</a>

![Quake 3: Arena](https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2200/header.jpg?t=1664229254)

Arena FPS game.

### Supported Platforms
![Windows](https://img.icons8.com/color/48/000000/windows-10.png) ![Mac](https://img.icons8.com/color/48/000000/mac-os.png) ![Linux](https://img.icons8.com/color/48/000000/linux.png)

### Server Info
`quake3.grlanparty.info`

This server is using the [lacledeslan/gamesvr-ioquake3](https://github.com/LacledesLAN/gamesvr-ioquake3) Docker image.

This container has the following modes:

**Vanilla:**
- FFA Deathmatch
- Team Deathmatch
- CTF

**Instagib:**
- Deathmatch
- Team Deathmatch
- 1v1
- CTF

**Other:**
- Free Tag Team Deathmatch

Server can be changed to any of the above modes by changing start CMD of the docker container.

### Installation

#### IO Quake3
IOQuake3 is a free, standalone engine based on the Quake 3: Arena source code. It requires a pak0.pak3 files from the original Quake game to play and is supported on all platforms.

https://ioquake3.org/get-it/

Download pak0.pk3 [here](https://grlanparty.info/assets/pak0.pk3) and place into your `quake3/baseq3/pak0.pk3` path.

#### Steam
Quake 3 is also available on [Steam](https://store.steampowered.com/app/2200/Quake_III_Arena/). The Steam client works
just as fine as any other client versions provided by IoQuake3. 
