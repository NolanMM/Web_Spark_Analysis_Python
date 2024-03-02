class ChartData {
  constructor() {
    this.labels = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];
    this.datasets = [];
  }

  addDataset(label, data, backgroundColor, borderColor, borderWidth, yAxisID) {
    this.datasets.push({
      label: label,
      data: data,
      backgroundColor: backgroundColor,
      borderColor: borderColor,
      borderWidth: borderWidth,
      yAxisID: yAxisID,
    });
  }
}

function updateFlexContainer(data) {
    const valueElements = document.querySelectorAll(".flex-value");
    if (valueElements.length !== Object.keys(data).length) {
        console.error("Data length doesn't match the number of elements.");
        return;
    }
    valueElements.forEach((element, index) => {
        element.textContent = data[Object.keys(data)[index]];
    });
}

async function fetchHistoryRecordFromServer() {
    try {
        const response = await fetch('/AnalysisDetails', {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        //salesData.datasets[0].data = data.monthlySales;
        //myChartSales.update();
        return data;
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
        const videoIDCell = document.createElement("td");
        videoIDCell.textContent = rowData.VideoID;
        row.appendChild(videoIDCell);

        const videoTitleCell = document.createElement("td");
        videoTitleCell.textContent = rowData.VideoTitle;
        row.appendChild(videoTitleCell);

        const viewCountCell = document.createElement("td");
        viewCountCell.textContent = rowData.ViewCount;
        row.appendChild(viewCountCell);

        const likeCountCell = document.createElement("td");
        likeCountCell.textContent = rowData.LikeCount;
        row.appendChild(likeCountCell);

        const dislikeCountCell = document.createElement("td");
        dislikeCountCell.textContent = rowData.DislikesCount;
        row.appendChild(dislikeCountCell);

        const commentsCountCell = document.createElement("td");
        commentsCountCell.textContent = rowData.CommentsCount;
        row.appendChild(commentsCountCell);

        // Create "Additional Information" cell with a details link
        const additionalInfoCell = document.createElement("td");
        const detailsLink = document.createElement("a");
        detailsLink.textContent = "Details";
        detailsLink.href = `/get_data/${rowData.VideoID}`; // Assuming VideoID is unique
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
window.addEventListener("load", async function () {
    try {
        const Data = await fetchHistoryRecordFromServer();
        const channel_name = getCookie('channel_name');
        const channelNameElement = document.getElementById('channel_name');
        if (channelNameElement) {
            channelNameElement.textContent = channel_name + ' ';
        }
        const flexData = {
            "TotalViews": Data.TotalViews,
            "TotalLikes": Data.TotalLikes,
            "TotalDislikes": Data.TotalDislikes,
            "TotalEngagement": Data.TotalEngagement,
        }

        // Update flex container
        updateFlexContainer(flexData);

        // Initialize chart datasets
        const Data_Views = new ChartData();
        const Data_Likes = new ChartData();
        const Data_Dislikes = new ChartData();
        const Data_Engagement = new ChartData();

        Data_Views.addDataset(
          "Channel Views",
          Data.views,
          "rgb(16,98,1)",
          "rgb(16,98,1)",
          1,
          "y-axis-views"
        );

        Data_Likes.addDataset(
            "Total Likes",
            Data.likes,
            "rgb(5,36,190)",
            "rgb(5,36,190)",
            5,
            "y-axis-likes"
        );

        Data_Dislikes.addDataset(
            "Total Dislikes",
            Data.dislikes,
            "rgba(126,3,3,1)",
            "rgb(126,3,3)",
            5,
            "y-axis-dislikes"
        );

        // Initialize monthly views chart
        var ctxViews = document.getElementById("MonthlyViews").getContext("2d");
        var myChartViews = new Chart(ctxViews, {
          type: "bar",
          data: {
              labels: Data.labels,
              datasets: [Data_Views.datasets[0]],
          },
          options: {
            maintainAspectRatio: false,
            responsive: true,
              gridLines: {
                    display: true,
                    color: "rgba(255,255,255,1)",
                    zeroLineColor: "rgb(255,255,255)",
                    zeroLineWidth: 2,
                    width: 5,
              }
          },
        });

        // Initialize monthly likes chart
        var ctxLikes = document.getElementById("MonthlyLikes").getContext("2d");
        var myChartLikes = new Chart(ctxLikes, {
          type: "line",
          data: {
              labels: Data.labels,
              datasets: [Data_Likes.datasets[0]],
          },
          options: {
            maintainAspectRatio: false,
            responsive: true,
          },
        });

        // Initialize monthly dislikes chart
        var ctxDislikes = document.getElementById("MonthlyDislikes").getContext("2d");
        var myChartDislikes = new Chart(ctxDislikes, {
          type: "line",
          data: {
              labels: Data.labels,
              datasets: [Data_Dislikes.datasets[0]],
          },
          options: {
            maintainAspectRatio: false,
            responsive: true,
          },
        });

        // Initialize monthly engagement chart
        var ctxMonthlyEngagement = document.getElementById("MonthlyEngagement").getContext("2d");
        var myChartMonthlyEngagement = new Chart(ctxMonthlyEngagement, {
          type: "bar", // Use a line chart for sales and views
          data: {
              labels: [
                  "January",
                  "February",
                  "March",
                  "April",
                  "May",
                  "June",
                  "July",
                  "August",
                  "September",
                  "October",
                  "November",
                  "December",
              ],
            datasets: [{
              label: 'Views',
              data: Data_Views.datasets[0].data,
              backgroundColor: 'rgba(16,98,1,0.3)',
              borderColor: 'rgb(16,98,1)',
              borderWidth: 3,
                yAxisID: 'y-axis-views',
            }, {
              label: 'Likes',
              data: Data_Likes.datasets[0].data,
              type: 'line',
              fill: true,
              borderColor: 'rgb(5,36,190)',
              borderWidth: 5,
                yAxisID: 'y-axis-likes',
            }]
          },
          options: {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
                yAxes: [
                    {
                        id: "y-axis-views",
                        type: "linear",
                        position: "left",
                        ticks: {
                            beginAtZero: true,
                        },
                    },
                    {
                        id: "y-axis-likes",
                        type: "linear",
                        position: "right",
                        ticks: {
                            beginAtZero: true,
                        },
                    },
                ],
            }
          },
        });

        try {
            tableData = Data.table_data;
            await updateTable(tableData);
        } catch (error) {
            console.error("Error:", error);
        }
    } catch (error) {
        console.error("Error fetching data:", error);
    }
});

if (document.querySelectorAll(".chart-container").length === 1) {
  // Add a class for full-width layout
  document.querySelector(".chart-container").classList.add("full-width-chart");
}
document.addEventListener("DOMContentLoaded", function() {
var scrollButton = document.getElementById('scrollButton');
var page2 = document.getElementById('section2');

scrollButton.addEventListener('click', function() {
  // Smooth scrolling
  page2.scrollIntoView({ behavior: 'smooth' });
});
});

document.addEventListener("DOMContentLoaded", function() {
var backtotop = document.getElementById('backToTop');
var page1 = document.getElementById('section2');

backtotop.addEventListener('click', function() {
  // Smooth scrolling
  page1.scrollIntoView({ behavior: 'smooth' });
});
});
// Get the progress bar and the progress text


