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



async function idk() {
    
    //events
    //Socket.onopen - socket connection is established.
    //Socket.onmessage - client receives data from server.

    //methods
    //Socket.send() The send(data) method transmits data using the connection.
    //Socket.close() The close() method would be used to terminate any existing connection.

    var host = "https://tictactoe-mini.herokuapp.com/";
    //opening a websocket
    var ws = new WebSocket(host);

    ws.onopen = function() {
                  
        // Web Socket is connected, send data using send()
        //rozumiem że tutaj ma sie cos dziać jak sie połączymy
        //mozna coś wysłac
        ws.send("Message to send");
        alert("Message is sent...");
    };

    //co zrobic jak dostaniemy jakie dane z servera
    ws.onmessage = function (event) { 
        
        var msg = JSON.parse(event.data);
        switch(msg.name) {
            case "Response":


            case "":


            case "":

        }
    };


    //do zamykania
    ws.onclose = function() { 
        // websocket is closed.
        alert("Connection is closed..."); 
    };


    return false;


}