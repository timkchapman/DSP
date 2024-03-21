let map;

async function initMap() {
    const position = { lat: parseFloat(latitude), lng: parseFloat(longitude) };

    // Import the required libraries
    const { Map } = await google.maps.importLibrary("maps");

    // Create a new map instance
    map = new Map(document.getElementById("map"), {
        zoom: 20,
        center: position,
        mapId: "DEMO_MAP_ID",
    });

    // Add a marker to the map
    new google.maps.Marker({
        map: map,
        position: position,
        title: "Venue",
    });
}

// Call the initMap function when the page has finished loading
document.addEventListener("DOMContentLoaded", initMap);
