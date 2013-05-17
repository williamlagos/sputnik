/* Namespace Create */ create = {

submitCause:function(event){
	event.preventDefault();
	$.ajax({
		url:'promote/projects',
		type:'POST',
		data:$('#project').serialize(),
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$.get('efforia/twitter/post',{
				'content':'Criei o projeto #'+$('input[name=title]').val()+' no Efforia.'
			},function(data){});
			$.get('efforia/facebook/post',{
				'content':'Criei o projeto #'+$('input[name=title]').val()+' no Efforia.'
			},function(data){});
			$('.form').html(data);
			$('.send').button('reset')
			.removeClass('projectcreate')
			.addClass('linkcreate');
			$.fn.eventLoop();
		}
	});
},

submitVideo:function(event){
	event.preventDefault();
	$('.send').button('loading');
	$('#video').submit();
},

submitMovement:function(event){
	event.preventDefault();
	var movement_title = $('#movement_title').val();
	var movement_interest = $('.selected').text().trim();
	$.ajax({
		url:'promote/movement',
		type:'POST',
		data:{
			'title':movement_title,
			'interest':movement_interest
		},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){ $.fn.showMosaic(); }
	});
},

selectKeyword:function(event){
	event.preventDefault();
	$('.keyword').removeClass('selected')
	$(this).addClass('selected');
},

showMovement:function(event){
	event.preventDefault();
	movement = $('.title',this).text().trim();
	$.ajax({
		url:'promote/movement',
		data:{'title':movement},
		beforeSend:function(){ $.fn.Progress('Carregando projetos'); },
		success:function(data){
			$('#Grade').Mosaic(data);
			$.fn.eventLoop(data);
		}
	});
},

promoteProject:function(event){
	event.preventDefault();
	$.get('promote/promote',{},function(data){
		$('.promotecontent').html(data);
		$('.send').removeClass('promote')
		.addClass('objectpromote');
		$.fn.eventLoop();
	});
},

promoteObject:function(event){
	event.preventDefault();
	var object_id = $('#Espaco .id').text().trim();
	var object_token = $('#Espaco .token').text().trim();
	$.ajax({
		url:'promote/promote',
		type:'POST',
		data:{
			'id':object_id,
			'token':object_token,
			'content':$('#promotetext').val()
		},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){ $.fn.showMosaic(); }
	})
},

showPromoted:function(event){
	event.preventDefault();
	var promoted = $('.promotedid',this).text().trim();
	$.ajax({
		url:'promote/project',
		data:{'id':promoted},
		beforeSend:function(data){ $.fn.Progress('Carregando conteúdo promovido'); },
		success:function(data){
			$('#Progresso').modal('hide');
			$('#Espaco').html(data).modal().addClass('player');
			var href = $('#player').attr('href');
			var span_width = $('.span4').width();
			$.e.playerOpt['initialVideo'] = $.e.lastVideo = href;
			$.e.playerOpt['width'] = span_width; 
			$.e.playerOpt['height'] = span_width/1.7;
			$("#player").tubeplayer($.e.playerOpt);
			$.fn.eventLoop();
		}
	});
},

selectVideo:function(event){
	event.preventDefault();
	$.fn.hideMenus();
	$.post('promote/collection',{},function(data){
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
	$.get('promote/project',{'id':project_id},function(data){
		$('#Espaco').html(data).modal().addClass('player');
		var href = $('#player').attr('href');
		var span_width = $('.span4').width();
		$.e.playerOpt['initialVideo'] = $.e.lastVideo = href;
		$.e.playerOpt['width'] = span_width; 
		$.e.playerOpt['height'] = span_width/1.7;
		$("#player").tubeplayer($.e.playerOpt);
		$.fn.eventLoop();
	});
},

pledgeProject:function(event){
	event.preventDefault();
	$.get('promote/pledge',{},function(data){
		$('.promotecontent').html(data);
		$('.second').removeClass('pledge').addClass('objectpledge');
		$.fn.eventLoop();
	});
},

transferPledge:function(event){
	event.preventDefault();
	var credits = $('#promotecredit').val();
	var project = $('#Espaco .id').text().trim();
	var user_id = $('#Espaco .userid').text().trim();
	$.ajax({
		url:'efforia/payment',
		type:'POST',
		data:{'credit':credits},
		beforeSend:function(){ $('.objectpledge').button('loading'); },
		success:function(data){
			if(data != ''){
				$('.promotecontent').html(data);
				$('#credits,#value').removeClass('span3').addClass('span1');
				$('#payment').removeClass('span5').addClass('span3');
			} else {
				$.ajax({
					type:'POST',
					url:'pledge',
					data:{'object':project,'credits':credits},
					success:function(data){ $.fn.showMosaic(); }
				});
			}
		}
	});
},

showBackers:function(event){
	event.preventDefault();
	var project_id = $('#Espaco .id').text().trim();
	$.ajax({
		url:'promote/backers',
		data:{'project_id':project_id},
		beforeSend:function(){ $.fn.Progress('Carregando apoiadores'); },
		success:function(data){	$('#Espaco').modal('hide'); $('#Grade').Mosaic(data); }
	});
},

showEvent:function(event){
	event.preventDefault();
	var event_id = $('.id',this).text().trim();
	$.get('promote/event',{'id':event_id},function(data){
		$('#Espaco').html(data).modal();
		$.fn.eventLoop();
	});
},

submitEvent:function(event){
	event.preventDefault();
	$.post('promote/calendar',$('#evento').serialize(),function(data){
		$.get('efforia/facebook/event',$('#evento').serialize(),function(data){
			var ident = data;
	        $.fn.eventLoop();
	        $.e.uploadOpt['url'] = 'efforia/facebook/eventcover?id='+ident;
	        $.e.uploadOpt['success'] = function(data){
	        	console.log(data);
	        }
	        $('.upload,.file').fileUpload($.e.uploadOpt);
		});
		$('.form').html(data);
		/*$.fn.showMosaic();*/ 
	});
}

}
