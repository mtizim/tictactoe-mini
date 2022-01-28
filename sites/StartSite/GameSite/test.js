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