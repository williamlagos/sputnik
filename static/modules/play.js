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
						  "<div style=\"float:left;\"><a onclick=\"$('#Player').tubeplayer('pause');\" class=\"player pcontrols "+$.e.control+"ui-icon-pause\"></span></a></div>"+
						  "<div style=\"float:left;\"><a class=\"player mute "+$.e.control+"ui-icon-volume-off\"></span></a></div></div>"+
						  "<div style=\"width:50%; float:right; text-align:right; margin-top:10px;\">"+
						  "<a class=\"fan"+$.e.control+"ui-icon-star\"></span></a>"+
						  "<a class=\"deletable"+$.e.control+"ui-icon-trash\"></span></a></div></div>"
		$('#Espaco').Window(data);
		$('#Espaco').css({'width':800,'height':500});
		$.e.playerOpt['initialVideo'] = $.e.lastVideo = $(this).parent().attr('href');
		$("#Player").tubeplayer($.e.playerOpt);
		$('#Espaco').bind('dialogclose',function(event,ui){ $('#Player').tubeplayer('destroy'); });
		$('#Espaco').dialog('option','position','center');
		$.fn.eventLoop();
	}
},

pauseButton:function(id){$('.pcontrols').parent().html("<a onclick=\"$('#Player').tubeplayer('pause');\" class=\"pcontrols "+$.e.control+"ui-icon-pause\" ></span></a>");},
playButton:function(){$('.pcontrols').parent().html("<a onclick=\"$('#Player').tubeplayer('play');\" class=\"pcontrols "+$.e.control+"ui-icon-play\" ></span></a>");},
muteButton:function(){$('.mute').parent().html("<a onclick=\"$('#Player').tubeplayer('unmute');\" class=\"unmute "+$.e.control+"ui-icon-volume-on\" ></span></a>");},
unmuteButton:function(){$('.unmute').parent().html("<a onclick=\"$('#Player').tubeplayer('mute');\" class=\"mute "+$.e.control+"ui-icon-volume-off\" ></span></a>");},
replay:function(){ 
	$('#Player,.player').hide();
	$('#Message').html("<div><img src='images/replay.png' style='width:50%; margin-left:25%;'/></div><h2>Reproduzir novamente?</h2>");
	$('#Message').show();
	$.fn.eventLoop();
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