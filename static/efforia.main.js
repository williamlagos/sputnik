document.documentElement.style.overflowX = 'hidden';
document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){
	if($.e.widthNow < 1280) $('body').css({'font-size':'0.8em'});
	$.ajaxSetup({cache:false});
	$('#datepicker').datepicker($.e.birthdayOpt);
	$('#start_time,#end_time').datepicker($.e.eventOption);
	$('#datepicker').datepicker('option',$.datepicker.regional['pt-BR']);
	$('#Grade').getInitialFeed();
	$('.mosaic-block').mosaic();
	$("input:submit, button", "#botoes" ).button();
	spin.createHelix();
	$.fn.eventLoop();
});