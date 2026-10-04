const userLocation = document.getElementById("userLocation");
const manualContainer = document.getElementById("manual-input-container");

function getLocation() {
  if (navigator.geolocation) {
    userLocation.innerHTML = "Locating...";
    navigator.geolocation.getCurrentPosition(success, error, {
      timeout: 7000
    });
  } else { 
    userLocation.innerHTML = "Geolocation is not supported by this browser.";
    showManualInputs();
  }
}

function success(position) {
  const lat = position.coords.latitude;
  const lon = position.coords.longitude;

  userLocation.innerHTML = "Latitude: " + lat + "<br>Longitude: " + lon;
  
  // Hide manual inputs if location lookup succeeds later
  manualContainer.style.display = "none";
}

function error(err) {
  userLocation.innerHTML = "Unable to retrieve your location automatically.";
  showManualInputs();
}

function showManualInputs() {
  manualContainer.style.display = "block";
}

function submitManualCoords() {
  const lat = document.getElementById("lat").value;
  const lon = document.getElementById("lon").value;

  if (!lat || !lon) {
    alert("Please enter both latitude and longitude.");
    return;
  }

  userLocation.innerHTML = "Latitude: " + lat + "<br>Longitude: " + lon;
}