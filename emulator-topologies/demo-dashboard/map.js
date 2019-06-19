var API_HOST = "http://fgcn-peuster2.cs.upb.de:32002";  // set to a remote url if dashboard is not served by REST API server
var ERROR_ALERT = false;
var TIMESTAMP = 0;
var CONNECTED = false;
var LATENESS_UPDATE_INTERVAL = 50;
var DATA_UPDATE_INTERVAL = 1000 * 5; // seconds
var LAST_UPDATE_TIMESTAMP = 0;
FACTORY_WIDTH = 50;
FACTORY_HEIGHT = 50;
OFFSET = 20;


var SCENARIO_FACTORIES = [
    {"lbl": "eu-west1", "x": 280, "y": 20},
    {"lbl": "us-east1", "x": 100, "y": 80},
    {"lbl": "us-west1", "x": 20, "y": 50},
    {"lbl": "br-east1", "x": 160, "y": 200},
    {"lbl": "cn-east1", "x": 550, "y": 110},
    {"lbl": "au-east1", "x": 600, "y": 240}
];

var SCENARIO_SERVICES = [
    {"id": "ns10", "lbl": "NS1.0", "type": 1, "visible": true, "x": 100, "y": 80},
    {"id": "ns11", "lbl": "NS1.1", "type": 1, "visible": true, "x": 550, "y": 110},
    {"id": "ns12", "lbl": "NS1.2", "type": 1, "visible": true, "x": 280, "y": 20},
    {"id": "ns20", "lbl": "NS2.0", "type": 2, "visible": true, "x": 100, "y": 80 + OFFSET},
    {"id": "ns21", "lbl": "NS2.1", "type": 2, "visible": true, "x": 20, "y": 50},
    {"id": "ns22", "lbl": "NS2.2", "type": 2, "visible": true, "x": 600, "y": 240},
    {"id": "ns23", "lbl": "NS2.3", "type": 2, "visible": true, "x": 280, "y": 20 + OFFSET},
    {"id": "ns24", "lbl": "NS2.4", "type": 2, "visible": true, "x": 160, "y": 200}
];

function errorAjaxConnection()
{
    // only do once
    if(!ERROR_ALERT)
    {
        ERROR_ALERT = true;
        // show message
        //alert("API request failed. Is the emulator running?", function() {
        //    // callback
        //    ERROR_ALERT = false;
        //});
    }
    CONNECTED = false;
    console.error("API request failed. Is the emulator running?")
}


function live_map_init()
{
	LMAP = Raphael("live-map", "100%", "100%");
	console.log("Live-Map initialized.");
}


function draw_text_box(x, y, text, front_color, back_color, stroke_color)
{
    var lbl = LMAP.text(x, y, text).attr("fill", front_color).attr("font-weight", "bold").attr("font-size", 12);
    var box = lbl.getBBox();
    var rect = LMAP.rect(box.x, box.y, box.width, box.height).attr("fill", back_color).attr("stroke", stroke_color);
    lbl.toFront();
}


function draw_background()
{
	var imgsrc = "img/world.png";
	var sf = .3;
	var x = 0;
	var y = 0;
	var width = 2292 * sf;
	var height = 1162 * sf;
	var img = LMAP.image(imgsrc, x, y, width, height).attr("opacity", 0.6);
	ELEMENTS.push(img);
}

function draw_factories()
{
    $.each(SCENARIO_FACTORIES, function(i, f) {
        var img = LMAP.image("img/factory.png", f.x, f.y, FACTORY_WIDTH, FACTORY_HEIGHT);
        ELEMENTS.push(img);
        draw_text_box(f.x + (FACTORY_WIDTH) / 2, f.y + FACTORY_HEIGHT + 12, f.lbl, "#FFFFFF", "#E88004", "#E88004");
	});
}

function draw_services()
{
    $.each(SCENARIO_SERVICES, function(i, s) {
        font_color = "#765A82";
        back_color = "#E1D5E7";
        stroke_color = "#9673A6";
        if (s.type == 2)
        {
            font_color = "#516A8F";
            back_color = "#DAE8FC";
            stroke_color = "#6C8EBF";  
        } 
        if (s.visible) {
            draw_text_box(s.x + (FACTORY_WIDTH) / 2, s.y + FACTORY_HEIGHT + 12 + OFFSET, s.lbl, font_color, back_color, stroke_color);
        }
	});
}

function live_map_paint() 
{
	LMAP.clear();
	ELEMENTS = [];
    draw_background();
    draw_factories();
    draw_services();
    //LMAP.renderfix();
}

function update_lateness_loop() {
    lateness= (Date.now() - LAST_UPDATE_TIMESTAMP) / 1000;
    $("#lbl_lateness").text("Lateness: " + Number(lateness).toPrecision(2) + "s");
    // loop while connected
    if(CONNECTED)
        setTimeout(update_lateness_loop, LATENESS_UPDATE_INTERVAL)
}

function set_service_visible(id)
{
    $.each(SCENARIO_SERVICES, function(i, s) {
        if (s.id == id)
            s.visible = true;
    });
}

function update_model(data)
{
    console.debug(data);
    $.each(SCENARIO_SERVICES, function(i, s) {
        s.visible = false;
    });
    // update model
    $.each(data, function(i, item) {
        if (item.instance_name == "eu.5gtango.tng-smpilot-ns1-emulator.0.1-inst.0")
            set_service_visible("ns10");
        if (item.instance_name == "eu.5gtango.tng-smpilot-ns1-emulator.0.1-inst.1")
            set_service_visible("ns11");
        if (item.instance_name == "eu.5gtango.tng-smpilot-ns1-emulator.0.1-inst.2")
            set_service_visible("ns12");
        if (item.instance_name == "eu.5gtango.tng-smpilot-ns2-emulator.0.1-inst.0")
            set_service_visible("ns20");
        if (item.instance_name == "eu.5gtango.tng-smpilot-ns2-emulator.0.1-inst.1")
            set_service_visible("ns21");
        if (item.instance_name == "eu.5gtango.tng-smpilot-ns2-emulator.0.1-inst.2")
            set_service_visible("ns22");
        if (item.instance_name == "eu.5gtango.tng-smpilot-ns2-emulator.0.1-inst.3")
            set_service_visible("ns23");
        if (item.instance_name == "eu.5gtango.tng-smpilot-ns2-emulator.0.1-inst.4")
            set_service_visible("ns24");
    });
    live_map_paint();
    LAST_UPDATE_TIMESTAMP = Date.now();
}

function fetch_service_status()
{
    // do HTTP request and trigger gui update on success
    var request_url = API_HOST + "/api/v3/requests";
    console.debug("fetching from: " + request_url);
    $.getJSON(request_url,  update_model);
}


function fetch_loop()
{
    // only fetch if we are connected
    if(!CONNECTED)
        return;
    // download data
    fetch_service_status();    
    // loop while connected
    if(CONNECTED)
        setTimeout(fetch_loop, DATA_UPDATE_INTERVAL);
}


function connect()
{
    console.info("connect()");
    // get host address
    //API_HOST = "http://" + $("#text_api_host").val();
    console.debug("API address: " + API_HOST);
    // reset data
    LAST_UPDATE_TIMESTAMP = Date.now();
    CONNECTED = true;
    // restart lateness counter
    update_lateness_loop();
    // restart data fetch loop
    fetch_loop();
}


$(document).ready(function(){
	console.info("document ready");
	// init live map
	live_map_init();
    live_map_paint();
    
    $.ajaxSetup({
        "error": errorAjaxConnection
    });

    // connect
    connect();
});

//$( window ).resize(function() {
//	resizeLiveMap();
//});