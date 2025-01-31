# Description: This file contains the asset file paths that are uploaded to S3. first argument is local file path,
# second argument is the destination path in the S3 bucket.
asset_file_paths = [
    # Pak0 file, obtained from Quake 3 Arena
    ("quake3/baseq3/pak0.pk3", "quake3/baseq3"),
    # Total Annihilation DRM free installers
    (
        "total_annihilation/setup_total_annihilation_commander_pack_3.1_(22139).exe",
        "total_annihilation",
    ),
    (
        "total_annihilation/total_annihilation__commander_pack_en_1_3_15733.pkg",
        "total_annihilation",
    ),
    # Unreal Tournament copyrighted assets, obtained from the Unreal Tournament GOTY edition steam, and
    # zipped all required files for the game to work as a Docker server.
    ("ut99/Maps-Music-Sounds-Textures.zip", "ut99"),
    # Command and Conquer Generals: Zero Hour
    ("cnc_generals_zero_hour/cnc_generals_zero_hour.iso", "cnc_generals_zero_hour"),
    ("cnc_generals_zero_hour/genpatcher_offline.zip", "cnc_generals_zero_hour"),
]
