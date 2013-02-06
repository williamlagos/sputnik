/* Namespace Store */ store = {

calculatePrice:function(event){
	event.preventDefault();
	value = ($('#credits').val()*$.e.price).toFixed(2);
	$('#value').attr('value',value);
	store.getRealPrice();
},

getRealPrice:function(){
	real_value = $.e.price.toFixed(2);
	$('#payment').children().find('#id_amount').attr('value',real_value);
	$('#payment').children().find('#id_quantity').attr('value',$('#credits').val());
},

calculateDelivery:function(event,callback){
	event.preventDefault();
	$.ajax({
		url:'correios',
		data:{'address':$('#id_address').val(),'object':$('.code').text()},
		beforeSend:function(){ $('.address').html('Pesquisando pelo endereço, aguarde...'); },
		success:function(data){
			$('.address').html(data);
			$('#payment').find('#id_amount').attr('value',$('.delivery').text());
			callback();
		}
	});
},

pay:function(event){
	if($('#id_amount').val() == '1.00'){
		if($('#id_address').val() == ''){
			alert('Defina o destino de sua compra primeiro.');
			event.preventDefault();
		}else{
			store.calculateDelivery(event,function(){ $.post('payment',{'credit':credits},function(data){$('#payment').find('form').submit();}); });
		}
	}
},

openDeliverable:function(event){
	event.preventDefault();
	credits = $('.description').text();
	objects = $('.time')[0].textContent;
	$.ajax({
		url:'delivery',
		data:{'quantity':$('.title').text(),'credit':credits},
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){ 
			button = "<a class=\"deliver\">Calcular frete</a><div class=\"code\" style=\"display:none;\">"+objects+"</div><div class=\"address\"></div>"
			$.fn.showMenus();
			$('#Espaco').Context(data,$('#Canvas').height()-10,$('#Canvas').width()-5);
			$('#Espaco').css({'background':'#222','border-radius':'50px','height':$('#Canvas').height()-20});
			$('.header').html('Compra de Produto');
			$('.tutor').html('Aqui é possível comprar produtos com os créditos do Efforia. Eles podem ser adquiridos na barra lateral ou no painel de controle do site, localizado logo ao lado da barra de busca. O CEP a ser informado é neste formato: 00000-000.');
			$('.tutor').css({'margin-top':'5%'}); 
			$('.image').html('<img src="images/present.png" width="80%" style="margin-left:10%;"/>');
			$('#id_address').parent().append(button);
			$('#payment').find('input[type=image]').attr('width','240');
			$('#payment').find('input[type=image]').attr('src','images/paypal.png');
			$('.deliver').button();
			$('#payment').find('input[type=image]').addClass('payment');
			$.fn.eventLoop();
		}
	});
},

openProduct:function(event){
	event.preventDefault();
	$.ajax({
		url:'products',
		data:{'product':$(this).find('.time').text()},
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){ 
			$('#Espaco').Window(data);
			$.fn.eventLoop();
		}
	});
},

buyMoreCredits:function(event){
	event.preventDefault();
	$.ajax({
		url:'payment',
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){
			$('#Espaco').Window(data);
			$('#payment').children().find('input[type=image]').attr('width','240');
			$('#payment').children().find('input[type=image]').attr('src','images/paypal.png');
			$('#payment').children().find('input[type=image]').click(store.getRealPrice);
			$.fn.eventLoop();
		}
	});
},

submitProduct:function(event){
	event.preventDefault();
	action = $('#defaultform').attr('action');
	$.post(action,$('#defaultform').serialize(),function(data){
		$('#Espaco').empty().dialog('destroy');
	});
},

showProducts:function(event){
	event.preventDefault();
	$.ajax({
		url:'products',
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){ $('#Grade').loadMosaic(data); }
	});
},

showMoreProducts:function(event){
	event.preventDefault();
	$.ajax({
		url:'products',
		data:{'more':'more'},
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){ $('#Grade').loadMosaic(data); }
	});
},

showProductCart:function(event){
	event.preventDefault();
	$.ajax({
		url:'cart',
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){	$('#Grade').loadMosaic(data); }
	});
},

cancelPurchase:function(event){
	event.preventDefault();
	$.post('cancel',{},function(data){$('#Espaco').empty().dialog('destroy'); $.fn.getInitialFeed();});
},

putOnCart:function(event){
	event.preventDefault();
	$.ajax({
		type:'POST',
		url:'cart',
		data:{'time':$('#Espaco').find('.time').text()},
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){ $('#Espaco').loadMosaic(data); }
	});
}

}