function drawSign(board, row, col,sign){
    //var firstRow=document.getElementById("table1").rows[0];
    //var x = firstRow.insertCell(-1);
    //x.innerHTML="<img src='images/circle.png/>";
    //document.getElementById("table1").rows[0].innerHTML="<img src='images/circle.png/>";
    var img = document.createElement('img'); 
    img.src = `images/${sign}.png`;
    img.width = "91";
    img.height = "86";
    img.position = "absolute";
    document.getElementById(`${board}-${row}-${col}`).appendChild(img);

}

function getNumber(){
    var number = document.getElementById("number").value;
    return number;
}

function onCellClicked(x,y,z){
    if (!window.canClickOnBoard) {return;} 
    window.canClickOnBoard = false; 
    var moveData = {
            row: y-1,  
            column: z-1, 
            board: x-1 
    };
   var moveDatajson = JSON.stringify(moveData); 

    var move_msg = {
            name: "InMessage",
            message_type: "move",
            token: window.token,
            payload: moveDatajson
    };
    ws.send(JSON.stringify(move_msg));
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
    var room_id = "chica";
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

    var host = `ws://tictactoe-mini.herokuapp.com/room/${room_id}/${sign}`;
    //opening a websocket
    var ws = new WebSocket(host);

    ws.onmessage = function (event) { 
        var msg = JSON.parse(event.data);
        console.log(msg);

        switch(msg.name) {
            case "OutMessage":
                switch(msg.message_type){
                    case "waiting_for_registration":
                        document.getElementById("messages").innerHTML = "Waiting for other player to join";
                        var register_msg = {
                            name: "InMessage",
                            message_type: "register",
                            token: window.token
                        };
                        var side = msg.payload;
                        console.log(register_msg);
                        ws.send(JSON.stringify(register_msg));
                    
                    case "board_data":

                    case "waiting_for_move":
                        document.getElementById("messages").innerHTML = "Make a move";
                        window.canClick = true;

                    case "waiting_for_other_move":
                        document.getElementById("messages").innerHTML = "Other player is making a move";
                    case "game_ended":
                    case "game_started":
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
