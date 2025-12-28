// Mapbox initialization and location handling
mapboxgl.accessToken = 'pk.eyJ1Ijoic29maXF1bCIsImEiOiJjbWpuOGZpeTQxNmtkM21xeXRiemUyaGVjIn0.8puYOnBgNmo7BGO4S_dpOg';

function initMap() {
    console.log('Initializing map...');
    const mapDiv = document.getElementById('map');
    const addressInput = document.getElementById('address');
    const latInput = document.getElementById('latitude');
    const lngInput = document.getElementById('longitude');
    const form = document.querySelector('form');

    // If no map or related elements exist, exit gracefully
    if (!mapDiv) {
        console.log('No map div found');
        return;
    }
    if (!addressInput) {
        console.log('No address input found');
        return;
    }

    console.log('Map elements found, creating map...');

    try {
        // Default to Dhaka, Bangladesh coordinates
        const defaultLocation = [90.4125, 23.8103]; // [lng, lat] for Mapbox
        
        // Initialize Mapbox map
        const map = new mapboxgl.Map({
            container: mapDiv,
            style: 'mapbox://styles/mapbox/streets-v11',
            center: defaultLocation,
            zoom: 13,
            interactive: false
        });

        console.log('Map created successfully');

        // Add marker
        const marker = new mapboxgl.Marker({ draggable: true })
            .setLngLat(defaultLocation)
            .addTo(map);

        console.log('Marker added');

        // Handle marker drag
        marker.on('dragend', function() {
            const lngLat = marker.getLngLat();
            console.log('Marker dragged to:', lngLat);
            
            if (latInput && lngInput) {
                latInput.value = lngLat.lat;
                lngInput.value = lngLat.lng;
            }
        });

        // Handle address input for geocoding
        if (addressInput) {
            let timeout;
            addressInput.addEventListener('input', function() {
                clearTimeout(timeout);
                timeout = setTimeout(() => {
                    const query = addressInput.value.trim();
                    if (query.length > 2) {
                        console.log('Geocoding query:', query);
                        
                        fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(query)}.json?access_token=${mapboxgl.accessToken}&country=BD`)
                            .then(response => response.json())
                            .then(data => {
                                console.log('Geocoding result:', data);
                                if (data.features && data.features.length > 0) {
                                    const feature = data.features[0];
                                    const [lng, lat] = feature.center;
                                    
                                    map.flyTo({ center: [lng, lat], zoom: 15 });
                                    marker.setLngLat([lng, lat]);
                                    
                                    if (latInput && lngInput) {
                                        latInput.value = lat;
                                        lngInput.value = lng;
                                    }
                                }
                            })
                            .catch(error => {
                                console.error('Geocoding error:', error);
                            });
                    }
                }, 500);
            });
        }

        // Form validation - allow submission without coordinates
        if (form) {
            form.addEventListener('submit', function(e) {
                console.log('Form submitting with coordinates:', latInput?.value, lngInput?.value);
                return true;
            });
        }

    } catch (error) {
        console.error('Error initializing map:', error);
    }
}

// Initialize map when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, checking for mapboxgl...');
    if (typeof mapboxgl !== 'undefined') {
        console.log('Mapbox GL found, initializing map');
        initMap();
    } else {
        console.error('Mapbox GL not loaded');
    }
});