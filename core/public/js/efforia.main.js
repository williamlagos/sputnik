document.documentElement.style.overflowX = 'hidden';
document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){
	$.ajaxSetup({cache:false});
	$('#Grade').getInitialFeed();
	$('.mosaic-block').mosaic();
	$("input:submit, button", "#botoes" ).button();
	spin.createHelix();
	$.fn.eventLoop();
});