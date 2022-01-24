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
  console.log(leaddata);

  //generowanie listy
  let list = document.getElementById("leaderboard");
  //leaddata.forEach((item)=>{
  //let li = document.createElement("li");
  //li.innerText = item.username;
  //list.appendChild(li);

  leaddata.forEach(function (player) {
    let li = document.createElement('li');
    list.appendChild(li);

    li.innerHTML += player.username + " | score: " + player.leaderboard_data.wins;
});

return false;
}

async function displayPlayer(){

    var token = window.localStorage.getItem("player_token");
    console.log(token);

    var object = {};
    object["access_token"] = token;
    var playerjson = JSON.stringify(object);
    console.log(playerjson);
    
    const response = await fetch('http://localhost:8000/player', {
        method: 'GET',
        headers: {
        'accept' : 'application/json',
        'Authorization' : 'Bearer '+token
     }
    });
    const playerdata = await response.json(); 
    console.log(playerdata);

    document.getElementById("logged_username").innerHTML = playerdata.username;
    document.getElementById("logged_wins").innerHTML = playerdata.leaderboard_data.wins;
    //document.getElementById("yourH1_element_Id").innerHTML = "yourTextHere";


    return false;


}