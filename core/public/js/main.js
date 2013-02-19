document.documentElement.style.overflowX = 'hidden';
//document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){
	$.ajaxSetup({cache:false});
	$('#Grade').getInitialFeed();
	$("input:submit, button", "#botoes" ).button();
	if($.e.spin == true) spin.createHelix();
	else $('#Canvas').hide();
	$.fn.eventLoop();
});