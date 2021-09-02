let map;
let marker;

// Map Initilizer
function initMap(){

    const options = {
        zoom: 8,
        center: {lat:43.6532,lng:-79.3832}
    }

    const map = new google.maps.Map(document.getElementById('map'), options)
    const geocoder = new google.maps.Geocoder();
    const infowindow = new google.maps.InfoWindow();

    google.maps.event.addListener(map, "click", (event) => {
        if (marker != undefined){
            marker.setMap(null); 
        }
        console.log(event.latLng)
        addMarker(event.latLng, map);
        populateInfoWindow(geocoder, map, infowindow)
      });

    let locationForm = document.getElementById('location-form')

    locationForm.addEventListener('click', () => {
        geocode(geocoder, map, infowindow)
    })
}

function geocode(geocoder, map, infowindow){
    let location = document.getElementById('location').value
    console.log(location)

    axios.get('https://maps.googleapis.com/maps/api/geocode/json', {
        params:{
            address:location,
            key:'AIzaSyBE6q-p1V_4JPmbof8z0OKZ255VvfJQJeU'
        }
    }).then((response) => {
        console.log(response)

        let addressComponents = response.data.results;
        let addressComponentsOutput = '<ul class="list-group">';

        for(let i=0; i<addressComponents.length;i++){
            addressComponentsOutput += `
                <li class="list-group-item bg-dark py-1 my-1" id="${'location-list-' + i.toString()}" value="${addressComponents[i].formatted_address}"><strong>${addressComponents[i].formatted_address}</strong></li>
            `
        }
        addressComponentsOutput += '</ul>'

        document.getElementById('address-components').innerHTML = addressComponentsOutput

        for(let i=0; i<addressComponents.length;i++){
            document.getElementById(`${'location-list-' + i.toString()}`).addEventListener('click', (response) => {
                setLocationValue(document.getElementById(`${'location-list-' + i.toString()}`).getAttribute('value'))
                
                let position = {
                    lat: addressComponents[i].geometry.location.lat,
                    lng: addressComponents[i].geometry.location.lng
                }

                if (marker != undefined){
                    marker.setMap(null); 
                }

                addMarker(position, map);
                populateInfoWindow(geocoder, map, infowindow)

            })
        }

    }).catch((error) => {
        console.log(error);
    })
}

function addMarker(position, map) {
    marker = new google.maps.Marker({
      position,
      map,
    });
  }

function populateInfoWindow(geocoder, map, infowindow){
    const latlng = {
        lat: marker.getPosition().lat(),
        lng: marker.getPosition().lng()
    }

    geocoder.geocode({ location: latlng })
    .then((response) => {
      if (response.results[0]) {
        map.setZoom(10);
        map.setCenter(latlng)
        console.log(response.results[0].formatted_address)
        infowindow.setContent(`<span id="infowindowContent" style="color:black;">${response.results[0].formatted_address}</span>`);
        infowindow.open(map, marker);
        
        infowindowContent = document.getElementById('infowindowContent')
        
        document.addEventListener('click',function(e){
            if(e.target && e.target.id== 'infowindowContent'){
                setLocationValue(response.results[0].formatted_address)
             }
         });

      } else {
        window.alert("No results found");
      }
    })
    .catch((e) => window.alert("Geocoder failed due to: " + e));
}

function setLocationValue(locationValue){
    document.getElementById('location').value = locationValue
}



