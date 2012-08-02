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
	if($('.message').text() == 'Você não possui nenhum movimento. Gostaria de criar um?'){
		$.fn.showContext(event,'movement?action=grid',function(data){$('#Grade').loadMosaic(data);});
	}else if($('.message').text().indexOf('Movimentos em aberto') != -1){
		$.fn.showContext(event,'movement?view=grid',function(data){$('#Grade').loadMosaic(data);});
	}else if($('.message').text().indexOf('Programações de vídeos disponíveis') != -1){
		$.fn.showContext(event,'schedule?view=grid',function(data){$('#Grade').loadMosaic(data);});	
	}else{
		$.fn.showContext(event,'schedule?action=grid',function(data){$('#Grade').loadMosaic(data);});
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
		$('#Grade').translate2D(0,0); $.e.marginTop = 0;
		$('#Grade').loadMosaic(data);
	});
},

openCausableSpread:function(event){
	event.preventDefault();
	object = $(this).find('.time').text();
	$.get('causes',{'view':'grid','object':object},function(data){$('#Grade').loadMosaic(data);});
},

selectVideo:function(event){
	event.preventDefault();
	$.fn.hideMenus();
	$.post('collection',{},function(data){
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
	if(!selection){
		object = $(this).find('.time').text();
		data = '<div id="Container"><div id="Message"></div><div id="Player"></div><div id="slider-range-min"></div>'+
						  '<div style="width:50%; float:left; margin-top:10px;">'+
						  "<div style=\"float:left;\"><a onclick=\"$('#Player').tubeplayer('pause');\" class=\"pcontrols "+$.e.control+"ui-icon-pause\"></span></a></div>"+
						  "<div style=\"float:left;\"><a class=\"mute "+$.e.control+"ui-icon-volume-off\"></span></a></div></div>"+
						  "<div style=\"width:50%; float:right; text-align:right; margin-top:10px;\">"+
						  "<a class=\"spread"+$.e.control+"ui-icon-star\"></span></a>"+
						  "<a class=\"deletable"+$.e.control+"ui-icon-trash\"></span></a></div></div>"
		$('#Espaco').Window(data);
		$('.spread').click(function(event){
			event.preventDefault();
			related = "<div class=\"time\" style=\"display:none;\">"+time+"</div>"
			$.get('spread',{'spread':'cause'},function(data){
				$.fn.showDataContext('',data+related);
				$('#Espaco').css({'background':'#222','border-radius':'50px'});
				$('#spreadpost').click(function(event){
					event.preventDefault();
					$.post('spread',{'spread':$('#id_content').val(),'time':object},function(data){
						alert(data);
						$('#Espaco').dialog('close');
					});
				});
			});
		});
		$('.deletable').click($.fn.deleteObject);
		$('#Espaco').css({'width':800,'height':500});
		$("#Player").tubeplayer({
			width: 770, // the width of the player
			height: 400, // the height of the player
			autoPlay: true,
			showinfo: false,
			autoHide: true,
			iframed: true,
			showControls: 0,
			allowFullScreen: "true", // true by default, allow user to go full screen
			initialVideo: $(this).parent().attr('href'), // the video that is loaded into the player
			preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
			onPlay: function(id){$('.pcontrols').parent().html("<a onclick=\"$('#Player').tubeplayer('pause');\" class=\"pcontrols "+$.e.control+"ui-icon-pause\" ></span></a>");},
			onPause: function(){$('.pcontrols').parent().html("<a onclick=\"$('#Player').tubeplayer('play');\" class=\"pcontrols "+$.e.control+"ui-icon-play\" ></span></a>");},
			onMute: function(){$('.mute').parent().html("<a onclick=\"$('#Player').tubeplayer('unmute');\" class=\"unmute "+$.e.control+"ui-icon-volume-on\" ></span></a>");},
			onUnMute: function(){$('.unmute').parent().html("<a onclick=\"$('#Player').tubeplayer('mute');\" class=\"mute "+$.e.control+"ui-icon-volume-off\" ></span></a>");},
			onStop: function(){}, // after the player is stopped
			onSeek: function(time){}, // after the video has been seeked to a defined point
			onPlayerPlaying: function(){},
			onPlayerEnded: function(){ 
				$('#Player').hide();
				$('.message').html('<h2>Reproduzir novamente?</h2>');
			}
		});
		$('.mute').click(function(event){
			event.preventDefault();
			$('#Player').tubeplayer('mute');
		});
		$('.unmute').click(function(event){
			event.preventDefault();
			$('#Player').tubeplayer('unmute');
		});
		$('#Espaco').bind('dialogclose',function(event,ui){ $('#Player').tubeplayer('destroy'); });
		$('#Espaco').dialog('option','position','center');
	}
}

}