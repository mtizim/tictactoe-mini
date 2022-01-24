async function generateList() {

const response = await fetch('http://localhost:8000/leaderboards', {
    method: 'GET',
    headers: {
      'accept' : 'application/json',
      'Authorization' : 'Bearer'
    }
  });
  const leaddata = await response.json(); //extract JSON from the http response
  //const lead = JSON.parse(leaderboardjson);
  //generowanie listy
  let list = document.getElementById("leaderboard");

  leaddata.forEach(function (player) {
    let li = document.createElement('li');
    list.appendChild(li);

    li.innerHTML += player.username + " | score: " + player.leaderboard_data.wins;
});

return false;
}

async function displayPlayer(){

    //var i;
    //console.log("local storage");
    //for (i = 0; i < localStorage.length; i++)   {
    //    console.log(localStorage.key(i) + "=[" + localStorage.getItem(localStorage.key(i)) + "]");
    //}
    //console.log("koniec storage");

    var token = window.localStorage.getItem("player_token");
    console.log(token);
    console.log("token");

    var object = {};
    object["access_token"] = token;
    var playerjson = JSON.stringify(object);
    console.log(playerjson);
    
    const response = await fetch('http://localhost:8000/player', {
        method: 'GET',
        headers: {
        'accept' : 'application/json',
        'Authorization' : 'Bearer '+ token
     }
    });
    const playerdata = await response.json(); 
    console.log(playerdata);

    document.getElementById("logged_username").innerHTML = playerdata.username;
    document.getElementById("logged_wins").innerHTML = playerdata.leaderboard_data.wins;
    //document.getElementById("yourH1_element_Id").innerHTML = "yourTextHere";


    return false;


}