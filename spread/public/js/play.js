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
		$('#Grade').loadMosaic(data); 
	});
},

loadPlayObject:function(event){
	event.preventDefault();
	var collected = ''; var id = '';
	var object = $(this).find('.time').text()
	var href = $(this).parent().attr('href');
	var time = $(this).find('.time').parent().html();
	var credit = $(this).find('.credit').text()
	if($.e.selection) return;
	if($(this).find('.buyvideo').length){
		$.ajax({
			url:'collect',
			data:{'object':object},
			success:function(data){ 
			if(data == 'no'){
				$.get('userid',{'object':object},function(data){ id = data; });
				$.ajax({
					type:'POST',
					url:'payment',
					data:{'credit':credit,'other':id},
					beforeSend:function(){ $('#Espaco').Progress(); },
					success:function(data){
						if(data != ''){ alert(data); $('#Espaco').empty().dialog('destroy');
						}else{
							$.ajax({
								type:'POST',
								url:'collect',
								data:{'object':object},
								success:function(data){}
							});
							play.openPlayer(time,href);
						}
					}
				});
			}
		}});
	}else{ play.openPlayer(time,href); }
},

openPlayer:function(time,href){
	$.ajax({url:'media',success:function(data){
		$('#Espaco').Window(time+data);
		$('#Espaco').find('.buyvideo').remove();
		$('#Espaco').css({'width':800,'height':600});
		$('#Container').css({'width':790,'height':430});
		$('.date').css({'display':'none'});
		$.e.playerOpt['initialVideo'] = $.e.lastVideo = href;
		$.e.playerOpt['width'] = 790;
		$.e.playerOpt['height'] = 430;
		$('.player,.general').addClass($.e.control);
		$("#Player").tubeplayer($.e.playerOpt);
		$('#Espaco').on('dialogclose',function(event,ui){ $('#Player').tubeplayer('destroy'); });
		$('#Espaco').dialog('option','position','center');
		$.fn.eventLoop();
	}});
},

playAgain:function(){ 
	$.e.duration = 0;
	$('#Player,.player').hide();
	$('#Message').html("<div><img src='images/replay.png' style='width:50%; margin-left:25%;'/></div><h2>Reproduzir novamente?</h2>");
	$('#Message').show();
	$.fn.eventLoop();
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

monetizeVideo:function(event){
	event.preventDefault();
	$(this).parent().prepend('<div style="text-align:right;"><label>Preço do vídeo (Em créditos)</label><input type="number" class="price eraseable"/></div>');
	$(this).remove();
},

loadCollection:function(event){
	event.preventDefault();
	$.post('collection',{},$('#Grade').loadMosaic);
},

}