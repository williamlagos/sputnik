document.documentElement.style.overflowX = 'hidden';
document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){
	if($.e.widthNow < 1280) $('body').css({'font-size':'0.8em'});
	$.ajaxSetup({cache:false});
	$('#Grade').getInitialFeed();
	$('.mosaic-block').mosaic();
	$("input:submit, button", "#botoes" ).button();
	spin.createHelix();
	$.fn.eventLoop();
});