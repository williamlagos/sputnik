document.documentElement.style.overflowX = "hidden"

#document.documentElement.style.overflowY = 'hidden';
$(document).ready ->
  $.ajaxSetup cache: false
  $.fn.verifyProjects()
  $("#Grade").showMosaic()
  $("input:submit, button", "#botoes").button()
  $.fn.activateInterface()
  $.fn.eventLoop()