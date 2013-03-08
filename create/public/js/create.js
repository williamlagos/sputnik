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

submitMovement:function(event){
	event.preventDefault();
	var movement_title = $('#movement_title').val();
	var movement_interest = $('.selected').text().trim();
	$.ajax({
		url:'movement',
		type:'POST',
		data:{
			'title':movement_title,
			'interest':movement_interest
		},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('#Espaco').modal('hide');
			window.location = '/';
		}
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
	$.get('movement',{'title':movement},function(data){
		$('#Grade').Mosaic(data);
		$.fn.eventLoop(data);
	});
},

promoteProject:function(event){
	event.preventDefault();
	$.get('promote',{},function(data){
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
		url:'promote',
		type:'POST',
		data:{
			'id':object_id,
			'token':object_token,
			'content':$('#promotetext').val()
		},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('#Espaco').modal('hide');
			window.location = '/';
		}
	})
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
	cred = $(this).find('.causecredits').parent().html();
	$.get('project',{'id':project_id},function(data){
		$('#Espaco').html(data).modal().addClass('player');
		var span_width = $('.span4').width();
		$.e.playerOpt['initialVideo'] = $.e.lastVideo = href;
		$.e.playerOpt['width'] = span_width; 
		$.e.playerOpt['height'] = span_width/1.7;
		$("#player").tubeplayer($.e.playerOpt);
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