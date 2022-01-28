//czyli 

async function doLoginForm() {
  var host = "https://tictactoe-mini.herokuapp.com/";
  // (B1) FORM DATA OBJECT
  var logindata = new FormData();
  logindata.append(
    "username",
    document.getElementById("username_log").value
  );
  logindata.append(
    "password",
    document.getElementById("password_log").value
  );
 var username = logindata.get("username");
 var password = logindata.get("password");

login_string = `grant_type=&username=${username}&password=${password}&client_id=&client_secret=`;

try{
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
  localStorage.setItem("player_token", token);
  console.log(login_responsejsonlog);

}catch(err){
  //console.log(err.message);
  //alert(err.message.detail);
  alert("error");
}


  return false;
}
