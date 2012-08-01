/* Namespace Store */ store = {

calculatePrice:function(event){
	event.preventDefault();
	value = ($('#id_credits').val()*$.e.price).toFixed(2);
	$('#value').html(value);
	$.fn.getRealPrice(event);
},

getRealPrice:function(event){
	real_value = $.e.price.toFixed(2);
	$('#payment').children().find('input[name=amount]').attr('value',real_value);
	$('#payment').children().find('input[name=quantity]').attr('value',$('#id_credits').val());
},

openDeliverable:function(event){
	event.preventDefault();
	$.get('delivery',{'quantity':$('.title').text(),'credit':$('.description').text()},function(data){ 
		button = "<div class=\"buttons-center\"><a class=\"deliver\" style=\"width:285px;\">Calcular frete</a></div><div class=\"address\"></div>"
		$.fn.showDataContext('Comprar um produto',data);
		$('#Esquerda,#Abas').show('fade');
		$('#Espaco').css({'background':'#222','border-radius':'50px','height':$('#Canvas').height()-5});
		$('#etiquetas').css({'text-align':'center'});
		$('.header').html('Compra de Produto');
		$('.tutor').html('Aqui é possível comprar produtos com os créditos do Efforia. Eles podem ser adquiridos na barra lateral ou no painel de controle do site, localizado logo ao lado da barra de busca.')
		$('.tutor').css({'margin-top':'5%','width':'80%'}) 
		$('#id_mail_code').parent().append(button);
		$('.deliver').button();
		$('.deliver').click(function(event){
			event.preventDefault();
			$.get('correios',$('#defaultform').serialize(),function(data){
				$('.address').html(data);
			});
		});
	});
},

openProduct:function(event){
	event.preventDefault();
	$.get('products',{'product':$('.product').find('.time').text()},function(data){ 
		$('#Espaco').loadDialogT(data);
		$('.cart').click(function(event){
			event.preventDefault();
			$.post('cart',{'time':$('#Espaco').find('.time').text()},function(data){alert(data);})
		}); 
	});
},

buyMoreCredits:function(event){
	event.preventDefault();
	$.get('payment',{},function(data){
		$.fn.loadDialogT(data);
		$('#payment').children().find('input[type=image]').attr('width','240');
		$('#payment').children().find('input[type=image]').attr('src','images/paypal.png');
		$('#payment').children().find('input[type=image]').click($.fn.getRealPrice);
		$('.calculate').click($.fn.calculatePrice);
	});
},

createNewProduct:function(event){
	event.preventDefault();
	$.get('products',{'action':'creation'},function(data){
		$.fn.showDataContext('Criar um produto',data);
		$('#Esquerda,#Abas').show('fade');
		$('#Espaco').css({'background':'#222','border-radius':'50px','height':$('#Canvas').height()-5});
		$('.header').html('Publicação de um Produto')
		$('.tutor').html('Aqui é possível incluir seus produtos dentro do portal Efforia. Com isso, eles aproveitam as facilidades de frete e de divulgação nas redes sociais que o Efforia oferece.')
		$('.tutor').css({'margin-top':'35%','width':'80%'})
		$('.submit').click(function(event){
			event.preventDefault();
			action = $('#defaultform').attr('action');
			$.post(action,$('#defaultform').serialize(),function(data){/*alert(data);*/});
		});
	});
},

showProducts:function(event){
	event.preventDefault();
	$.get('products',{},function(data){$('#Grade').loadMosaic(data);});
},

showProductCart:function(event){
	event.preventDefault();
	$.get('cart',{},function(data){
		$('#Grade').loadMosaic(data);
	});
}

}