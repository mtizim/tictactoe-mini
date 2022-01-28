async function generateList() {

var host = "https://tictactoe-mini.herokuapp.com/";
const response = await fetch(`${host}leaderboards`, {
    method: 'GET',
    headers: {
      'accept' : 'application/json',
      'Authorization' : 'Bearer'
    }
  });
  const leaddata = await response.json(); //extract JSON from the http response
  //const lead = JSON.parse(leaderboardjson);
  console.log(leaddata);

  //generowanie listy
  let list = document.getElementById("leaderboard");

  leaddata.forEach(function (player) {
    let li = document.createElement('li');
    list.appendChild(li);

    li.innerHTML += player.username + " | score: " + player.leaderboard_data.wins;
});

//list with active rooms
const rooms_response = await fetch(`${host}rooms/active`, {
    method: 'GET',
    headers: {
      'accept' : 'application/json',
      'Authorization' : 'Bearer'
    }
  });
  const roomsdata = await rooms_response.json(); //extract JSON from the http response
  console.log(roomsdata);

  let roomlist = document.getElementById("activerooms");

  roomsdata.forEach(function (room) {
    let li = document.createElement('ul');
    li.onclick = () => joinExisting(room.identifier);
    li.style.listStyleType = 'none'
    roomlist.appendChild(li);

    li.innerHTML += room.identifier;
    });



return false;
}

async function displayPlayer(){

    var host = "https://tictactoe-mini.herokuapp.com/";

    var token = window.localStorage.getItem("player_token");
    console.log(token);

    var object = {};
    object["access_token"] = token;
    var playerjson = JSON.stringify(object);
    console.log(playerjson);
    
    const response = await fetch(`${host}player`, {
        method: 'GET',
        headers: {
        'accept' : 'application/json',
        'Authorization' : 'Bearer '+ token
     }
    });
    const playerdata = await response.json(); 

    document.getElementById("logged_username").innerHTML = playerdata.username || "anonymous";
    document.getElementById("logged_wins").innerHTML = playerdata.leaderboard_data?.wins || 0;


    return false;


}

async function joinExisting(room_id){


  localStorage.setItem("room_id", room_id);

}