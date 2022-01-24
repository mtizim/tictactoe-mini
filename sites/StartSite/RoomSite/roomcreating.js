//czyli 

async function doCreateRoom() {

  var host = "https://tictactoe-mini.herokuapp.com/";
  // (B1) FORM DATA OBJECT
  var roomdata = new FormData();
  roomdata.append(
    "room_id",
    document.getElementById("roomid").value
  );
  
  //circle or cross
  var sign =  document.querySelector('input[name="sign"]:checked').value;
  
  var object = {};
  roomdata.forEach(function (v, k) {
    object[k] = v;
  });
  var roomjson = JSON.stringify(object);


console.log(object.room_id);
var token = window.localStorage.getItem("player_token");
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

  return false;
}
