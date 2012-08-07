document.documentElement.style.overflowX = 'hidden';
document.documentElement.style.overflowY = 'hidden';

var angle = 0;

$(document).ready(function(){
	$.ajaxSetup({cache:false});
	$('#datepicker').datepicker($.e.birthdayOpt);
	$('#start_time,#end_time').datepicker($.e.eventOption);
	$('#datepicker').datepicker('option',$.datepicker.regional['pt-BR']);
	//$('#Grade').getInitialFeed();
	$('.mosaic-block').mosaic();
	$("input:submit, button", "#botoes" ).button();
	if($.e.widthNow < 1280) $('body').css({'font-size':'0.8em'});
	$.ajax({
		url:'interface.svg',
		dataType:'xml',
		success:function(xml){
			xml.getElementsByTagName("svg")[0].setAttribute('width','650');
			xml.getElementsByTagName("svg")[0].setAttribute('height','650');
			canvg('efforia',xml);
		}
	});
	$('#Canvas').on('click',function(e){
		e.preventDefault();
		angle += 45;
		$('#efforia').rotate2D(angle);
	});
	$.fn.eventLoop();
});