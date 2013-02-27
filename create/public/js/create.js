/* Namespace Create */ create = {

submitCause:function(event){
	event.preventDefault();
	$.ajax({
		url:'projects',
		type:'POST',
		data:$('#project').serialize(),
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('.form').html(data);
			$('.send').button('reset')
			.removeClass('projectcreate')
			.addClass('linkcreate');
			$.fn.eventLoop();
			//$.get('twitter_post',$('#project').serialize(),function(data){});
		}
	});
},

submitVideo:function(event){
	event.preventDefault();
	$('.send').button('loading');
	$('#video').submit();
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
	title = $(this).find('h2').text();
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
 
showProject:function(event){
	event.preventDefault();
	var project_id = $('.id',this).text().trim();
	var href = $(this).attr('href');
	invest = '<div style="text-align:center;"><div><a class="invests ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em; width:200px;" href="#">Ver investidores</a></div><p></p>'
	pledge = '<div><a class="pledge ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em; width:200px;" href="#">Investir nesta causa</a></div><p></p></div>'
	cred = $(this).find('.causecredits').parent().html();
	//$.get('userid',{'object':object},function(data){ $.e.lastId = data; });
	$.get('project',{'id':project_id},function(data){
		$('#Espaco').html(data).modal().addClass('player');
		//$('.modal-body').addClass('player-height');
		$.e.playerOpt['initialVideo'] = $.e.lastVideo = href;
		$.e.playerOpt['width'] = 320; $.e.playerOpt['height'] = 180;
		$("#player").tubeplayer($.e.playerOpt);
		$('#Espaco').on('dialogclose',function(event,ui){ $('#Player').tubeplayer('destroy'); });
		$.fn.eventLoop();
	});
},

pledgeCause:function(event){
	event.preventDefault();
	$.ajax({
		url:'templates/pledge.html',
		beforeSend:function(){ $('#Espaco').Progress() },
		success:function(data){
			$('#Espaco').Window(data);
			$('#other').attr('value',$.e.lastId);
			$('#cause').attr('value',$.e.lastObject);
			$.fn.eventLoop();
		}
	});
},

transferPledge:function(event){
	event.preventDefault();
	credits = $('#credits').val();
	cause = $('#cause').val();
	$.ajax({
		url:'payment',
		type:'POST',
		data:{'credit':credits},
		beforeSend:function(){ $('#Espaco').Progress() },
		success:function(data){
			if(data != ''){ alert(data); $('#Espaco').empty().dialog('destroy');
			}else{
				$.ajax({
					type:'POST',
					url:'create',
					data:{'object':cause,'credits':credits},
					success:function(data){	$('#Espaco').loadMosaic(data); }
				});
			}
			$('#Espaco').empty().dialog('destroy');
		}
	});
},

showInvests:function(event){
	event.preventDefault();
	$.ajax({
		url:'create',
		data:{'object':$.e.lastObject},
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){	$('#Espaco').loadMosaic(data); }
	});
}

}