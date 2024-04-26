var map = L.map('map').setView([2.924911, 11.156187], 14);


L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var myIcon = L.icon({
    iconUrl: staticUrl,
    iconSize: [35, 35]
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
            <h4>${office.properties.name}</h4>
            <p>${office.properties.address}</p>
            <div class="phone-number">
                <a href="tel:${office.properties.phone}">${office.properties.phone}</a>
            </div>
        </div
    `
}

var officeLayer = L.geoJSON(officeList, {
    onEachFeature: showPopup,
    pointToLayer: function(feature, latlng){
        return L.marker(latlng, {icon: myIcon});
    }
});

officeLayer.addTo(map);

function populateOffice() {
    const ul = document.querySelector('.list');
    officeList.forEach((office) => {
        const li = document.createElement('li');
        const div = document.createElement('div');
        const a = document.createElement('a');
        const p = document.createElement('p');

        a.addEventListener("click", ()=>{
            flytoStore(office);
        });

        div.classList.add('office-item');
        a.innerHTML = office.properties.name;
        a.href = '#';
        p.innerHTML = office.properties.address;

        div.appendChild(a);
        div.appendChild(p);
        li.appendChild(div);
        ul.appendChild(li);
    });
}

populateOffice()

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


console.log('Valeur des données :', myDataValue);

$.ajax({
    url: '/data/',  // Remplacez par l'URL de votre vue
    method: 'GET',
    success: function(geojson) {
        // Les données sont maintenant disponibles en tant qu'objet JavaScript
        console.log(geojson);

        // Vous pouvez maintenant utiliser les données pour les afficher dans votre page
        // Par exemple, vous pouvez les ajouter à un élément de votre page :
        }
    });