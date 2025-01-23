# https://github.com/alicecantsleep/new-ut2004-docker
FROM deathbydentures/ut2k4:beta6

COPY UT2004.ini /usr/src/ut2004/System/UT2004.ini
COPY entrypoint.sh /entrypoint.sh

# Regular deathmatch
CMD ["ucc-bin", "server", "DM-Morpheus3?game=XGame.xDeathMatch", "ini=UT2004.ini", "-nohomedir", "-lanplay"]

# Mutant game mode (what is this?
# CMD ["ucc-bin", "server", "DM-Deck17?game=BonusPack.xMutantGame", "ini=UT2004.ini", "-nohomedir", "-lanplay"]

# TDM Facing worlds classic
# CMD ["ucc-bin", "server", "CTF-FaceClassic?game=XGame.xCTFGame", "ini=UT2004.ini", "-nohomedir", "-lanplay"]
# with mutators
#CMD ["ucc-bin", "server", "CTF-FaceClassic?game=XGame.xCTFGame?mutator=XGame.MMutInstaGib,UnrealGame.MutLowGrav", "ini=UT2004.ini", "-nohomedir", "-lanplay"]

# bombing run
# CMD ["ucc-bin", "server", "BR-Serenity?game=XGame.xBombingRun", "ini=UT2004.ini", "-nohomedir", "-lanplay"]
# more documentation about mutators seem to work for this container, although lacledesLAN's container is not working for me
# https://github.com/LacledesLAN/gamesvr-ut2004/blob/master/Documentation/ServerSetup.md

# SkaarjPack Invastion
# CMD ["ucc-bin", "server", "DM-Antalus?game=SkaarjPack.Invasion", "ini=UT2004.ini", "-nohomedir", "-lanplay"]
