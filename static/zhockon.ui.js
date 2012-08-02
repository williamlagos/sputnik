$.fn.Window = function(data){
	$(this).dialog('destroy');
	$(this).empty();
	closebutton = '<div style="height:15px;"><a class="ui-dialog-titlebar-close ui-corner-all" role="button" href="#" style="top:15px;"><span class="close ui-icon ui-icon-closethick">fechar</span></a></div>'
	$(this).html(closebutton+data);
	$(this).dialog({
		height:'auto',width:'auto',modal:true,
		position:'center',resizable:false,draggable:false
	});
	$('.ui-dialog').find('.ui-dialog-titlebar').remove();
	$('.close').click(function(event){
		event.preventDefault();
		$('#Espaco').dialog('destroy');
		$('#Player').tubeplayer('destroy');
	});
}

$.fn.Dialog = function(data){
	$(this).dialog('destroy');
	$(this).empty();
	cancelbutton = '<a class="cancel ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em 1em; float:right;">Cancelar</a>';
	$(this).html(data);
	$('form').append(cancelbutton);
	$(this).dialog({
		height:'auto',width:'auto',modal:true,
		position:'center',resizable:false,draggable:false
	});
	$('.ui-dialog').find('.ui-dialog-titlebar').remove();
	$('.cancel').click(function(event){
		event.preventDefault();
		$('#Espaco').dialog('close');
		$('#Espaco').empty();
	});
}

$.fn.Mosaic = function(data){
	$(this).empty();
	$(this).html(data);
	$('.mosaic-block').mosaic();	
}

$.fn.Progress = function(){
	$(this).empty().dialog('destroy');
	$(this).dialog({resizable:false,modal:true,height:'auto',width:'auto',minHeight:48});
	$(this).html("<img src='images/progress.gif'/>");
	$('.ui-dialog-titlebar').remove();
}

$.fn.showDataContext = function(title,data){
	$('#Espaco').empty().dialog('destroy');
	$('#Espaco').html(data);
	$("#Abas").tabs({ ajaxOptions: { success: function(data){ $.fn.eventLoop(); } } });
	$( ".tabs-bottom .ui-tabs-nav, .tabs-bottom .ui-tabs-nav > *" )
	.removeClass( "ui-corner-all ui-corner-top" )
	.addClass( "ui-corner-bottom" );
	$('.ui-tabs-nav').append('<a class="cancel ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em 1em; float:right; border-bottom-right-radius:50px;">Cancelar</a>');
	$('#Espaco').dialog({
		title:title,height:$('#Canvas').height()-5,width:$('#Canvas').width()-5,
		position:['right','bottom'],resizable:false,draggable:false
	});
	if($('#Canvas').is(':hidden')){
		$('.ui-dialog').css({'left':0,'width':$('#Grade').width()-5});
	}
	$('.ui-tabs-nav').css({'border-bottom-left-radius':'50px','border-bottom-right-radius':'50px'});
	$('.ui-tabs-selected').css({'border-bottom-left-radius':'50px'});
	$('.ui-dialog').find('.ui-dialog-titlebar').remove();
	$('#Abas').css({'height':$('#Canvas').height()-30,'background':'#222'});
	$('#Espaco').css({'height':$('#Canvas').height(),'background':'black'});
}

$.fn.clickContent = function(event){
	event.preventDefault();
	if($.e.selection){
		time = $(this).find('.time').text();
		if($(this).attr('class') == 'mosaic-overlay selected'){
			$.e.objects.removeItem(time);
			$(this).attr('style','background:url(../images/bg-black.png); display: inline; opacity: 0;')
			$(this).attr('class','mosaic-overlay');
		}else{
			$(this).attr('style','background:url(../images/bg-red.png); display: inline; opacity: 0;')
			$(this).attr('class','mosaic-overlay selected');
			$.e.objects.push(time);
		}
	}
}

$.fn.editNewField = function(event){
	event.preventDefault();
	if(!$(this).hasClass('erased')){
		$(this).attr('value','');
		$(this).addClass('erased');
	}
}

$.fn.showContext = function(event,context,callback){
	event.preventDefault();
	$.ajax({
		url:context,
		beforeSend: $('#Espaco').Progress(),
		success: function(data){ callback(data); }
	});
}
