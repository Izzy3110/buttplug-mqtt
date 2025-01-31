function getValueLocal() {
    let item = localStorage.getItem("current_value");
    let json_item = JSON.parse(item);
    return json_item["value"];
  }
  
  // Function to get the current timestamp in milliseconds
  function getTimestamp() {
    return new Date().getTime();
  }
  
  // Function to update the chart
  function updateChart() {
    var timestamp = getTimestamp();
    var value = getValueLocal(); // Get the new value from localStorage
  
    // Add the new data point (timestamp and value)
    data.push([timestamp, value]);
  
    // Keep only the last 'maxDataPoints' points
    if (data.length > maxDataPoints) {
      data.shift(); // Remove the first data point (scrolling effect)
    }
  
    // Calculate the new center X position (middle of the screen)
    centerOffset += updateInterval;
  
    // Redraw the chart with the updated data
    plot.setData([data]);
    plot.setupGrid();
    plot.draw();
  
    // Adjust the x-axis range to keep the chart centered on the current data
    var minTime = timestamp - (maxDataPoints * updateInterval) / 2;
    var maxTime = timestamp + (maxDataPoints * updateInterval) / 2;
  
    // Set the new x-axis range to center the chart
    plot.getAxes().xaxis.options.min = minTime;
    plot.getAxes().xaxis.options.max = maxTime;
  
    plot.setupGrid();
    plot.draw();
  }
  
  
  const movePointOnMouseMove = (event) => {
    console.log("movePointOnMouseMove")
    if($(event.target).attr('id').startsWith('btn-')) {
        return;
    }
    if (isDragging && point) {
      const rect = box.getBoundingClientRect();
      const mouseY = event.clientY - rect.top; // Get mouse Y position relative to the box
        
    
      // Restrict movement within the vertical bounds of the box
      const boundedY = Math.max(0, Math.min(mouseY - 10, rect.height - 20));
      point.style.top = `${boundedY}px`;
  
      // Store the new Y percentage
      pointYPercent = (boundedY / rect.height) * 100;
      var reversedValue = 100 - pointYPercent;
      localStorage.setItem(
        "current_value",
        JSON.stringify({ value: reversedValue }),
      );
      socket.emit("mouse_move_point", { "y%": reversedValue });
    }
  };
  
  const startDragging = (event) => {
    if (event.button === 0 && point) {
      // Left button clicked
      isDragging = true;
      document.addEventListener("mousemove", movePointOnMouseMove); // Global mousemove for dragging
    }
  };
  
  const stopDragging = () => {
    // Left button released
    isDragging = false;
    document.removeEventListener("mousemove", movePointOnMouseMove); // Remove global mousemove listener
  };

  const createPointAtValue = (y_value) => {
    const rect = box.getBoundingClientRect();
    const mouseY = y_value - rect.top; // Get mouse Y position relative to the box

    if (!point) {
      // If point doesn't exist, create it at the calculated position
      point = document.createElement("div");
      point.classList.add("point");
      point.style.left = `${rect.width / 2 - 10}px`; // Center horizontally
      point.style.top = `${mouseY - 10}px`; // Position at mouse Y
      box.appendChild(point);

      // Make the point draggable immediately after creation
      makePointDraggable(point);

      // Store the Y percentage relative to the box height
      pointYPercent = (mouseY / rect.height) * 100;
    } else {
      // If point exists, move it to the new Y position
      point.style.top = `${mouseY - 10}px`;

      // Update the stored Y percentage
      pointYPercent = (mouseY / rect.height) * 100;
    }

    var reversedValue = 100 - pointYPercent;
    localStorage.setItem(
      "current_value",
      JSON.stringify({ value: reversedValue }),
    );

    socket.emit("mouse_create_point", {
      "y%": pointYPercent,
      src: point ? "point_existed" : "point_not_existed",
    });
  };

  const createPointAtMouseClick = (event) => {
    const rect = box.getBoundingClientRect();
    const mouseY = event.clientY - rect.top; // Get mouse Y position relative to the box
  
    if (!point) {
      // If point doesn't exist, create it at the calculated position
      point = document.createElement("div");
      point.classList.add("point");
      point.style.left = `${rect.width / 2 - 10}px`; // Center horizontally
      point.style.top = `${mouseY - 10}px`; // Position at mouse Y
      box.appendChild(point);
  
      // Make the point draggable immediately after creation
      makePointDraggable(point);
  
      // Store the Y percentage relative to the box height
      pointYPercent = (mouseY / rect.height) * 100;
    } else {
      // If point exists, move it to the new Y position
      point.style.top = `${mouseY - 10}px`;
  
      // Update the stored Y percentage
      pointYPercent = (mouseY / rect.height) * 100;
    }
  
    var reversedValue = 100 - pointYPercent;
    localStorage.setItem(
      "current_value",
      JSON.stringify({ value: reversedValue }),
    );
  
    socket.emit("mouse_create_point", {
      "y%": pointYPercent,
      src: point ? "point_existed" : "point_not_existed",
    });
  };
  
  
  const movePointToPercentage = (percent) => {
    if (point) {
      const rect = box.getBoundingClientRect();
      const newY = (1 - percent / 100) * rect.height; // Invert the calculation
  
      point.style.top = `${newY - 10}px`; // Subtract 10px to center the point (adjust if needed)
      pointYPercent = percent;
  
      current_value = percent;
  
      localStorage.setItem(
        "current_value",
        JSON.stringify({ value: current_value }),
      );
  
      socket.emit("mouse_move_point", {
        "y%": percent,
        src: "button",
        target: "percentage_" + percent,
      });
    }
  };
  
  const makePointDraggable = (point) => {
    // Attach mousedown event to the point itself for dragging
    point.addEventListener("mousedown", (event) => {
      event.preventDefault();
      const rect = box.getBoundingClientRect();
      const shiftY = event.clientY - point.getBoundingClientRect().top;
      const moveAt = (pageY) => {
        const newY = pageY - rect.top - shiftY;
        const boundedY = Math.max(0, Math.min(newY, rect.height - 20));
        point.style.top = `${boundedY}px`;
  
        // Update the stored Y percentage
        pointYPercent = (boundedY / rect.height) * 100;
      };
  
      const onMouseMove = (moveEvent) => moveAt(moveEvent.clientY);
  
      document.addEventListener("mousemove", onMouseMove);
  
      document.addEventListener(
        "mouseup",
        () => {
          document.removeEventListener("mousemove", onMouseMove);
        },
        { once: true },
      );
    });
  };

  const movePointToValue = (y_value) => {
    const mouseY = y_value * $(box).height();
    let box_height = $(box).height()
    let box_width = $(box).width()
    let y_percent = y_value * 100;
    console.log(y_percent)
    console.log(mouseY)
    if (!point) {
      // If point doesn't exist, create it at the calculated position
      point = document.createElement("div");
      point.classList.add("point");
      point.style.left = `${box_width / 2 - 10}px`; // Center horizontally
      point.style.top = `${mouseY - 10}px`; // Position at mouse Y
      box.appendChild(point);

      // Make the point draggable immediately after creation
      makePointDraggable(point);

      // Store the Y percentage relative to the box height
      pointYPercent = (mouseY / rect.box_height) * 100;
    } else {
      // If point exists, move it to the new Y position
      console.log('movePointToMouseClickValue')
      point.style.top = `${mouseY - 10}px`;
      pointYPercent = (mouseY / box_height) * 100;
    }

    var reversedValue = 100 - pointYPercent;
    localStorage.setItem(
      "current_value",
      JSON.stringify({ value: reversedValue }),
    );

    // Emit point creation
    socket.emit("mouse_create_point", {
      "y%": reversedValue,
      src: point ? "point_existed" : "point_not_existed",
    });
  };

  const movePointToMouseClick = (event) => {
    const rect = box.getBoundingClientRect();
    const mouseY = event.clientY - rect.top;
    let y_percent = (event.clientY / rect.height) * 100;
  
    if (!point) {
      // If point doesn't exist, create it at the calculated position
      point = document.createElement("div");
      point.classList.add("point");
      point.style.left = `${rect.width / 2 - 10}px`; // Center horizontally
      point.style.top = `${mouseY - 10}px`; // Position at mouse Y
      box.appendChild(point);
  
      // Make the point draggable immediately after creation
      makePointDraggable(point);
  
      // Store the Y percentage relative to the box height
      pointYPercent = (mouseY / rect.height) * 100;
    } else {
      // If point exists, move it to the new Y position
      console.log('movePointToMouseClick')
      point.style.top = `${mouseY - 10}px`;
      pointYPercent = (mouseY / rect.height) * 100;
    }
  
    var reversedValue = 100 - pointYPercent;
    localStorage.setItem(
      "current_value",
      JSON.stringify({ value: reversedValue }),
    );
  
    // Emit point creation
    socket.emit("mouse_create_point", {
      "y%": reversedValue,
      src: point ? "point_existed" : "point_not_existed",
    });
  };
  
  // Redraw the point when the window is resized, adjust based on Y percentage
  const redrawPoint = () => {
    if (point && pointYPercent !== null) {
      const rect = box.getBoundingClientRect();
      const currentY = (pointYPercent / 100) * rect.height; // Recalculate Y based on the percentage
      // const currentX = parseInt(point.style.left); // Get the current X position of the point
  
      // Recalculate the left position based on the new box width
      const newX = rect.width / 2 - 10; // Center horizontally based on the new width
      point.style.left = `${newX}px`;
  
      // Recalculate the Y position based on the Y percentage
      point.style.top = `${currentY - 10}px`;
  
      var reversedValue = 100 - pointYPercent;
      localStorage.setItem(
        "current_value",
        JSON.stringify({ value: reversedValue }),
      );
  
      // Optionally, you can emit the point's new position after resizing
      socket.emit("mouse_move_point", { "y%": pointYPercent, target: "redraw" });
    }
  };
  
  
  const movePointToSavedPosition = (key) => {
    const savedPosition = localStorage.getItem("pointPosition_" + key.toString());
    // console.log(savedPosition);
    if (savedPosition && !isSaving) {
      isSaving = true; // Lock the move operation
  
      const position = JSON.parse(savedPosition);
      if (position.key === key && point) {
        point.style.left = `${position.x}px`;
        point.style.top = `${position.y}px`;
        console.log(`Point moved to saved position: ${JSON.stringify(position)}`);
      }
  
      // Unlock the move operation after the move is done
      isSaving = false;
    }
  };
  
  const document_OnKeyDown =  (event) => {
    if (keyPressed) return; // If key is already pressed, ignore subsequent keydowns
  
    if (event.key === "1" || event.key === "Numpad1") {
      keyPressed = true;
      clearTimeout(keyPressTimer);
      keyPressTimer = setTimeout(() => {
        savePointToLocalStorage(1); // Save position after 2 seconds
      }, 2000);
    }
  
    if (event.key === "2" || event.key === "Numpad2") {
      keyPressed = true;
      clearTimeout(keyPressTimer);
      keyPressTimer = setTimeout(() => {
        savePointToLocalStorage(2); // Save position after 2 seconds
      }, 2000);
    }
  
    if (event.key === "3" || event.key === "Numpad3") {
      keyPressed = true;
      clearTimeout(keyPressTimer);
      keyPressTimer = setTimeout(() => {
        savePointToLocalStorage(3); // Save position after 2 seconds
      }, 2000);
    }
  
    // Add similar cases for other keys if needed...
  }
  
  const document_OnKeyUp = (event) => {
    current_value = getValueLocal();
  
    if (keyPressed) {
      clearTimeout(keyPressTimer); // Clear the long press timer
      keyPressed = false; // Reset key press status
  
      if (event.key === "1" || event.key === "Numpad1") {
        movePointToSavedPosition(1); // Move point to saved position on short press
      }
  
      if (event.key === "2" || event.key === "Numpad2") {
        movePointToSavedPosition(2); // Move point to saved position on short press
      }
  
      if (event.key === "3" || event.key === "Numpad3") {
        movePointToSavedPosition(3); // Move point to saved position on short press
      }
  
      // Add similar cases for other keys if needed...
    }
  }
  
  const savePointToLocalStorage = (key) => {
    if (point && !isSaving) {
      isSaving = true; // Lock the save operation
  
      const rect = point.getBoundingClientRect();
      const pointPosition = {
        key: key,
        x: rect.left,
        y: rect.top,
      };
  
      // Store the position in localStorage
      localStorage.setItem(
        "pointPosition_" + key.toString(),
        JSON.stringify(pointPosition),
      );
      console.log(`Point position saved: ${JSON.stringify(pointPosition)}`);
  
      // Unlock the save operation after the save is done
      isSaving = false;
    }
  };
  
  const box_OnMouseDown = (event) => {
    
    if (event.button === 0) {
      // Left mouse button
      if (!point) {
        createPointAtMouseClick(event);
      }
      
    } else if (event.button === 2) {
      // Right mouse button
      if (point) {
        point.remove();
        point = null;
        //var reversedValue = 100 - pointYPercent;
        localStorage.setItem("current_value", JSON.stringify({ value: 0 }));
        
        socket.emit("mouse_create_point", {
          "y%": 0,
          src: "point_deleted",
        });
      }
    }
  }

let reconnectInterval = 2000; // 2 seconds
let isManuallyClosed = false; // To track if the user manually closed the connection
let reconnect_attempts = 1;
let hasReconnected = false;
function connectWebSocket() {
    socket = io();

    socket.on("connect", () => {
        if(hasReconnected) {
        console.log("WebSocket reconnected");
        socket.emit("system", {"reconnected": true})
        } else {
            console.log("WebSocket connected");
        }

    });

    socket.on("disconnect", () => {
        console.log("WebSocket disconnected, attempting to reconnect...");
        if (!isManuallyClosed) {
            console.log("reconnecting for the ("+reconnect_attempts+") in "+ reconnectInterval + "ms...")
            setTimeout(connectWebSocket, reconnectInterval);
            hasReconnected= true
            reconnect_attempts++;
        }
    });

    socket.on("connect_error", (error) => {
        // console.error("WebSocket connection error:", error);
        if (!isManuallyClosed) {
            setTimeout(connectWebSocket, reconnectInterval);
        }
    });

    // Your existing event listeners
    socket.on("mouse_move_point", (data) => {
        let inverted = 1 - data.value;
        console.log("value: " + inverted);
        if (inverted < 1) {
            if (!point) {
                createPointAtValue(inverted);
            } else {
                movePointToValue(inverted);
            }
        } else {
            if (point) {
                point.remove();
                point = null;
                localStorage.setItem("current_value", JSON.stringify({ value: 0 }));

                socket.emit("mouse_create_point", {
                    "y%": 0,
                    src: "point_deleted",
                });
            }
        }
    });
}