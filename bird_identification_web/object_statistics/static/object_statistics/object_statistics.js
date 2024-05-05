/* 
(C) Hynek V. Svobodny, 2024

This script handles the object statistics chart and its navigation
*/



function showChart(canvas, config) {
    var options = config.options;

    // Set tooltip callback functions
    var tooltipCallbacks = options.plugins.tooltip.callbacks;
    var tooltipVariables = options.plugins.tooltip.callbackVariables;
    var luxonConfig = options.scales.x.adapters.date;
    var timeFormat = tooltipVariables.timeFormat;
    var valueUnit = tooltipVariables.valueUnit;
    tooltipCallbacks.title = (context) => luxon.DateTime.fromMillis(context[0].parsed.x, luxonConfig).toFormat(timeFormat);
    tooltipCallbacks.label = (context) => `${context.dataset.label}: ${context.parsed.y}`;


    // Define interaction functions if child timespan is present
    var childTimespan = currentTimespan.child_timespan;
    if (childTimespan) {
        
        // Sets the cursor to pointer when on active elements to show they are clickable
        // based on the example at https://stackoverflow.com/a/45150374
        options.onHover = (e, activeElements) => {
            if (activeElements.length) canvas.style.cursor = 'pointer';
            else canvas.style.cursor = 'default';
         }
        
        // Redirects to the child timespan and the clicked time
        // based on the example at https://stackoverflow.com/a/58821503
        options.onClick = (e, activeElements) => {
            if (activeElements.length) {
                var activeElement = activeElements[0];
                var time = config.data.datasets[activeElement.datasetIndex].data[activeElement.index].inputTime;
                loadNewTime(childTimespan, time);
            }
        };
    };

    // View the chart
    var chartObj = new Chart(canvas, config);
};

// Sets event handlers for a timespan form
function setTimeSelectFormHandlers(form) {
    var timespanInput = form['timespan'];
    var timeModeInput = form['time-mode'];
    var timeInput = form['time-input'];

    // Refreshes time input field type when the timespan changes
    timespanInput.onchange = () => {
        var timespanName = timespanInput.value;
        var timespan = timespansAvailable[timespanName];
        timeInput.type = timespan['input_type'];
        timeInput.value = timespan['default_time']
        timeInput.min = timespan['min_time'];
        timeInput.max = timespan['max_time'];
    };

    // Enables or disables the time input field according to whether time mode is custom or not
    var timeModeOnchange = () => {
        if (timeModeInput.value == "custom") {
            timeInput.removeAttribute('disabled');
        } else {
            timeInput.setAttribute('disabled', '');
        };
    };
    timeModeInput.forEach(e => e.onchange = timeModeOnchange)

    // Calls loadNewTime with the values from the form on submit
    form.onsubmit = () => {
        var timespan = timespanInput.value;
        var time;
        if (timeModeInput.value == 'recent') {
            time = 'recent';
        } else {
            time = timeInput.value
        };
        loadNewTime(timespan, time); // Load the page with the specified timespan and time
        return false;
    }
}

// Loads the page with the the selected time
function loadNewTime(timespan, time) {
    var url = selfURLTemplate.replace('$TIMESPAN', timespan).replace('$TIME_INPUT', time);
    location = url;
}