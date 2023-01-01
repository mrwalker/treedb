let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 17,
    center: new google.maps.LatLng(30.52098, -97.88927),
    mapTypeId: "satellite",
  });

  // Create a <script> tag to load inventory data
  const script = document.createElement("script");

  // Use data hosted by the treedb app; provide a callback to retrieve JSONP
  script.src =
    "http://localhost:8000/trees/json/?callback=tree_map_callback";
  document.getElementsByTagName("head")[0].appendChild(script);
}

// Set a marker for each tree
const tree_map_callback = function (results) {
  for (let i = 0; i < results.length; i++) {
    // Tree fields
    const tree_id = results[i].pk;
    const site_tree_id = results[i].fields.site_tree_id;
    const title = results[i].fields.title;
    const description = results[i].fields.description;
    const anchor = site_tree_id + " - " + title + ": " + description;
    const url = "http://localhost:8000/trees/" + tree_id + "/";

    const infowindow = new google.maps.InfoWindow({
      content: "<a href='" + url + "'>" + anchor + "</a>",
    });

    // Location
    const location_lat = results[i].fields.location_lat;
    const location_lon = results[i].fields.location_lon;
    const latLng = new google.maps.LatLng(location_lat, location_lon);

    const marker = new google.maps.Marker({
      position: latLng,
      map: map,
      title: title,
    });

    marker.addListener("click", () => {
      infowindow.open({
        anchor: marker,
        map,
        shouldFocus: false,
      });
    });
  }
};

window.initMap = initMap;
window.tree_map_callback = tree_map_callback;
