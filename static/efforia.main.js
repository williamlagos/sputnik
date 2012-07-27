document.documentElement.style.overflowX = 'hidden';
document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){
	$.ajaxSetup({cache:false});
	$('#radio').buttonset();
	$('#id_username,#id_email,#id_last_name,#id_first_name').addClass('eraseable');
	$('#payment').children().find('input[type=image]').attr('width','240');
	$('#payment').children().find('input[type=image]').attr('src','images/paypal.png');
	$('#payment').children().find('input[type=image]').click($.fn.getRealPrice);
	$('#overlay').hide();	
	$('#datepicker').datepicker($.e.birthdayOpt);
	$('#start_time,#end_time').datepicker($.e.eventOption);
	$('#datepicker').datepicker('option',$.datepicker.regional['pt-BR']);
	$('.mosaic-block').mosaic();
	$.fn.eventLoop();
});