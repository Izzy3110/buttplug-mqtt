const socket = io();
const box = document.getElementById("box");

let point = null;
let isDragging = false;
let pointYPercent = null; // Store the percentage of the Y position relative to the box height
let updateChart_interval;
let current_value;
let centerOffset = 0;
let plot;
let updateInterval = 50; // Interval in milliseconds (100ms)
let maxDataPoints = 100; // Maximum number of points to display
let data = [];

let keyPressTimer = null; // To store the timer for key press
let keyPressed = false; // To track if the key is pressed
let isSaving = false; // Flag to prevent multiple saves at once


