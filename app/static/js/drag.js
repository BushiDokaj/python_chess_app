function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  var square_one = document.getElementById(data).getAttribute("data-square");
  var identify = ev.target.id;
  var square_two = document.getElementById(identify).getAttribute("data-square");

  var move = {
    sq_one: square_one,
    sq_two: square_two
  };

  fetch(`${window.origin}/`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(move),
    cache: "no-cache",
    headers: new Headers({
        "content-type": "application/json"
    })
  });
}