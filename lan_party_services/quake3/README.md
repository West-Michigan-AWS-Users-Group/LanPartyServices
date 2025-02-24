# Quake 3
<a href="https://grlanparty.info" style="text-decoration: none; color: black;">&#8592; Back</a>

![Quake 3: Arena](https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2200/header.jpg?t=1664229254)

Arena FPS game.

### Supported Platforms
![Windows](https://img.icons8.com/color/48/000000/windows-10.png) ![Mac](https://img.icons8.com/color/48/000000/mac-os.png) ![Linux](https://img.icons8.com/color/48/000000/linux.png)

### Server Info
`quake3.grlanparty.info` <span id="server-status"></span>

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
- Freeze Tag Team Deathmatch

### Installation

#### IO Quake3
IOQuake3 is a free, standalone engine based on the Quake 3: Arena source code and has a client for all platforms.

Download [here](https://ioquake3.org/get-it/). 

It requires a pak0.pak3 files from the original Quake game to play.

Download pak0.pk3 [here](https://grlanparty.info/assets/pak0.pk3) and place into your `quake3/baseq3/pak0.pk3` path.

#### Steam
Quake 3 is also available on [Steam](https://store.steampowered.com/app/2200/Quake_III_Arena/). The Steam client works
just as fine as any other client versions provided by IoQuake3. 


<script>
document.addEventListener("DOMContentLoaded", function() {
    const statusElement = document.getElementById("server-status");

    fetch("https://api.grlanparty.info/status?stack_name=quake3")
        .then(response => response.json())
        .then(data => {
            console.log("Response data:", data);
            const circle = document.createElement("span");
            circle.style.display = "inline-block";
            circle.style.width = "10px";
            circle.style.height = "10px";
            circle.style.borderRadius = "50%";
            circle.style.marginLeft = "5px";
            circle.style.backgroundColor = data.result === true ? "green" : "grey";
            statusElement.appendChild(circle);
        })
        .catch(error => {
            console.error("Error fetching server status:", error);
        });
});
</script></body></html>
