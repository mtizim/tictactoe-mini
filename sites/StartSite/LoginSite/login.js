//czyli 

async function doLoginForm() {
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
console.log(login_string);
  //POST token logging in
  const login_response = await fetch("http://localhost:8000/token", {
    method: "POST",
    body: login_string, // string or object
    headers: {
      accept: "application/json",
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
  const login_responsejsonlog = await login_response.json(); //extract JSON from the http response
  console.log(login_responsejsonlog);
//putting the player token in the storage
  var token = login_responsejsonlog.access_token;
  localStorage.clear();
  localStorage.setItem("player_token", token);  

  return false;
}
