$(function() { 
 
  // call the tablesorter plugin 
  $("table").tablesorter({ 
 
    // initialize zebra striping and filter widgets 
    widgets: ["zebra", "filter"], 
 
    headers: { 5: { sorter: true, filter: true } }, 
 
    widgetOptions : { 
 
      // css class applied to the table row containing the filters & the inputs within that row 
      filter_cssFilter : 'tablesorter-filter', 
 
      // filter widget: If there are child rows in the table (rows with class name from "cssChildRow" option) 
      // and this option is true and a match is found anywhere in the child row, then it will make that row 
      // visible; default is false 
      filter_childRows : false, 
 
      // Set this option to true to use the filter to find text from the start of the column 
      // So typing in "a" will find "albert" but not "frank", both have a's; default is false 
      filter_startsWith : false 
 
    } 
 
  }); 
 
});
