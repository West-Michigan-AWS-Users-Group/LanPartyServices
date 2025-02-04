# Unreal Tournament 99
<a href="https://grlanparty.info" style="text-decoration: none; color: black;">&#8592; Back</a>

![Unreal Tournament 99](https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/13240/header.jpg?t=1671033924)

Legendary FPS Arena shooter.

### Supported Platforms
![Windows](https://img.icons8.com/color/48/000000/windows-10.png) ![Mac](https://img.icons8.com/color/48/000000/mac-os.png) ![Linux](https://img.icons8.com/color/48/000000/linux.png)

### Server Info
`ut99.grlanparty.info` <span id="server-status"></span>

Tested Game Modes/Mutators:
- CTF Instagib
- DM Rocket Arena

Game modes can be changed by redeploying the server with the desired mutator.

### Installation

#### Steam
Unreal Tournament 99 was de-listed from Steam years ago, however you might have it in your library. This version
of the game works just as fine as any other client versions provided by OldUnreal.

#### Source
Download latest version of Unreal Tournament from the [OldUnreal Github](https://github.com/OldUnreal/UnrealTournamentPatches/releases)

Download the necessary files from the mirror site [here](https://grlanparty.info/assets/Maps-Music-Sounds-Textures.zip).

Follow the instructions [here](https://github.com/OldUnreal/UnrealTournamentPatches/blob/master/README.md) for your OS specific installation.


<script>
document.addEventListener("DOMContentLoaded", function() {
    const statusElement = document.getElementById("server-status");

    fetch("https://api.grlanparty.info/status?stack_name=ut99")
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
</script>
