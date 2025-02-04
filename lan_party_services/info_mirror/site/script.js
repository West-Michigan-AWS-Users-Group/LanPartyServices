
        document.addEventListener("DOMContentLoaded", function() {
            const folders = ['starcraft', 'ut2k4', 'ut99', 'tee_worlds', 'quake3', 'open_red_alert', 'warhammer_40k_speed_freeks', 'api', 'nlb', 'bar', 'total_annihilation', 'cnc_generals_zero_hour'];
            const folderList = document.getElementById("folder-list");
    
            // Sort folders alphabetically
            folders.sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));
    
            folders.forEach(folder => {
                const listItem = document.createElement("li");
                const link = document.createElement("a");
                link.href = `/${folder}/index.html`;
    
                // Replace underscores with spaces and capitalize each word, except for specific cases
                let formattedName;
                if (folder === 'ut2k4') {
                    formattedName = 'Unreal Tournament 2004';
                } else if (folder === 'ut99') {
                    formattedName = 'Unreal Tournament 1999';
                } else if (folder === 'bar') {
                    formattedName = 'Beyond All Reason';
                } else if (folder === 'cnc_generals_zero_hour') {
                    formattedName = 'Command and Conquer Generals: Zero Hour';
                } else {
                    formattedName = folder.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
                }
                link.textContent = formattedName;
    
                listItem.appendChild(link);
                folderList.appendChild(listItem);
            });
        });
    