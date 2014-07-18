$('document').ready(function() {
  console.log("Tablesorter");
  $('#myTable').tablesorter({ headers : { 0 : { filter: true} } });
