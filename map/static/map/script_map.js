var map = L.map('map').setView([2.924911, 11.156187], 14);


L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var myIcon = L.icon({
    iconUrl: staticUrl,
    iconSize: [50, 50]
});

function showPopup(feature, layer){
    layer.bindPopup(makePopupcontent(feature),
    {
        closeButton: false,
        offset: L.point(0, -8)
    });
}

function makePopupcontent(office){
    return `
        <div>
            <h4>${office.properties.titre}</h4>
            <img src=${office.properties.link} alt="">
            <p>${office.properties.descrip}</p>
        </div>
    `
}


function flytoStore(office) {
    const lat = office.geometry.coordinates[1];
    const lng = office.geometry.coordinates[0];
    map.flyTo([lat, lng], 18, {
        duration: 4
    });
    setTimeout(()=>{
        L.popup({closeButton: false, offset:L.point(0, -8)})
            .setLatLng([lat, lng])
            .setContent(makePopupcontent(office))
            .openOn(map);
    }, 3000);
}


$.ajax({
    url: '/data/',  // Remplacez par l'URL de votre vue
    method: 'GET',
    success: function(geojson) {
        // Les données sont maintenant disponibles en tant qu'objet JavaScript
        console.log(geojson);

        // Vous pouvez maintenant utiliser les données pour les afficher dans votre page
        // Par exemple, vous pouvez les ajouter à un élément de votre page :
        var officeLayer = L.geoJSON(geojson, {
            onEachFeature: showPopup,
            pointToLayer: function(feature, latlng){
            return L.marker(latlng, {icon: myIcon});
            }
        });

        officeLayer.addTo(map);

        function populateOffice() {
            geojson.forEach((geojson) => {
                const a = document.getElementById(geojson.properties.id);

                a.addEventListener("click", ()=>{
                    flytoStore(geojson);
                });
            });
        }

        populateOffice()
        }
    });