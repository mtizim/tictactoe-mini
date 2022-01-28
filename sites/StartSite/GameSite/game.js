function drawSign(board, row, col, sign){
    //var firstRow=document.getElementById("table1").rows[0];
    //var x = firstRow.insertCell(-1);
    //x.innerHTML="<img src='images/circle.png/>";
    //document.getElementById("table1").rows[0].innerHTML="<img src='images/circle.png/>";
    if(sign=="none"){return;}
    var img = document.createElement('img'); 
    img.src = `images/${sign}.png`;
    img.width = "91";
    img.height = "86";
    img.position = "absolute";
    if (document.getElementById(`${board}-${row}-${col}`).children.length < 1){
         document.getElementById(`${board}-${row}-${col}`).appendChild(img);
    }
   

}

//function getNumber(){
//    var number = document.getElementById("number").value;
//    return number;
//}

function onCellClicked(x, y, z){
    if (!window.canClickOnBoard) {return;} 
    window.canClickOnBoard = false; 
    var moveData = {
            row: y-1,  
            column: z-1, 
            board: x-1 
    };

    var move_msg = {
            name: "InMessage",
            message_type: "move",
            token: window.token,
            payload: moveData
    };
    console.log(move_msg); 
    window.ws.send(JSON.stringify(move_msg));
    return false;
}

async function sockets() {
    
    var room_id = localStorage.getItem("room_id");
    //var number = getNumber();
    var sign = localStorage.getItem("sign");
    window.token = localStorage.getItem("player_token");
    //if (number==1){
    //    var sign = "cross"; 
    //    window.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJDSE1VUkEiLCJleHAiOjE2NDMzOTk1ODB9.GmeQheo4MtHoxQ-8l26FZBUpl0yYiweoTuVRNLZLYQs";
    //}else{
    //    var sign = "other"; 
    //    window.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmd1cyIsImV4cCI6MTY0MzM5OTY1OX0.EgYKx5gvh-5HwCeZo59SvcQS2f8ideQjvTOjf20CiP4";
    //}
    console.log(window.token);
    console.log(room_id);
    document.getElementById("tx_roomname").innerHTML = room_id;
    document.getElementById("tx_opponentname").innerHTML = "waiting for a player...";

    var host = `ws://tictactoe-mini.herokuapp.com/room/${room_id}/${sign}`;
    //opening a websocket
    window.ws = new WebSocket(host);

    window.ws.onmessage = function (event) { 
        var msg = JSON.parse(event.data);
        console.log(msg);

        switch(msg.name) {
            case "OutMessage":
                switch(msg.message_type){
                    case "waiting_for_registration":
                        var info = msg.payload;
                        document.getElementById("tx_sign").innerHTML = info;
                        
                        document.getElementById("messages").innerHTML = "Waiting for other player to join";
                        var register_msg = {
                            name: "InMessage",
                            message_type: "register",
                            token: window.token
                        };
                        
                        console.log(register_msg);
                        window.ws.send(JSON.stringify(register_msg));
                        break;
                    case "game_started":
                        var info = msg.payload;
                        document.getElementById("tx_opponentname").innerHTML = info.opponent_name;

                    case "waiting_for_move":
                        console.log("czeka na ruch");
                        document.getElementById("messages").innerHTML = "Make a move";
                        window.canClickOnBoard = true;
                        break;

                    case "waiting_for_other_move":
                        document.getElementById("messages").innerHTML = "Other player is making a move";
                        break;

                    case "board_data":
                        console.log("weszlo w board data");
                        var data = msg.payload;
                        if(data == null){break;}
                        for(let i = 0; i < data.length; i++) { //board
                            for(let j = 0; j < data[i].length; j++) { //row
                                 for(let k = 0; k < data[i][j].length; k++) { //column
                                    // console.log(data[i][j][k]);
                                    drawSign(i+1, j+1, k+1, data[i][j][k]);
                                 }
                            }
                        }
                        break;
                    case "game_ended":
                        var win = msg.payload;
                        if(win.reason == "cross_won"){
                            document.getElementById("messages").innerHTML = "Cross Won!";}
                        if(win.reason == "circle_won"){
                            document.getElementById("messages").innerHTML = "Circle Won!";}
                        if(win.reason == "cross_surrender"){
                            document.getElementById("messages").innerHTML = "Cross Surrendred";}
                        if(win.reason == "circle_surrender"){
                            document.getElementById("messages").innerHTML = "Circle Surrendred";}
                        if(win.reason == "player_quit"){
                            document.getElementById("messages").innerHTML = "Player quited";}
                            


                    //case "game_ended":
                    //    document.getElementById("messages").innerHTML = "Game ended";
                    //    break;
                }
        }

    };


}

async function doSurrender(){
    var surrender_msg = {
            name: "InMessage",
            message_type: "surrender",
            token: window.token
    };
    console.log(surrender_msg); 
    window.ws.send(JSON.stringify(surrender_msg));
    
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
