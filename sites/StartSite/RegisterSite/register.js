async function doRegisterForm() {

  var host = "https://tictactoe-mini.herokuapp.com/";
  // (B1) FORM DATA OBJECT
  var registerdata = new FormData();

  // (B2) APPEND FIELDS
  registerdata.append(
    "username",
    document.getElementById("username_col").value
  );
  registerdata.append(
    "password",
    document.getElementById("password_col").value
  );

  var object = {};
  registerdata.forEach(function (v, k) {
    object[k] = v;
  });
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
  console.log("registered");
 

 //silent loging in
var username = registerdata.get("username");
var password = registerdata.get("password");

login_string = `grant_type=&username=${username}&password=${password}&client_id=&client_secret=`;
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
  localStorage.setItem("player_token", token);
  //setCookie("player_token", token, 10);
  //console.log(getCookie("player_token"));
  console.log("token wypisany");



  return false;
}
