$.ajax({
  url: "http://127.0.0.1:5000/predicted_totw",
})
.done(function( data ) {
    var offence_no = data['ATT'].length;
    var midfield_no = data['MID'].length;
    var def_no = data['DEF'].length;

    for (i=0; i<offence_no; i++){
        fillData('offence', data['ATT'][i]);
    }

    for (i=0; i<midfield_no; i++){
        fillData('midfield', data['MID'][i]);
    }

    for (i=0; i<def_no; i++){
        fillData('defence', data['DEF'][i]);
    }

    fillData('goalkeep', data['GK'][0]);
});

function fillData(position, player){
    var def = document.getElementsByClassName(position);
    var defence = def[0];

    var player_name = player[0];
    var player_photo = player[1];

    var Player = document.createElement("div");
    var Player_photo = document.createElement("div");
    Player_photo.style.backgroundImage="url("+player_photo+")";
    Player_photo.style.backgroundSize="100% 100%";
    var Player_name = document.createElement("div");
    Player_name.innerHTML = player_name;

    Player.className = "Player";
    Player_photo.className = "Player_photo";
    Player_name.className = "Player_name";
    Player.appendChild(Player_photo);
    Player.appendChild(Player_name);
    document.body.getElementsByClassName(position)[0].appendChild(Player);
}

