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

function getNumber(){
    var number = document.getElementById("number").value;
    return number;
}

function onCellClicked(x, y, z){
    console.log("kliknieto"+x+y+z);

    if (!window.canClickOnBoard) {return;} 
    window.canClickOnBoard = false; 
    var moveData = {
            row: y-1,  
            column: z-1, 
            board: x-1 
    };
   //var moveDatajson = JSON.stringify(moveData); 

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

//onClick = function(){if (!canClickOnBoard) {return;} canClickOnBoard = false;}
 //events
    //Socket.onopen - socket connection is established.
    //Socket.onmessage - client receives data from server.

    //methods
    //Socket.send() The send(data) method transmits data using the connection.
    //Socket.close() The close() method would be used to terminate any existing connection.
    
    //tu to bedzie inaczej przekazane
async function idk() {
    var room_id = "zanana";
    var number = getNumber();

    if (number==1){
        var sign = "cross"; 
        window.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmd1cyIsImV4cCI6MTY0MzM3MzMwN30.kE8v6qFOOGL7mmKLk0wOuYaj3hz1pne1_GHOKipgYJA";
    }else{
        var sign = "other"; 
        window.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJDSE1VUkEiLCJleHAiOjE2NDMzNzI2MzF9.xP4to7Nej3inEKJuMfbpAzdARBslyPDlY8hR79jXsYM";
    }
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

                    //case "game_ended":
                    //    document.getElementById("messages").innerHTML = "Game ended";
                    //    break;
                }
        }

    };

    //do zamykania
    //ws.onclose = function() { 
    //    // websocket is closed.
    //    alert("Connection is closed..."); 
    //};
    //return false;

}
