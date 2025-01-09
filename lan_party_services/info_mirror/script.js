document.addEventListener("DOMContentLoaded", function() {
    const folders = ["quake3"];
    const folderList = document.getElementById("folder-list");

    folders.forEach(folder => {
        const listItem = document.createElement("li");
        const link = document.createElement("a");
        link.href = `/${folder}/`;
        link.textContent = folder;
        listItem.appendChild(link);
        folderList.appendChild(listItem);
    });
});
