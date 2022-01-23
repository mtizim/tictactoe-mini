async function doRegisterForm() {
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

  // wypisać
  for (let [k, v] of registerdata.entries()) {
    console.log(k, v);
  }

  var object = {};
  registerdata.forEach(function (v, k) {
    object[k] = v;
  });
  var registerjson = JSON.stringify(object);
  //dla testu
  console.log(registerjson);

  const response = await fetch("http://localhost:8000/register", {
    method: "POST",
    body: registerjson, // string or object
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
    },
  });
  const responsemyJson = await response.json(); //extract JSON from the http response
  console.log(responsemyJson);
  // do something with myJson

  return false;
}
