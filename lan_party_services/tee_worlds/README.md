# Teeworlds
<a href="https://grlanparty.info" style="text-decoration: none; color: black;">&#8592; Back</a>

![Teeworlds](https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/380840/header.jpg?t=1578354106)

https://www.teeworlds.com/

Side scroller multiplayer mayhem. CTF, DM and TDM game modes, all free.

### Supported Platforms
![Windows](https://img.icons8.com/color/48/000000/windows-10.png) ![Mac](https://img.icons8.com/color/48/000000/mac-os.png) ![Linux](https://img.icons8.com/color/48/000000/linux.png)

### Server Info
`tee-worlds.grlanparty.info:8303` <span id="server-status"></span>

### Installation
Teeworlds is available as a standalone [installer](https://www.teeworlds.com/?page=downloads) and on [Steam](https://store.steampowered.com/app/380840/Teeworlds/?curator_clanid=6859938&curator_listid=48389).


<script>
document.addEventListener("DOMContentLoaded", function() {
    const statusElement = document.getElementById("server-status");

    fetch("https://api.grlanparty.info/status?stack_name=teeworlds")
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
