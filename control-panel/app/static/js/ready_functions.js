$(document).ready(function () {
  // Initialize the Flot chart
  plot = $.plot("#realtime-chart", [data], {
    series: {
      lines: {
        show: true,
        fill: true,
        lineWidth: 1, // Optional: You can control the line thickness here
      },
      points: {
        show: false, // Hide points
      },
    },
    colors: ["#00A0FF", "#22C0FF"],
    grid: {
      show: false, // Disable the grid
      backgroundColor: "black", // Set background color to black
      borderWidth: 0, // No borders
      borderColor: "transparent", // Transparent border
      hoverable: true,
      clickable: true,
    },
    xaxis: {
      mode: "time", // Time-based x-axis
      tickSize: [1, "second"], // Tick interval is 1 second
      timeformat: "%H:%M:%S", // Display time format (hours:minutes:seconds)
      color: "green", // White color for x-axis ticks
    },
    yaxis: {
      min: 0,
      max: 100,
      color: "green", // White color for y-axis ticks
    },
    legend: {
      show: false, // Disable the legend
    },
    shadowSize: 0, // No shadow
  });

  // Update the chart every 100ms (0.1s)
  updateChart_interval = setInterval(updateChart, updateInterval);

  $.each($("button[id^='btn-']"), (index, element) => {
    let percentage_button_value = parseInt($(element).attr('id').split('btn-')[1])
    let percentage_button = $(element)[0]
    percentage_button.addEventListener('click', () => {
      movePointToPercentage(percentage_button_value)
    })
  }) 
  $.each($("div[id^='btn-']"), (index, element) => {
    let percentage_button_value = parseInt($(element).attr('id').split('btn-')[1])
    let percentage_button = $(element)[0]
    percentage_button.addEventListener('click', () => {
      movePointToPercentage(percentage_button_value)
    })
  })   



});


    
  // Add event listeners for mouse actions
  document.addEventListener("mousedown", startDragging); // Start dragging when mouse button is pressed
  document.addEventListener("mouseup", stopDragging); // Stop dragging when mouse button is released
  box.addEventListener("click", movePointToMouseClick);
  box.addEventListener("mousedown", box_OnMouseDown);

  // Add event listeners for keyboard actions
  document.addEventListener("keydown", document_OnKeyDown);
  document.addEventListener("keyup", document_OnKeyUp);

  // Prevent context menu from appearing on right-click
  box.addEventListener("contextmenu", (event) => event.preventDefault());

  // Add event listeners for window actions
  window.addEventListener("resize", redrawPoint);