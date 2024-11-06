// const fs = require('fs').promises;



// Initialize the map and set view to London, Ontario
const map = L.map('map').setView([42.9849, -81.2453], 12);

// Add a tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Hardcoded locations of McDonald's in London, Ontario
const mcDonaldsLocations = [
    { lat: 42.981, lng: -81.249, name: "1074 Wellington Road South", node:0 },
    { lat: 42.914, lng: -81.292, name: "4350 Wellington Road South", node:1 },
    { lat: 42.950, lng: -81.217, name: "462 Wharncliffe Road", node:2 },
    { lat: 42.967, lng: -81.228, name: "330 Clarke Road", node:3 },
    { lat: 42.970, lng: -81.270, name: "61 Oxford Street West", node:4 },
    // { lat: 42.936, lng: -81.227, name: "385 Wellington Road South" },
    // { lat: 42.992, lng: -81.249, name: "151 Dundas Street" },
    // { lat: 42.951, lng: -81.231, name: "959 Hamilton Road East" },
    // { lat: 42.969, lng: -81.240, name: "1159 Highbury Avenue" },
    // { lat: 42.952, lng: -81.285, name: "1105 Wellington Road South (Walmart - White Oaks Mall)" },
    // { lat: 42.973, lng: -81.281, name: "1033 Wonderland Road South" },
    // { lat: 42.953, lng: -81.237, name: "1950 Dundas Street" }
];

// Add markers for each McDonald's location
mcDonaldsLocations.forEach(location => {
    L.marker([location.lat, location.lng])
        .addTo(map)
        .bindPopup(`<b>McDonald's</b><br>${location.name}`);
});

//get routes to load map
async function initializeMap(){
    response = await fetch("http://localhost:3000/routes")
    jsonData= await response.json()
        // defining the routes the trucks take
        firstRoute = jsonData.firstRouteToSend
        secondRoute = jsonData.secondRouteToSend

        //unnecessary now but set so that it starts drawing lines from first node
        previousNode = null
        currentNode=null
        let previousCoordinates;
        let currentCoordinates
       for (let node of firstRoute){
        // defining the node to start at first node in the route
            if(previousNode==null){
                previousNode = node
                continue
            }
            //updating coordinates to draw lines in order of how it is traveled
            mcDonaldsLocations.forEach(item =>{
                if(item.node==previousNode){
                    previousCoordinates = [item.lat,item.lng]
                    console.log(item.node)
                }
                if(item.node==node){
                    currentCoordinates= [item.lat,item.lng]
                    console.log(item.node)
                }
            })
            //draw the line and add it to the map visual
            const linePath = L.polyline([previousCoordinates, currentCoordinates], {
                color: 'blue',
                weight: 5,
                opacity: 0.7
            }).addTo(map);

            previousNode = node;
            
        }
            // reset to draw second route
            previousNode = null
            currentNode=null
            
            // do it second time (maybe make a function to do this so that it can be scaled)
            for (let node of secondRoute){  
                if(previousNode==null){
                    previousNode = node
                    continue
                }
                mcDonaldsLocations.forEach(item =>{
                    if(item.node==previousNode){
                        previousCoordinates = [item.lat,item.lng]
                    }
                    if(item.node==node){
                        currentCoordinates= [item.lat,item.lng]
                    }
                })
                const linePath = L.polyline([previousCoordinates, currentCoordinates], {
                    color: 'red',
                    weight: 5,
                    opacity: 0.7
                }).addTo(map);

                previousNode = node;
    }
}


document.addEventListener('DOMContentLoaded', async function(){
    initializeMap()
 });


// // Read the JSON file using fs
// fs.readFile('testing/routes.json', 'utf8')
//     .then(data => {
//         const jsonData = JSON.parse(data);
//         console.log(jsonData);

//        firstRoute = jsonData.firstRouteToSend
//        secondRoute = jsonData.secondRouteToSend
//         previousNode = null
//         currentNode=null
//         previousCoordinates;
//         currentCoordinates
//        for (let node in firstRoute){
//             if(previousNode==null){
//                 previousNode = node
//                 continue
//             }
//             mcDonaldsLocations.forEach(item =>{
//                 if(item.node==previousNode){
//                     previousCoordinates = [item.lat,item.lng]
//                 }
//                 if(item.node==node){
//                     currentCoordinates= [item.lat,item.lng]
//                 }
//             })
//             const linePath = L.polyline([previousCoordinates, currentCoordinates], {
//                 color: 'blue',
//                 weight: 5,
//                 opacity: 0.7
//             }).addTo(map);
//        }
//        //console.log(firstRoute,secondRoute)

    
//     })
//     .catch(error => {
//         console.error("Error loading JSON file:", error);
//     });
