/* Namespace Play */ play = {

submitPlay:function(event){
	event.preventDefault();
	$.post('content',{},function(data){
		$.fn.hideMenus(); 
		$('#Grade').loadMosaic(data); 
	});
},

loadPlayObject:function(event){
	event.preventDefault();
	if(!$.e.selection){
		data = '<div id="Container"><div id="Message"></div><div id="Player"></div><div id="slider-range-min"></div>'+
						  '<div style="width:50%; float:left; margin-top:10px;">'+
						  "<div style=\"float:left;\"><a onclick=\"$('#Player').tubeplayer('pause');\" class=\"pcontrols "+$.e.control+"ui-icon-pause\"></span></a></div>"+
						  "<div style=\"float:left;\"><a class=\"mute "+$.e.control+"ui-icon-volume-off\"></span></a></div></div>"+
						  "<div style=\"width:50%; float:right; text-align:right; margin-top:10px;\">"+
						  "<a class=\"fan"+$.e.control+"ui-icon-star\"></span></a>"+
						  "<a class=\"deletable"+$.e.control+"ui-icon-trash\"></span></a></div></div>"
		$('#Espaco').Window(data);
		$('.fan').click(function(event){
			event.preventDefault();
			$.get('fan',{'text':$('#Espaco').find('.time').text()},function(data){
				$('#Grade').loadMosaic(data);
				$('#Espaco').dialog('close');
			});
		});
		$('.deletable').click($.fn.deleteObject);
		$('#Espaco').css({'width':800,'height':500});
		$("#Player").tubeplayer({
			width: 770, // the width of the player
			height: 430, // the height of the player
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
				$('#Message').html("<div><img src='images/replay.png' style='width:50%; margin-left:25%;'/></div><h2>Reproduzir novamente?</h2>");
				$('#Message').on('click',function(event){
					event.preventDefault();
					$('#Message').hide();
					$('#Player').tubeplayer('play',$(this).parent().attr('href'));
					$('#Player').show();
				});
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
},

getVideoInformation:function(event){
	event.preventDefault();
	$.get('expose',$('#conteudo').serialize()+'&category='+$.e.option,function(data){
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
		success:function(data){$('#Grade').loadMosaic(data);}
	});
	$.get('known',{'info':'user'},function(data){$('#Esquerda').html(data);}); 
}

}