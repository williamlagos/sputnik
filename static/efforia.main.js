document.documentElement.style.overflowX = 'hidden';
document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){
	$.ajaxSetup({cache:false});
	$('#datepicker').datepicker($.e.birthdayOpt);
	$('#start_time,#end_time').datepicker($.e.eventOption);
	$('#datepicker').datepicker('option',$.datepicker.regional['pt-BR']);
	$('.mosaic-block').mosaic();
	$.fn.eventLoop();
});