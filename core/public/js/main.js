document.documentElement.style.overflowX = 'hidden';
//document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){
	$.ajaxSetup({cache:false});
	$('#Grade').getInitialFeed();
	$("input:submit, button", "#botoes" ).button();
	$.fn.activateInterface();
	$('#Grade').infinitescroll({
	    navSelector  : "div.navigation",            
	                   // selector for the paged navigation (it will be hidden)
	    nextSelector : "div.navigation a:first",    
	                   // selector for the NEXT link (to page 2)
	    itemSelector : "#Grade div.post"          
	                   // selector for all items you'll retrieve
	});
	$.fn.eventLoop();
});