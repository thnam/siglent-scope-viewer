function reloadBypassCache() {
  // Create and update the timestamp
  const timestamp = new Date().toLocaleString();
  document.getElementById("timestamp").innerHTML = "Timestamp: " + timestamp;

  // Get the image element, with a random id
  const image = document.getElementById("screenshot");
  image.src = "scope.png?t=" + Math.random();
}

window.addEventListener('load',
  // refresh the image every 1 second
  function() {
    setInterval(() => { reloadBypassCache(); }, 1000);
  },
  false
);
