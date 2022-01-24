async function doLogAnon() {
    var host = "https://tictactoe-mini.herokuapp.com/";

    const response = await fetch(`${host}token/anon`, {
    method: "POST",
    body: "", // string or object
    headers: {
      accept: "application/json"
    },
  });
  const responsejson = await response.json(); //extract JSON from the http response
  console.log(responsejson);

  //tutaj trzeba wrzucić token do cookiesow/storage/czegokolwiek co by zadziałało





}