/* Namespace Spread */ spread = {

submitPage:function(event){
	event.preventDefault();
	$.ajax({
		url:'pages',
		type:'POST',
		data:{
			'content':$('#pagetxt').val(),
			'title':$('#pagetitle').val()
		},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('#Espaco').modal('hide');
			$('#Grade').html(data);
		}
	})
},

submitSpread:function(event){
	event.preventDefault();
	$.ajax({
		url:'spread',
		type:'POST',
		data:{'content':$('#spreadtext').val()},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$.get('twitter/post',{'content':$('#spreadtext').val()},function(data){});
			$.get('facebook/post',{'content':$('#spreadtext').val()},function(data){});
			$.fn.showMosaic();
		}
	});
},

submitEvent:function(event){
	event.preventDefault();
	$.post('calendar',$('#evento').serialize(),function(data){
		$.get('facebook/event',$('#evento').serialize(),function(data){});
		$.fn.showMosaic(); 
	});
},

submitImage:function(event){
	event.preventDefault();
},

showSpreadable:function(event){
	event.preventDefault();
	var spread_id = $('.id',this).text().trim();
	$.get('spreadable',{'id':spread_id},function(data){
		$('#Espaco').html(data).modal();
		$.fn.eventLoop();
	});
},

showEvent:function(event){
	event.preventDefault();
	var event_id = $('.id',this).text().trim();
	$.get('event',{'id':event_id},function(data){
		$('#Espaco').html(data).modal();
		$.fn.eventLoop();
	});
},

showImage:function(event){
	event.preventDefault();
	var image_id = $('.id',this).text().trim();
	$.get('image',{'id':image_id},function(data){
		$('#Espaco').html(data).modal();
		$.fn.eventLoop();
	});
},

showPageEdit:function(event){
	event.preventDefault();
	var pagedit_id = $('.id',this).text().trim();
	$.get('pageedit',{'id':pagedit_id},function(data){
		$('#Espaco').html(data).modal();
		$.fn.activateEditor();
		$.fn.eventLoop();
	});
},

savePage:function(event){
	event.preventDefault();
	var pagesave_id = $('#Espaco .id').text().trim();
	$.ajax({
		url:'pageedit',
		type:'POST',
		data:{
			'id':pagesave_id,
			'title':$('#pagetitle').val(),
			'content':$('#pagetxt').val()
		},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){ $.fn.showMosaic(); }
	});
},

spreadSpread:function(event){
	event.preventDefault();
	var object_id = $('#Espaco .id').text().trim();
	$.get('spreadspread',{'id':object_id},function(data){
		$('.spreadcontent').html(data);
		$('.send').removeClass('spread')
		.addClass('objectspread');
		$.fn.eventLoop();
	});
},

spreadObject:function(event){
	event.preventDefault();
	var object_id = $('#Espaco .id').text().trim();
	var object_token = $('#Espaco .token').text().trim();
	$.ajax({
		url:'spreadspread',
		type:'POST',
		data:{
			'id':object_id,
			'token':object_token,
			'content':$('#spreadtext').val(),
		},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$.fn.showMosaic();
		}
	});
},

showSpreaded:function(event){
	event.preventDefault();
	var spreaded_id = $('.spreadedid',this).text().trim();
	var spreaded_token = $('.spreadedtoken',this).text().trim();
	$.ajax({
		url:'spreaded',
		data:{ 
			'spreaded_id':spreaded_id,
			'spreaded_token':spreaded_token
		},
		beforeSend: function(){ $.fn.Progress('Carregando comentários') },
		success:function(data){ 
			$('#Grade').Mosaic(data);
			$.fn.eventLoop();
		}
	});
},

}
/* Namespace Play */ play = {

submitVideoInfo:function(event){
	event.preventDefault();
	$.get('expose',$('#conteudo').serialize()+'&category=0'+'&credit=0',function(data){
		$('.form').html(data);
		$('.send')
		.removeClass('postspread eventspread videospread listspread')
		.addClass('uploadspread')
		$.fn.eventLoop();
	});
},
		
submitPlay:function(event){
	event.preventDefault();
	$.post('content',{},function(data){
		$.fn.hideMenus(); 
		$('#Grade').Mosaic(data);
		$.fn.eventLoop();
	});
},

hidePlayable:function(event){
	$('#Player').tubeplayer('destroy');
	$('#Espaco').removeClass('player');
},

showPlayable:function(event){
	event.preventDefault();
	var playable_id = $('.id',this).text().trim();
	var href = $(this).attr('href');
	$.get('playable',{'id':playable_id},function(data){
		$('#Espaco').html(data).modal().addClass('player');
		$('.modal-body').addClass('player-height video');
		$.e.playerOpt['initialVideo'] = $.e.lastVideo = href;
		$.e.playerOpt['width'] = 770; $.e.playerOpt['height'] = 350;
		$("#player").tubeplayer($.e.playerOpt);
		$.fn.eventLoop();
	});
},

playNext:function(){
	$.e.position++;
	if($.e.position < $.e.videos.length){
		href = $.e.videos[$.e.position];
		$('#Player').empty().tubeplayer('destroy');
		$.e.playerOpt['initialVideo'] = href;
		$.e.playerOpt['onPlayerEnded'] = function(){ play.playNext($.e.position); };
		$('#Player').tubeplayer($.e.playerOpt);	
	}else{
		$.e.position = 0;
		play.playAgain();
	}
},

playlistObject:function(event){
	event.preventDefault();
	$('.playable,.causable').each(function(){ $.e.videos.push($(this).parent().attr('href')); });
	href = $.e.videos[0]
	$.get('templates/player.html',function(data){
		$('#Espaco').Window(data);
		$('#Espaco').css({'width':800,'height':500});
		$.e.playerOpt['initialVideo'] = $.e.lastVideo = href;
		$.e.playerOpt['onPlayerEnded'] = function(){ play.playNext($.e.position); };
		$('.player,.general').addClass($.e.control);
		$("#Player").tubeplayer($.e.playerOpt);
		$('#Espaco').on('dialogclose',function(event,ui){ $('#Player').tubeplayer('destroy'); });
		$('#Espaco').dialog('option','position','center');
		$.fn.eventLoop();
	});
},

play:function(event){
	event.preventDefault();
	$(this).removeClass('play').addClass('pause');
	$(this).html('<span class="ui-icon ui-icon-pause" > </span></a>');
	$('#Player').tubeplayer('play');
	$.fn.eventLoop();
},

pause:function(event){
	event.preventDefault();
	$(this).removeClass('pause').addClass('play');
	$(this).html('<span class="ui-icon ui-icon-play" > </span></a>');
	$('#Player').tubeplayer('pause'); 
	$.fn.eventLoop();
},

mute:function(event){
	event.preventDefault();
	$(this).removeClass('mute').addClass('unmute');
	$(this).html('<span class="ui-icon ui-icon-volume-on" > </span>');
	$('#Player').tubeplayer('mute');
	$.fn.eventLoop();
},

unmute:function(event){
	event.preventDefault();
	$(this).removeClass('unmute').addClass('mute');
	$(this).html('<span class="ui-icon ui-icon-volume-off" > </span>');
	$('#Player').tubeplayer('unmute');
	$.fn.eventLoop();
},

replay:function(event){
	event.preventDefault();
	$('#Player').empty().tubeplayer('destroy');
	$('#Message').hide();
	$('#Player').tubeplayer($.e.playerOpt);
	$('#Player,.player').show();
},

getVideoInformation:function(event){
	event.preventDefault();
	if($('.price').length) price = $('.price').val();
	else price = 'none';
	$.get('expose',$('#conteudo').serialize()+'&category='+$.e.option+'&price='+price,function(data){
		$('#conteudo').parent().html(data);
		$('#overlay').hide();
		$.fn.eventLoop();
	});
},

submitContent:function(event){
	event.preventDefault();
	$('#conteudo').submit();
},

progressHandlingFunction:function(e){
    if(e.lengthComputable) $('progress').attr({value:e.loaded,max:e.total});
},

uploadProgress:function(){
	$('#overlay').css({ height: $('#upload').height() });
	$('#overlay').show();
	myXhr = $.ajaxSettings.xhr();
	if(myXhr.upload) myXhr.upload.addEventListener('progress',$.fn.progressHandlingFunction,false);
	return myXhr;
},

finishUpload:function(data){
	$.e.token = data;
	$('#overlay').find('p').html('Upload concluído.');
	$('#Espaco').dialog('close');
	$.ajax({
		url:'/',
		data:{'feed':'feed'},
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){
			$('#Grade').Mosaic(data);
			$.fn.eventLoop();
		}
	});
	$.get('known',{'info':'user'},function(data){$('#Esquerda').html(data);}); 
},

fan:function(event){
	event.preventDefault();
	$.ajax({
		url:'fan',
		data:{'text':$('#Espaco').find('.time').text()},
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){
			$('#Grade').Mosaic(data);
			$('#Espaco').dialog('close');
			$.fn.eventLoop();
		}
	});
},

}


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
        data:{'product':$(this).find('.id').text().trim()},
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
    $.post('products',$('#product').serialize(),function(data){
        $('.modal-body').html(data);
        $.e.uploadOpt['url'] = $('#image').attr('action'); 
		$('.upload,.file').fileUpload($.e.uploadOpt);
        $.fn.eventLoop();
        //$('#Espaco').empty().dialog('destroy');
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
        success:function(data){ $('#Grade').loadMosaic(data); }
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
        data:{'id':$('#Espaco').find('.id').text().trim()},
        beforeSend:function(){ $('#Espaco').Progress(); },
        success:function(data){ $('#Grade').Mosaic(data); }
    });
}

}
