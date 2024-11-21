var map;
function initMap() {
    const origin = { lat: 44.977276, lng: -93.232266 };
    map = new google.maps.Map(document.getElementById("mapForm"), {
      zoom: 16,
      center: origin,
    });

    map.addListener("click", function(poi) {
        let poiInput = poi.latLng;
        var geocoder = new google.maps.Geocoder();

        geocoder.geocode({"location" : poiInput}, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK && results[0]) {
                document.getElementById("loc").value = results[0].formatted_address;
            }
            else {
                alert ("Geocode was not successful for the following reason: " + status);
            }
        });
    });
  } 

function autoC() {
    let search = document.getElementById("loc");
    let autoC = new google.maps.places.Autocomplete(search);
}
  
