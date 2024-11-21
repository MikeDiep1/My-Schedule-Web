function showBigPic(num) {
    //window.alert("got to showbigPicnumber is " + num);
    bigimage.style.zIndex = "999";
    bigpic = document.getElementById("big");
    if (parseInt(num) == 1) {
        bigimage.src = "/img/Bruininks.jpg";
        bigimage.alt = "Bruininks";
        bigimage.height = "250";
        bigimage.width = "280";
    }
    else if (parseInt(num) == 2) {
        bigimage.src = "/img/anderson.jpg";
        bigimage.alt = "Anderson";
        bigimage.height = "250";
        bigimage.width = "280";
    }
    else if (parseInt(num) == 3) {
        bigimage.src = "/img/Carlson.jpg";
        bigimage.alt = "Carlson";
        bigimage.height = "250";
        bigimage.width = "280";
    }
    else if (parseInt(num) == 4) {
        bigimage.src = "/img/Rarig.jpg";
        bigimage.alt = "Rarig";
        bigimage.height = "250";
        bigimage.width = "280";
    }
    else if (parseInt(num) == 5) {
        bigimage.src = "/img/Comedy.jpg";
        bigimage.alt = "Comedy";
        bigimage.height = "250";
        bigimage.width = "280";
    }
    else if (parseInt(num) == 6) {
        bigimage.src = "/img/Recwell.jpg";
        bigimage.alt = "RecWell";
        bigimage.height = "250";
        bigimage.width = "280";
    }
    else if (parseInt(num) == 7) {
        bigimage.src = "/img/Spyhouse.jpg";
        bigimage.alt = "Spyhouse";
        bigimage.height = "250";
        bigimage.width = "280";
    }
    else if (parseInt(num) == 8) {
        bigimage.src = "/img/Walmart.jpg";
        bigimage.alt = "Walmart";
        bigimage.height = "250";
        bigimage.width = "280";
    }
    else if (parseInt(num) == 9) {
        bigimage.src = "/img/direction.png";
        bigimage.alt = "directions";
        bigimage.height = "250";
        bigimage.width = "280";
        bigimage.style.zIndex = "1";
    }
    else {
        bigimage.src = "/img/ggophers-mascot.png";
        bigimage.alt = "GOLDY's headas*";
        bigimage.height = "250";
        bigimage.width = "280";
    }
}

function clock() {
    var dateToday = new Date();
    var hour = dateToday.getHours();
    var min = dateToday.getMinutes();
    var sec = dateToday.getSeconds();
    if (hour >= 12) {
        amPM = "PM";
        hour -= 12;
    }
    else {
        amPM = "AM";
    }
    if (hour === 0) {
        hour = 12;
    }

    document.getElementById("Hour").textContent = hour;
    document.getElementById("Minute").textContent = min;
    document.getElementById("Second").textContent = sec;
    document.getElementById("AmPM").textContent = amPM;
}
var intId = setInterval(function () { clock(); }, 1000);


navigator.geolocation.getCurrentPosition(function (pos) {
    myLocation = {
        lat: pos.coords.latitude,
        lng: pos.coords.longitude,
    };
});

var marker2;
var infowindow2;

function initMap() {
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const directionsService = new google.maps.DirectionsService();
    var myLatLng = { lat: 44.977276, lng: -93.232266 };
    var map = new google.maps.Map(document.getElementById('scheduleMap'), {
        center: myLatLng,
        zoom: 13
    });
    var geocoder = new google.maps.Geocoder(); // Create a geocoder object

    var markers = [];
    let eventTime = document.getElementsByClassName("time");
    let eventTime2 = document.getElementsByClassName("time2");
    let event2 = document.getElementsByClassName("event");
    let eventLocation = document.getElementsByClassName("location");
    for(let i = 0; i < eventLocation.length; i++) {
        markers.push(event2[i].innerText + '<br>' + eventTime[i].innerText + ' ' + eventTime2[i].innerText + '<br>' + eventLocation[i].innerText);
    }
    for(let m = 0; m < markers.length; m++) {
        geocodeAddress(geocoder, map, markers[m]);
    }

    directionsRenderer.setMap(map);
    directionsRenderer.setPanel(document.getElementById("sidebar"));

    const onChangeHandler = function () {
        calculateAndDisplayRoute(directionsService, directionsRenderer);
    };
    document.getElementById("getDir").addEventListener("click", onChangeHandler);
}

function geocodeAddress(geocoder, resultsMap, address) {
    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            resultsMap.setCenter(results[0].geometry.location);
    
            marker2 = new google.maps.Marker({
                map: resultsMap,
                position: results[0].geometry.location,
                title: address
            });
            infowindow2 = new google.maps.InfoWindow({
                content: address
            });
            google.maps.event.addListener(marker2, 'click', createWindow(resultsMap, infowindow2, marker2));
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        } //end if-then-else
    }); // end call to geocoder.geocode function
} // end geocodeAddress function

// Function to return an anonymous function that will be called when the rmarker created in the 
// geocodeAddress function is clicked	
function createWindow(rmap, rinfowindow, rmarker) {
    return function () {
        rinfowindow.open(rmap, rmarker);
    }
}

let myLocation;

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    const end = document.getElementById("myInput").value;
    var commute = document.querySelector('input[name="commute"]:checked').value;

    // Execute different functions based on the selected value
    if (commute === "Walk") {
        directionsService
            .route({
                origin: myLocation,
                destination: end,
                travelMode: google.maps.TravelMode.WALKING,
            })
            .then((response) => {
                directionsRenderer.setDirections(response);
            })
            .catch((e) => window.alert("Directions request failed due to " + e));
    } else if (commute === "Drive") {
        directionsService
            .route({
                origin: myLocation,
                destination: end,
                travelMode: google.maps.TravelMode.DRIVING,
            })
            .then((response) => {
                directionsRenderer.setDirections(response);
            })
            .catch((e) => window.alert("Directions request failed due to " + e));
    } else if (commute === "Transit") {
        directionsService
            .route({
                origin: myLocation,
                destination: end,
                travelMode: google.maps.TravelMode.TRANSIT,
            })
            .then((response) => {
                directionsRenderer.setDirections(response);
            })
            .catch((e) => window.alert("Directions request failed due to " + e));
    }
}