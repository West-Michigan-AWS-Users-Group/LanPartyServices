# Unreal Tournament 2004
<a href="https://grlanparty.info" style="text-decoration: none; color: black;">&#8592; Back</a>

![Unreal Tournament 2004](https://shared.steamstatic.com/store_item_assets/steam/apps/13230/header.jpg?t=1671033925)

The next iteration of the legendary FPS Arena shooter, Unreal Tournament, adding new weapons, vehicles, and game modes.

### Supported Platforms
![Windows](https://img.icons8.com/color/48/000000/windows-10.png) ![Mac](https://img.icons8.com/color/48/000000/mac-os.png)

### Server Info
`ut2k4.grlanparty.info` <span id="server-status"></span>

This server has a number of mutators listed [here](https://github.com/LacledesLAN/gamesvr-ut2004).

### Installation

#### Mac M1 (Using Whisky)
Note: This game is not natively supported on Mac M1. You will need to use Whiskey to run the game as outlined in the reddit post [here](https://www.reddit.com/r/unrealtournament/comments/18wkbqq/guide_ut_on_apple_silicon/).

- Download Whisky [here](https://getwhisky.app/)

- Using Whiskey, install the dependencies after launch

- Download the UT2k4 installer [here](https://archive.org/download/ut2004-3369/UT2004.zip).

- Create a new bottle in Whiskey, unzip the contents of the ut2004 installer into the bottle's C:\Program Files (x86) directory.

- Edit the bottle's registry to include UT2004.reg file key included in the zip file.

- Launch the game from Whisky.

#### Windows
- Download the UT2k4 installer [here](https://archive.org/details/ut2004-3369).

- Launch the 64 bit version of the game.

<script>
document.addEventListener("DOMContentLoaded", function() {
    const statusElement = document.getElementById("server-status");

    fetch("https://api.grlanparty.info/status?stack_name=ut2k4")
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

