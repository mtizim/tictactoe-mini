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
  //przykladowy
  //let li = document.createElement('li');
  //li.onclick = () => joinExisting("test room");
  //li.style.listStyleType = 'none'

  //roomlist.appendChild(li);

  //li.innerHTML += "test room";

  roomsdata.forEach(function (room) {
    let li = document.createElement('li');
    li.onclick = () => joinExisting(room.identifier);
    li.style.listStyleType = 'none'

    roomlist.appendChild(li);

    li.innerHTML += room.identifier;
    });



return false;
}

async function displayPlayer(){

    var host = "https://tictactoe-mini.herokuapp.com/";
    var token = localStorage.getItem("player_token");
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
  localStorage.setItem("sign", "other");
  window.location.href='../GameSite/GameSite.html'

}





//testy

async function testy1() {
        //do testów
    var host = "https://tictactoe-mini.herokuapp.com/";
    //rejestracja
    var object = {};
    object["username"] = "CHMURA";
    object["password"] = "guwnodupa";
    var username = "CHMURA";
    var password = "guwnodupa"

    var registerjson = JSON.stringify(object);
    //dla testu
    console.log(registerjson);

    const response = await fetch(host+'register', {
        method: "POST",
        body: registerjson, // string or object
        headers: {
        accept: "application/json",
        "Content-Type": "application/json",
        },
    });
    const responsemyJson = await response.json(); //extract JSON from the http response
    console.log(responsemyJson);

    //logowanie
    var login_string = `grant_type=&username=${username}&password=${password}&client_id=&client_secret=`;
    console.log(login_string);
    //POST token
    const login_response = await fetch(host+'token', {
        method: "POST",
        body: login_string, // string or object
        headers: {
        accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        },
    });
    const login_responsejsonlog = await login_response.json(); //extract JSON from the http response

    var token = login_responsejsonlog.access_token;
    console.log(token);
    console.log("token1");
    //window.localStorage.setItem("player_token", token);
    //setCookie("player_token", token, 10);
    // console.log(getCookie("player_token"));
    // console.log("token wypisany");

    //tworzenie pokoju
    var object = {};
    object["room_id"] = "przelas";
    var roomjson = JSON.stringify(object);


    console.log(object.room_id);
    //var token = window.localStorage.getItem("player_token");
    console.log(token);
    //POST new room
    const room_response = await fetch(`${host}room/${object.room_id}`, {
        method: "POST",
        body: roomjson, // string or object
        headers: {
        accept: "application/json",
        'Authorization' : 'Bearer '+ token
        },
    });
    const roomresponsejson = await room_response.json(); //extract JSON from the http response
    console.log(roomresponsejson);
    console.log("pokoj utowrozny");


  

return false;
}

async function pokoj(){
    var host = "https://tictactoe-mini.herokuapp.com/";
    var token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJDSE1VUkEiLCJleHAiOjE2NDMzOTk1ODB9.GmeQheo4MtHoxQ-8l26FZBUpl0yYiweoTuVRNLZLYQs";
    var object = {};
    object["room_id"] = "dorta";
    var roomjson = JSON.stringify(object);


    console.log(object.room_id);
    //var token = window.localStorage.getItem("player_token");
    console.log(token);
    //POST new room
    const room_response = await fetch(`${host}room/${object.room_id}`, {
        method: "POST",
        body: roomjson, // string or object
        headers: {
        accept: "application/json",
        'Authorization' : 'Bearer '+ token
        },
    });
    const roomresponsejson = await room_response.json(); //extract JSON from the http response
    console.log(roomresponsejson);
    console.log("pokoj utowrozny");
    return false;
}

async function testy2() {
        //do testów
    var host = "https://tictactoe-mini.herokuapp.com/";
    //rejestracja
    var object = {};
    object["username"] = "stringus";
    object["password"] = "blablabla";
    var username = "stringus";
    var password = "blablabla"

    var registerjson = JSON.stringify(object);
    //dla testu
    console.log(registerjson);

    const response = await fetch(host+'register', {
        method: "POST",
        body: registerjson, // string or object
        headers: {
        accept: "application/json",
        "Content-Type": "application/json",
        },
    });
    const responsemyJson = await response.json(); //extract JSON from the http response
    console.log(responsemyJson);

    //logowanie
    var login_string = `grant_type=&username=${username}&password=${password}&client_id=&client_secret=`;
    console.log(login_string);
    //POST token
    const login_response = await fetch(host+'token', {
        method: "POST",
        body: login_string, // string or object
        headers: {
        accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        },
    });
    const login_responsejsonlog = await login_response.json(); //extract JSON from the http response

    var token = login_responsejsonlog.access_token;
    console.log(token);
    console.log("token2");

return false;
}