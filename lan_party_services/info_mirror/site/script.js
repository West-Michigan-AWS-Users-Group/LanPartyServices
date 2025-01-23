
    document.addEventListener("DOMContentLoaded", function() {
        const folders = ['starcraft', 'ut2k4', 'ut99', 'tee_worlds', 'quake3', 'open_red_alert', 'warhammer_40k_speed_freeks', 'total_annihilation'];
        const folderList = document.getElementById("folder-list");

        // Sort folders alphabetically
        folders.sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));

        folders.forEach(folder => {
            const listItem = document.createElement("li");
            const link = document.createElement("a");
            link.href = `/site/${folder}/index.html`;

            // Replace underscores with spaces and capitalize each word, except for specific cases
            let formattedName;
            if (folder === 'UT2K4' || folder === 'UT99') {
                formattedName = folder;
            } else {
                formattedName = folder.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
            }
            link.textContent = formattedName;

            listItem.appendChild(link);
            folderList.appendChild(listItem);
        });
    });
    