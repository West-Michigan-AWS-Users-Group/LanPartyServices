document.addEventListener("DOMContentLoaded", function() {
    const folders = ["open_red_alert", "quake3", "tee-worlds", "total-annihilation", "ut99"];
    const folderList = document.getElementById("folder-list");

    folders.forEach(folder => {
        const listItem = document.createElement("li");
        const link = document.createElement("a");
        link.href = `/lan_party_services/info_mirror/${folder}/index.html`;
        link.textContent = folder;
        listItem.appendChild(link);
        folderList.appendChild(listItem);
    });
});
