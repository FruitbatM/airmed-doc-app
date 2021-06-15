//Add Google Map
function initMap() {
    // Airmed clinic location
    const airmed = {
      lat: 53.3244431, 
      lng: -6.3857893
    };
    // The map centered at Airmed
    const map = new google.maps.Map(document.getElementById('map'), {
      zoom: 8,
      center: airmed,
    });
    // Add marker
    const marker = new google.maps.Marker({
      position: airmed,
      map: map,
    });
  }