# Open Red Alert
<a href="https://grlanparty.info" style="text-decoration: none; color: black;">&#8592; Back</a>

![Open Red Alert](https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2229840/header.jpg?t=1711105061)

Open source port of Command and Conquer: Red Alert and classic Westwood RTS engine. Has the ability to play every Westwood game from the Tiberium universe, such as Tiberian Dawn, Red Alert, and Dune 2000.

### Supported Platforms
![Windows](https://img.icons8.com/color/48/000000/windows-10.png) ![Mac](https://img.icons8.com/color/48/000000/mac-os.png) ![Linux](https://img.icons8.com/color/48/000000/linux.png) ![FreeBSD](https://img.icons8.com/color/48/000000/free-bsd.png)


### Server Info
`openra.grlanparty.info` <span id="server-status"></span>

Running in [this](https://github.com/OpenRA/OpenRA/wiki/Dedicated-Server) docker container image.

### Installation
Download and install the game from the [official site](https://www.openra.net/download/). Follow the instructions for your respective platform.

<script>
document.addEventListener("DOMContentLoaded", function() {
    const statusElement = document.getElementById("server-status");

    fetch("https://api.grlanparty.info/status?stack_name=openra")
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

