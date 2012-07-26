$.fn.calculatePrice = function(event){
	event.preventDefault();
	value = ($('#id_credits').val()*price).toFixed(2);
	$('#value').html(value);
	$.fn.getRealPrice(event);
}

$.fn.getRealPrice = function(event){
	real_value = price.toFixed(2);
	$('#payment').children().find('input[name=amount]').attr('value',real_value);
	$('#payment').children().find('input[name=quantity]').attr('value',$('#id_credits').val());
}