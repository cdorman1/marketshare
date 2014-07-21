$('document').ready(function() {
  console.log("Tablesorter");
  $('#myTable').tablesorter();

  $("#trigger-link").click(function() { 
    // set sorting column and direction, this will sort on the first and third column the column index starts at zero 
    var sorting = [[0,0],[2,0]]; 
    // sort on the first column and third columns 
    $("table").trigger("sorton",[sorting]); 
    // return false to stop default link action 
    return false; 
  }); 
 
});
