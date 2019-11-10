$(function() {
  const url = "https://shubham-zvbj.localhost.run/";

  $.get(url + "getGraphData", function(graphData) {
    if (graphData.message == "ok") {
      var data = {
        labels: graphData.result.HourlyLineChart_X,
      
        datasets: [
          {
            label: "# of faults detected",
            lineTension: 0,
            data: graphData.result.HourlyLineChart_Y,
            backgroundColor: [
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)"
            ],
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)"
            ],
            borderWidth: 1,
            fill: false
          }
        ]
      };

      var lineData2 = {
        labels: graphData.result.HourlyTotalChart_X,
        datasets: [
          {
            label: "# of faults detected",
            lineTension: 0,
            data: graphData.result.HourlyTotalChart_Y,
            backgroundColor: [
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)"
            ],
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)"
            ],
            borderWidth: 1,
            fill: false
          }
        ]
      };

      var barData = {
        labels: graphData.result.rotatorLevelCheck_X,
        datasets: [
          {
            label: "# of faults detected",
            data: graphData.result.rotatorLevelCheck_Y,
            backgroundColor: [
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)"
            ],
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)"
            ],
            borderWidth: 1,
            fill: false
          }
        ]
      };

      var barData2 = {
        labels: graphData.result.stackLevelChart_X,
        datasets: [
          {
            label: "# of faults detected",
            data: graphData.result.stackLevelChart_Y,
            backgroundColor: [
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)"
            ],
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)"
            ],
            borderWidth: 1,
            fill: false
          }
        ]
      };

      var options = {
        scales: {
          yAxes: [
            
            {
              scaleLabel: {
                display: true,
                labelString: '# of faults detected',
                fontSize: '16'
              },
              ticks: {
                beginAtZero: true
              }
            }
          ]
        },
        legend: {
          display: false
        },
        elements: {
          point: {
            radius: 5
          }
        }
      };
      var doughnutPieData = {
        datasets: [
          {
            data: graphData.result.batchPieChart_Y,
            backgroundColor: [
              "rgba(255, 99, 132, 0.5)",
              "rgba(54, 162, 235, 0.5)",
              "rgba(255, 206, 86, 0.5)",
              "rgba(75, 192, 192, 0.5)",
              "rgba(153, 102, 255, 0.5)",
              "rgba(255, 159, 64, 0.5)"
            ],
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)"
            ]
          }
        ],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: graphData.result.batchPieChart_X
      };

      var doughnutPieData2 = {
        datasets: [
          {
            data: graphData.result.batchTotal_Y,
            backgroundColor: [
              "rgba(255, 99, 132, 0.5)",
              "rgba(54, 162, 235, 0.5)",
              "rgba(255, 206, 86, 0.5)",
              "rgba(75, 192, 192, 0.5)",
              "rgba(153, 102, 255, 0.5)",
              "rgba(255, 159, 64, 0.5)"
            ],
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)"
            ]
          }
        ],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: graphData.result.batchTotal_X
      };

      var doughnutPieOptions = {
        responsive: true,
        animation: {
          animateScale: true,
          animateRotate: true
        }
      };

      // Get context with jQuery - using jQuery's .get() method.
      if ($("#barChart").length) {
        var barChartCanvas = $("#barChart")
          .get(0)
          .getContext("2d");
        // This will get the first returned node in the jQuery collection.
        var barChart = new Chart(barChartCanvas, {
          type: "bar",
          data: barData,
          options: options
        });
      }

      if ($("#barChart2").length) {
        var barChartCanvas = $("#barChart2")
          .get(0)
          .getContext("2d");
        // This will get the first returned node in the jQuery collection.
        var barChart = new Chart(barChartCanvas, {
          type: "bar",
          data: barData2,
          options: options
        });
      }

      if ($("#lineChart").length) {
        var lineChartCanvas = $("#lineChart")
          .get(0)
          .getContext("2d");
        var lineChart = new Chart(lineChartCanvas, {
          type: "line",
          data: data,
          options: options
        });
      }

      if ($("#lineChart2").length) {
        var lineChartCanvas = $("#lineChart2")
          .get(0)
          .getContext("2d");
        var lineChart = new Chart(lineChartCanvas, {
          type: "line",
          data: lineData2,
          options: options
        });
      }

      if ($("#pieChart").length) {
        var pieChartCanvas = $("#pieChart")
          .get(0)
          .getContext("2d");
        var pieChart = new Chart(pieChartCanvas, {
          type: "pie",
          data: doughnutPieData,
          options: doughnutPieOptions
        });
      }

      if ($("#pieChart2").length) {
        var pieChartCanvas = $("#pieChart2")
          .get(0)
          .getContext("2d");
        var pieChart = new Chart(pieChartCanvas, {
          type: "pie",
          data: doughnutPieData2,
          options: doughnutPieOptions
        });
      }
    } else {
      alert("Error Occured!!");
    }
  });
});
