
/* placeholder for reading in actual values */
function read_scraped_file() {
  return 999
}

function update_html() {
  var points_left = read_scraped_file()
  document.getElementById("demo").innerHTML = points_left;
}