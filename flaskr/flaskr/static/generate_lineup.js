var offence_no = 3;
var midfield_no = 3;
var def_no = 4;
$(function() {
    $("#submitBtn").click(function() {
    $.ajax({
        type: "GET",
        url: $SCRIPT_ROOT + "/getplayers/",
        contentType: "application/json; charset=utf-8",
        data: { echoValue: $('input[name="echoText"]').val() },
        success: function(data) {
        $}})})})


for (i=1; i<=offence_no; i++){
var off = document.getElementsByClassName("offence");
var offence = off[0];
var Player = document.createElement("div");
var Player_photo = document.createElement("div");
var Player_name = document.createElement("div");

Player.className = "Player";
Player_photo.className = "Player_photo";
Player_name.className = "Player_name";
Player.appendChild(Player_photo);
Player.appendChild(Player_name);

Player_photo.style.background = "red";
Player_name.style.background = "green";
offence.style.background = "blue";
document.body.getElementsByClassName('offence')[0].appendChild(Player);
}

for (i=1; i<=midfield_no; i++){

var mid = document.getElementsByClassName("midfield");
var midfield = mid[0];

var Player = document.createElement("div");
var Player_photo = document.createElement("div");
var Player_name = document.createElement("div");

Player.className = "Player";
Player_photo.className = "Player_photo";
Player_name.className = "Player_name";
Player.appendChild(Player_photo);
Player.appendChild(Player_name);

Player_photo.style.background = "red";
Player_name.style.background = "green";

midfield.style.background = "blue";
document.body.getElementsByClassName('midfield')[0].appendChild(Player);
}

for (i=1; i<=def_no; i++){

var def = document.getElementsByClassName("defence");
var defence = def[0];

var Player = document.createElement("div");
var Player_photo = document.createElement("div");
var Player_name = document.createElement("div");

Player.className = "Player";
Player_photo.className = "Player_photo";
Player_name.className = "Player_name";
Player.appendChild(Player_photo);
Player.appendChild(Player_name);

Player_photo.style.background = "red";
Player_name.style.background = "green";
defence.style.background = "blue";
document.body.getElementsByClassName('defence')[0].appendChild(Player);
}

var goa = document.getElementsByClassName("goalkeep");
var goalkeep = goa[0];

var Player = document.createElement("div");
var Player_photo = document.createElement("div");
var Player_name = document.createElement("div");

Player.className = "Player";
Player_photo.className = "Player_photo";
Player_name.className = "Player_name";
Player.appendChild(Player_photo);
Player.appendChild(Player_name);

Player_photo.style.background = "red";
Player_name.style.background = "green";
goalkeep.style.background = "blue";
document.body.getElementsByClassName('goalkeep')[0].appendChild(Player);