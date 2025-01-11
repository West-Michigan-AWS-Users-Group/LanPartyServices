
document.addEventListener("DOMContentLoaded", function() {
    const folders = ['descent3', 'starcraft', 'ut2k4', 'ut99', 'tee_worlds', 'quake3', 'open_red_alert', 'total_annihilation'];
    const folderList = document.getElementById("folder-list");

    folders.forEach(folder => {
        const listItem = document.createElement("li");
        const link = document.createElement("a");
        link.href = `/${folder}/index.html`;
        link.textContent = folder;
        listItem.appendChild(link);
        folderList.appendChild(listItem);
    });
});
