var geo = [];

var distance = false;

var sideMenu = false;

var markers = [];

var current_position, current_accuracy;

//-- Define radius function
if (typeof (Number.prototype.toRad) === "undefined") {
    Number.prototype.toRad = function () {
        return this * Math.PI / 180;
    }
}

//-- Define degrees function
if (typeof (Number.prototype.toDeg) === "undefined") {
    Number.prototype.toDeg = function () {
        return this * (180 / Math.PI);
    }
}


function initDemoMap(){
  /*  
    if(navigator.geolocation) {
               
               // timeout at 60000 milliseconds (60 seconds)
               var options = {timeout:60000};
               navigator.geolocation.getCurrentPosition(showLocation, errorHandler, options);
            } else {
               alert("Sorry, browser does not support geolocation!");
            }*/


    var Esri_WorldImagery = L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, ' +
        'AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    });

    var Esri_DarkGreyCanvas = L.tileLayer(
        "http://{s}.sm.mapstack.stamen.com/" +
        "(toner-lite,$fff[difference],$fff[@23],$fff[hsl-saturation@20])/" +
        "{z}/{x}/{y}.png",
        {
            attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, ' +
            'NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
        }
    );
    
   var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {

	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
});
    
    var OpenStreetMap_BlackAndWhite = L.tileLayer('http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', 
                                                  
                                                  {
	
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
});

    var layers = {
        "Dark Canvas": Esri_DarkGreyCanvas,
        "Satellite": OpenStreetMap_Mapnik,
        "Grey Canvas": OpenStreetMap_BlackAndWhite
        
    };

    var map = L.map('map', {
        zoomControl: false,
        layers: [ Esri_DarkGreyCanvas ]
    });

   
			
    geocoder = L.Control.Geocoder.nominatim();
			
        control = L.Control.geocoder({
				geocoder: geocoder,
            
                placeholder:"Inserisci una localita'..",
                collapsed: false,
                errorMessage: "Nessuna località trovata!"
			
            }).addTo(map);
    
     L.control.zoom({
     
        position:'topright'
     
    }).addTo(map);
    
     var griglia = L.latlngGraticule({
    
                    showLabel: true,
            
                    color: '#00293c',
            
                    zoomInterval: [
    
                        {start: 2, end: 2, interval: 40},
                        {start: 3, end: 3, interval: 20},
                        {start: 4, end: 4, interval: 10},
                        {start: 5, end: 7, interval: 5},
                        {start: 8, end: 20, interval: 0.5}

                    ],
         
         latLineCurved: 2
     
     });
        
    var graticule = {
        
        "Graticule": griglia
    
    };
    
    
    L.control.coordinates({
			
			decimals:2,
			decimalSeperator:",",
			labelTemplateLat:"Latitude: {y}",
			labelTemplateLng:"Longitude: {x}"
		}).addTo(map);
    
    map.on('zoomend', function() {
        
        var mapZoom = map.getZoom();
     
        console.log(D01+" - "+D02+" - "+D03);
    
        if(mapZoom === zoomLevelD01 && !D01){
            
            addToMap(1);
            
        }else if(mapZoom === zoomLevelD02 && !D02){
         
            addToMap(2)
            
        }else if(mapZoom === zoomLevelD03 && !D03){
         
            addToMap(3)
            
        }
         
    });
   
    var layerControl = L.control.layers(layers, graticule);
    layerControl.addTo(map);
    
 /*   var mainMenu = L.Control.extend({
		    options: {
		        position: 'topright'
		    },

		    onAdd: function (map) {
		        this._div = L.DomUtil.create('div', 'mainMenu');
		        this._div.innerHTML = '<h3>Main Menu</h3>';

		        this._div.innerHTML += '<h4>Data:</h4> MODIS NDVI <h4>AOI:</h4> Kenya, Africa <br><br>'
		        this._div.innerHTML += '<h4>Indicator:</h4>'
		       
		        this._div.innerHTML += '<button onClick="addToMap(1)" >D01</button>';
                this._div.innerHTML += '<button onClick="addToMap(2)" >D02</button>';
                this._div.innerHTML += '<button onClick="addToMap(3)" >D03</button>';
		        return this._div;
		    },
		});
		map.addControl(new mainMenu());*/
    
    map.setView([38.476716, 10.848234], 4);

    map.on('locationfound', onLocationFound);
    map.on('locationerror', onLocationError);
    
     var marker;

   var Geodesic;
    
   var me = this;
    
    map.on('click', function(){
       
        if(sideMenu){
            
            closeNav();
            
        }
        
        
    });
    
    /*map.on('click', function(e) {
        
     
        if(distance === true){
        
        if(markers.length > 1){
         
            
            clearAll();

        }
    
			geocoder.reverse(e.latlng, map.options.crs.scale(map.getZoom()), function(results) {
				var r = results[0];
                console.log(r);
				if (r) {
					if (marker) {
						marker.
							setLatLng(r.center).
							setPopupContent(r.name).
							openPopup();
					} else {
						marker = L.marker(r.center).bindPopup(r.name).addTo(map).openPopup();
					}
				}
			});
        
        marker = new L.Marker(e.latlng, {draggable:true});
        markers.push(marker);
        map.addLayer(marker);
        marker.bindPopup("").openPopup();
        if(markers.length > 1){
          
            console.log(markers.length-2);
            console.log(markers.length-1);
            
            var lat1 = Number(markers[markers.length-2].getLatLng().lat).toFixed(2);
            var lng1 = Number(markers[markers.length-2].getLatLng().lng).toFixed(2);
            
            $('#lat_punto_1').text(lat1);
            $('#lng_punto_1').text(lng1);

            var lat2 = Number(markers[markers.length-1].getLatLng().lat).toFixed(2);
            var lng2 = Number(markers[markers.length-1].getLatLng().lng).toFixed(2);
            
            $('#lat_punto_2').text(lat2);
            $('#lng_punto_2').text(lng2);
        
            Geodesic = new L.geodesic([[markers[markers.length-2].getLatLng(), markers[markers.length-1].getLatLng()]], {
               //Geodesic = L.geodesic([[markers[0].getLatLng(), markers[1].getLatLng()]], {
			
                    weight: 5,
			
                    opacity: 1,
			
                    color: '#00293c',
			
                    steps: 50
		
                }).addTo(map);
            
            geo.push(Geodesic);
                       		    
           // me.update();

        var info = new L.control({position: 'bottomleft'});
		info.onAdd = function (map) {
		    this._div = L.DomUtil.create('div', 'info');
		    this.update();
		    return this._div;
		};
		info.update = function (props) {
		
            var distanza = (props ? (props.distance>10000)?(props.distance/1000).toFixed(0)+' km':(props.distance).toFixed(0)+' m' : 'invalid');
            
            $('#km').text(distanza);
        };
		info.addTo(map);
            
		Geodesic.update = function () {
            
            console.log("lat_lng: ");
		  
            Geodesic.setLatLngs([[markers[markers.length-2].getLatLng(), markers[markers.length-1].getLatLng()]]);
            
            var lat1 = Number(markers[markers.length-2].getLatLng().lat).toFixed(2);
            var lng1 = Number(markers[markers.length-2].getLatLng().lng).toFixed(2);
            
            $('#lat1').text(lat1);
            $('#lng1').text(lng1);

            var lat2 = Number(markers[markers.length-1].getLatLng().lat).toFixed(2);
            var lng2 = Number(markers[markers.length-1].getLatLng().lng).toFixed(2);
            
            $('#lat_punto_2').text(lat2);
            $('#lng_punto_2').text(lng2);

            info.update(Geodesic._vincenty_inverse(markers[0].getLatLng(), markers[1].getLatLng()));
		};
            
		Geodesic.update();

          
            
                markers[markers.length-2].on('drag',  Geodesic.update);
                markers[markers.length-1].on('drag',  Geodesic.update);
           
        }
        
       
        
        console.log("latitude: "+e.latlng.lat+" - longitude: "+e.latlng.lng);
        
    }
        
		});*/
    
    $('#location').click( function(e) {map.locate({setView: true, maxZoom: 12}); closeNav();} );

    $('#distance').click( function(e) { 
        
        if(distance === true){
            
             $('#distanza').css('display', 'none');
            
            distance = false;
            
            $('#map').css( 'cursor', '-webkit-grab' );
            
            clearAll();
            
            closeNav();
            
        }else{
            
            distance = true;
            
            $('#map').css( 'cursor', 'crosshair' );
            
            $('#distanza').css('display', 'block');

            closeNav();
            
        }
        
        console.log("distance: "+distance); 
    
    
    });
    
    $('#domainSelector').on('change', function(){
        
        addToMap(Number($('#domainSelector').val()));
        
    });
    
  var sidebar = L.control.sidebar({ container: 'sidebar' })
            .addTo(map);
    
    return {
        map: map,
        layerControl: layerControl
    };
}

// demo map
var mapStuff = initDemoMap();
var map = mapStuff.map;
var layerControl = mapStuff.layerControl;

var layerD01, layerD02, layerD03;

var zoomLevelD01, zoomLevelD02, zoomLevelD03;

var boundsD01, boundsD02, boundsD03;

var D01 = false, D02 = false, D03 = false;

    
var currentdate = new Date(); 

var data = currentdate.getFullYear()+""+(currentdate.getMonth()+1)+""+currentdate.getDate()

var ora;

var disp_ora;

if(currentdate.getHours() < 10){
    
    disp_ora = "0"+currentdate.getHours(); 
    
    ora = "0"+currentdate.getHours()+"00";
    
}else{
    
    disp_ora = currentdate.getHours();
    
    ora = currentdate.getHours()+"00";
    
}

$('#_data').html(currentdate.getDate()+"/"+(currentdate.getMonth()+1)+"/"+currentdate.getFullYear());

$('#_ora').html(disp_ora+":00");

var ora2 = currentdate.getHours();

var currDate= data+"Z"+ora;

//console.log("currDate: ", currDate);

getD01();

//test();

if(ora2 < 10){
    
    ora2 = "0"+ora2;
    
}

$('#dateSelector option[value='+ ora2 +']').attr("selected",true);
//$('#dateSelector option[value=' + ora + ']').prop('selected',true);

		$('#domainRefresh').on('click', function () {
            
            currentdate = parseDate($("#datepicker").val())+"Z"+$("#dateSelector").val()+"00";
        
            $('#_data').html($("#datepicker").val());

            $('#_ora').html($("#dateSelector").val()+":00");
            
		   getD01();
            
		});


$('#location').on('click', function () {

            if(navigator.geolocation) {
               
               // timeout at 60000 milliseconds (60 seconds)
               var options = {timeout:60000};
               navigator.geolocation.getCurrentPosition(showLocation);
            } else {
               alert("Sorry, browser does not support geolocation!");
            }
		});

function getD01(){
    
    removeOverLayer();
    
    $.getJSON('//193.205.230.6/products/wrf5/forecast/d01/grib/json?date='+currDate, function (data) {
   
    var corner1 = L.latLng(data[0].header.la1, data[0].header.lo1),

        corner2 = L.latLng(data[0].header.la2, data[0].header.lo2),

        bounds = L.latLngBounds(corner1, corner2);
        
        boundsD01 = bounds;

        var mid = middlePoint(Number(data[0].header.la1), Number(data[0].header.lo1), Number(data[0].header.la2), Number(data[0].header.lo2));
        
        layerD01 = L.velocityLayer({
		
            displayValues: true,
		
            displayOptions: {
			
                velocityType: 'Vento dominiop D01',
            
                displayPosition: 'bottomleft',
			
                displayEmptyString: 'No wind data'
		
            },
		
            data: data,
        
            colorScale: ["#FFFFFF", "#26E1F8", "#0917C0", "#159A00", "#169E00", "#FF9300", "#C62F00", "#AB1C8F"]
	
        });

        zoomLevelD01 = map.getBoundsZoom(bounds, false, 0);
        
        // set zoom level for d01 bounds
        
        map.fitBounds(boundsD01);
    
        layerD01.addTo(map);
        
        D01 = true;
        
        $('#geo').html("Europa");
        
        console.log("zoomLevelD01: ", zoomLevelD01);

        getD02();

});
    
}

function getD02(){
    
    $.getJSON('http://193.205.230.6/products/wrf5/forecast/d02/grib/json?date='+currDate, function (data) {
   
    var corner1 = L.latLng(data[0].header.la1, data[0].header.lo1),

        corner2 = L.latLng(data[0].header.la2, data[0].header.lo2),

        bounds = L.latLngBounds(corner1, corner2);
        
        boundsD02 = bounds;
            
    layerD02 = L.velocityLayer({
		displayValues: true,
		displayOptions: {
			velocityType: 'Vento dominiop D02',
            displayPosition: 'bottomleft',
			displayEmptyString: 'No wind data'
		},
		data: data,
        colorScale: ["#FFFFFF", "#26E1F8", "#0917C0", "#159A00", "#169E00", "#FF9300", "#C62F00", "#AB1C8F"]
	});

        //layerControl.addOverlay(layerD02, 'Wind - D02');
           
        zoomLevelD02 = map.getBoundsZoom(bounds, false, 0);
        
        console.log("zoomLevelD02: ", zoomLevelD02);
        
        getD03();

});
    
}

function getD03(){
    
    $.getJSON('http://193.205.230.6/products/wrf5/forecast/d03/grib/json?date='+currDate, function (data) {
   
    var corner1 = L.latLng(data[0].header.la1, data[0].header.lo1),

        corner2 = L.latLng(data[0].header.la2, data[0].header.lo2),

        bounds = L.latLngBounds(corner1, corner2);
        
        boundsD03 = bounds;
        
    layerD03 = L.velocityLayer({
		displayValues: true,
		displayOptions: {
			velocityType: 'Vento dominiop D03',
            displayPosition: 'bottomleft',
			displayEmptyString: 'No wind data'
		},
		data: data,
        colorScale: ["#FFFFFF", "#26E1F8", "#0917C0", "#159A00", "#169E00", "#FF9300", "#C62F00", "#AB1C8F"]
	});

        //layerControl.addOverlay(layerD03, 'Wind - D03');
        
        zoomLevelD03 = map.getBoundsZoom(bounds, false, 0);
        
        console.log("zoomLevelD03: ", zoomLevelD03);
        
});
    
}

function parseDate(data){
    
    var split = data.split("/");
    
    return split[2]+""+split[1]+""+split[0];
    
}

function showLocation(position) {
   //console.log("Latitude: " + position.coords.latitude + "<br>Longitude: " + position.coords.longitude);
    
    map.setView([position.coords.latitude, position.coords.longitude], 4);
    
}


function addToMap(value){
        
    removeOverLayer();
    
    switch(value){
            
        case 1:
    
            layerD01.addTo(map);
                
            map.fitBounds(boundsD01);
            
            D01 = true;
            
            $('#geo').html("Europa");
            
            break;

        case 2:
                        
            layerD02.addTo(map);
    
            map.fitBounds(boundsD02);

            D02 = true;
            
            $('#geo').html("Italia");
            
            break;
            
        case 3:
                    
            layerD03.addTo(map);
    
            map.fitBounds(boundsD03);

            D03 = true;
            
            $('#geo').html("Campania");
            
            break;
            
                
                }
    
    
}

function removeOverLayer(){
            
    if(layerD01 !== undefined){
          
        layerD01.remove();
        
        delete layerD01;
        
        D01 = false;
          
    }
    
    if(layerD02 !== undefined){
          
        layerD02.remove();
        
        delete layerD02;
        
        D02 = false;
        
    }
    
    if(layerD03 !== undefined){
          
        layerD03.remove();
        
        delete layerD03;
        
        D03 = false;
        
    }
    
}

//-- Define middle point function
function middlePoint(lat1, lng1, lat2, lng2) {
	
    //-- Longitude difference
    var dLng = (lng2 - lng1).toRad();

    //-- Convert to radians
    lat1 = lat1.toRad();
    lat2 = lat2.toRad();
    lng1 = lng1.toRad();

    var bX = Math.cos(lat2) * Math.cos(dLng);
    var bY = Math.cos(lat2) * Math.sin(dLng);
    var lat3 = Math.atan2(Math.sin(lat1) + Math.sin(lat2), Math.sqrt((Math.cos(lat1) + bX) * (Math.cos(lat1) + bX) + bY * bY));
    var lng3 = lng1 + Math.atan2(bY, Math.cos(lat1) + bX);

    //-- Return result
    return [lat3.toDeg(), lng3.toDeg()];
}

function onLocationFound(e) {
      // if position defined, then remove the existing position marker and accuracy circle from the map
      if (current_position) {
          map.removeLayer(current_position);
          map.removeLayer(current_accuracy);
      }

      var radius = e.accuracy / 2;

      current_position = L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + radius + " meters from this point").openPopup();

      current_accuracy = L.circle(e.latlng, radius).addTo(map);
       
    }

    
function onLocationError(e) {

    alert(e.message);
    
}

function openNav() {
    
    document.getElementById("mySidenav").style.width = "400px";
    
    sideMenu = true;
    
}

function closeNav() {

    document.getElementById("mySidenav").style.width = "0";
             
    sideMenu = false;
    
}

function clearAll(){
    
    for(var i=0; i<markers.length; i++){
                
                map.removeLayer(markers[i]);   
                
            }
             
            for(var i=0; i<geo.length; i++){
                
                map.removeLayer(geo[i]);   
                
            }
            
            geo.length = 0
            
            markers.length = 0
    
}

function test(){

    console.log('http://193.205.230.6/products/wrf5/forecast/d03/grib/json?date='+currDate);



    $.ajax({
    url: 'http://193.205.230.6/products/wrf5/forecast/d03/grib/json?date='+currDate,
 
    // The name of the callback parameter, as specified by the YQL service
    jsonp: "callback",
 
    // Tell jQuery we're expecting JSONP
    dataType: "json",
 
    
    // Work with the response
    success: function( response ) {
        console.log( response ); // server response
    },
        
         // Work with the response
    error: function( response ) {
        console.log( "error: "+JSON.stringify(response) ); // server response
    }
});
    
}

function logResults(json){
  console.log(json);
}

  
