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
        dataType:"json"
    });

}

function pwdVis() {
    var box1 = document.getElementById("sensBox1");
    var box2 = document.getElementById("sensBox2");
    var box3 = document.getElementById("sensBox3");
    
    if (box1.type === "password") {
      box1.type = "text";
    } else {
      box1.type = "password";
    }

    if (box2.type === "password") {
        box2.type = "text";
      } else {
        box2.type = "password";
      }

      if (box3.type === "password") {
        box3.type = "text";
      } else {
        box3.type = "password";
      }
  }
  
// function get_idle_image(){
//     console.log("get_ii");
//     var sel_image = document.getElementById("file_select").value;

//     var image_arr = [
//         {"selected": sel_image},
//     ];

//     $.ajax({
//         type: "POST",
//         url: "/selected/",
//         data: JSON.stringify(settings_arr),
//         contentType: "application/json",
//         dataType:"json",
//     });
// }

