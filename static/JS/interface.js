function get_settings() {
    console.log("get_settings");
    console.log(document.readyState);
    var onoff = document.getElementById("onoffcheck").checked;
    var brightness = parseInt(document.getElementById("brightslide").value);
    var idle_display = document.getElementById("setting").value;
    // console.log(brightness);
    // console.log(onoff);
    // console.log(idle_display);

    var settings_arr = [
        {"onoff": onoff},
        {"brightness":brightness},
        {"idle_display":idle_display},
    ];

    $.ajax({
        type: "POST",
        url: "/onoff/",
        data: JSON.stringify(settings_arr),
        contentType: "application/json",
        dataType:"json",
    
    });

}
