/* Namespace Create */ create = {

submitCause:function(event){
	event.preventDefault();
	if($.e.token == ''){
		alert('Selecione um vídeo para acompanhar a causa primeiro.');
		return;
	}
	serialized = $('#causas').serialize()+'&category='+$.e.option+'&token='+$.e.token;
	$.post('causes',serialized,function(data){ 
		$.fn.hideMenus();
		$('#Grade').loadMosaic(data);
	});
},

loadListContext:function(event){
	event.preventDefault();
	if($('.message').text() == 'Você não possui nenhum movimento. Gostaria de criar um?'){
		$.ajax({
			url:'movement?action=grid',
			beforeSend:$('#Espaco').Progress(),
			success:function(data){ 
				$.e.selection = true;
				$('#Grade').Mosaic(data); 
				$.fn.eventLoop(); 
			}
		});
	}else if($('.message').text().indexOf('Movimentos em aberto') != -1){
		$.ajax({
			url:'movement?view=grid',
			beforeSend:$('#Espaco').Progress(),
			success:function(data){ 
				$.e.selection = false;
				$('#Grade').Mosaic(data); 
				$.fn.eventLoop(); 
			}
		});
	}else if($('.message').text().indexOf('Programações de vídeos disponíveis') != -1){
		$.ajax({
			url:'schedule?view=grid',
			beforeSend:$('#Espaco').Progress(),
			success:function(data){
				$.e.selection = false; 
				$('#Grade').Mosaic(data); 
				$.fn.eventLoop(); 
			}
		});	
	}else{
		$.ajax({
			url:'schedule?action=grid',
			beforeSend:$('#Espaco').Progress(),
			success:function(data){ 
				$.e.selection = true;
				$('#Grade').Mosaic(data); 
				$.fn.eventLoop();
			}
		});
	}
	$.fn.hideMenus();
	$('#Espaco').dialog('close');
	selection = true;
},

loadListMosaic:function(event){
	event.preventDefault();
	title = $(this).find('h2').html();
	refer = $(this).attr('href');
	$.get(refer,{'view':refer,'title':title},function(data){
		$('#Grade').translate(0,0); $.e.marginTop = 0;
		$('#Grade').loadMosaic(data);
	});
},

openCausableSpread:function(event){
	event.preventDefault();
	object = $(this).find('.time').text();
	$.ajax({
		url:'causes',
		beforeSend:function(){ $('#Espaco').Progress(); },
		data:{'view':'grid','object':object},
		success:function(data){ $('#Grade').loadMosaic(data); }
	});
},

selectVideo:function(event){
	event.preventDefault();
	$.fn.hideMenus();
	$.post('collection',{},function(data){
		$('#Espaco').dialog('close');
		$('#Grade').empty();
		$('#Grade').html(data);
		$('.mosaic-block').mosaic();
		$('.playable').click(function(event){
			event.preventDefault();
			$.e.token = $(this).parent().attr('href');
			$.fn.showMenus();
			$('#Espaco').dialog('open');
		});
	});
},
 
openCausable:function(event){
	event.preventDefault();
	if($.e.selection) return;
	href = $(this).parent().attr('href');
	time = $(this).find('.time').parent().html();
	$.get('templates/player.html',function(data){
		$('#Espaco').Window(time+data);
		$('#Espaco').css({'width':800,'height':570});
		$.e.playerOpt['initialVideo'] = $.e.lastVideo = href;
		$('.player,.general').addClass($.e.control);
		$("#Player").tubeplayer($.e.playerOpt);
		$('#Espaco').on('dialogclose',function(event,ui){ $('#Player').tubeplayer('destroy'); });
		$('#Espaco').dialog('option','position','center');
		$.fn.eventLoop();
	});
},

}