//Add Google Map

let map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
      center: { 
        lat: 53.3244431, 
        lng: -6.3857893
      },
      zoom: 10
    });
  }