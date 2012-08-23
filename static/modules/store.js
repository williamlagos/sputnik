/* Namespace Store */ store = {

calculatePrice:function(event){
	event.preventDefault();
	value = ($('#credits').val()*$.e.price).toFixed(2);
	$('#value').html(value);
	store.getRealPrice();
},

getRealPrice:function(){
	real_value = $.e.price.toFixed(2);
	$('#payment').children().find('#id_amount').attr('value',real_value);
	$('#payment').children().find('#id_quantity').attr('value',$('#credits').val());
},

openDeliverable:function(event){
	event.preventDefault();
	$.ajax({
		url:'delivery',
		data:{'quantity':$('.title').text(),'credit':$('.description').text()},
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){ 
			button = "<a class=\"deliver\">Calcular frete</a><div></div><div class=\"address\"></div>"
			$.fn.showMenus();
			$('#Espaco').Context(data,$('#Canvas').height()-10,$('#Canvas').width()-5);
			$('#Espaco').css({'background':'#222','border-radius':'50px','height':$('#Canvas').height()-20});
			$('.header').html('Compra de Produto');
			$('.tutor').html('Aqui é possível comprar produtos com os créditos do Efforia. Eles podem ser adquiridos na barra lateral ou no painel de controle do site, localizado logo ao lado da barra de busca.');
			$('.tutor').css({'margin-top':'5%','width':'80%'}); 
			$('#id_address').parent().append(button);
			$('#payment').find('input[type=image]').attr('width','240');
			$('#payment').find('input[type=image]').attr('src','images/paypal.png');
			$('#payment').find('input[type=image]').click(store.getRealPrice);
			$('.deliver').button();
			$('.deliver').click(function(event){
				event.preventDefault();
				$.get('correios',{'address':$('#id_address').val()},function(data){
					$('.address').html(data);
					$('#id_amount').attr('value','20.00')
				});
			});
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
			$('.cart').click(function(event){
				event.preventDefault();
				$.post('cart',{'time':$('#Espaco').find('.time').text()},function(data){alert(data);})
			}); 
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

createNewProduct:function(event){
	event.preventDefault();
	$.ajax({
		url:'products',
		data:{'action':'creation'},
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){
			$('#Espaco').Context(data,$('#Canvas').height()-10,$('#Canvas').width()-5);
			$.fn.showMenus();
			$('#Espaco').css({'background':'#222','border-radius':'50px','height':$('#Canvas').height()-20});
			$('.header').html('Publicação de um Produto')
			$('.tutor').html('Aqui é possível incluir seus produtos dentro do portal Efforia. Com isso, eles aproveitam as facilidades de frete e de divulgação nas redes sociais que o Efforia oferece.');
			$('.tutor').css({'margin-top':'35%','width':'80%'})
			$('.submit').click(function(event){
				event.preventDefault();
				action = $('#defaultform').attr('action');
				$.post(action,$('#defaultform').serialize(),function(data){
					$('#Espaco').empty().dialog('destroy');
				});
			});
		}
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

showProductCart:function(event){
	event.preventDefault();
	$.ajax({
		url:'cart',
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){	$('#Grade').loadMosaic(data); }
	});
}

}