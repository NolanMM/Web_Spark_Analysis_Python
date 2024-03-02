async function fetchHistoryDataFromServer() {
    try {
        const response = await fetch('/History', {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error fetching monthly sales data:", error);
    }
}


async function updateTable(tableData) {
    const tableBody = document.getElementById("table-body");
    tableBody.innerHTML = ""; // Clear previous data before populating
    tableBody.classList.add("scrollable-table-body");
    tableData.forEach((rowData) => {
        const row = document.createElement("tr");

        // Create cells for each column
        const channelIDCell = document.createElement("td");
        channelIDCell.textContent = rowData.channel_id;
        row.appendChild(channelIDCell);

        const channelNameCell = document.createElement("td");
        channelNameCell.textContent = rowData.channel_name;
        row.appendChild(channelNameCell);

        const DateCreatedCell = document.createElement("td");
        DateCreatedCell.textContent = rowData.date_created;
        row.appendChild(DateCreatedCell);

        // Create "Additional Information" cell with a details link
        const additionalInfoCell = document.createElement("td");
        const detailsLink = document.createElement("a");
        detailsLink.textContent = "Details";
        detailsLink.href = `/AnalysisDetails`+ "?channel_id=" + rowData.channel_id + "&date_created=" + rowData.date_created + "&channel_name=" + rowData.channel_name;
        detailsLink.methods = "GET";
        additionalInfoCell.appendChild(detailsLink);
        row.appendChild(additionalInfoCell);

        // Append the row to the table body
        tableBody.appendChild(row);
    });
    // Scroll bars will appear if the table is too long
    tableBody.classList.add("scrollable-table-body");
}
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return decodeURIComponent(cookieValue);
        }
    }
    return null;
}

function setCookie(key, value) {
    let allCookies = document.cookie;
    let cookieString = key + "=" + value;
    allCookies += "; " + cookieString;
    document.cookie = allCookies;
}

window.addEventListener("load", async function () {
    try
    {
        const historyData = await fetchHistoryDataFromServer();
        await updateTable(historyData);
    }
    catch (error)
    {
        console.error("Error fetching history data:", error);
    }
});