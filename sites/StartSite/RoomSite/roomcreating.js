

async function doCreateRoom() {

  var host = "https://tictactoe-mini.herokuapp.com/";
  var roomdata = new FormData();
  roomdata.append(
    "room_id",
    document.getElementById("roomid").value
  );
  
  //circle or cross
  var sign =  document.querySelector('input[name="sign"]:checked').value;
  localStorage.setItem("sign", sign);

  var object = {};
  roomdata.forEach(function (v, k) {
    object[k] = v;
  });
  var roomjson = JSON.stringify(object);

var token = localStorage.getItem("player_token");
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
  localStorage.setItem("room_id", object.room_id);

if(roomresponsejson != null){alert(roomresponsejson.detail);}else{
    window.location.href='../GameSite/GameSite.html';
  }

  return false;
}
