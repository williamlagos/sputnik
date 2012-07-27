$.fn.loadDialog = function(data){
	$('#Espaco').dialog('destroy');
	$('#Espaco').empty();
	closebutton = '<div style="height:15px;"><a class="ui-dialog-titlebar-close ui-corner-all" role="button" href="#" style="top:15px;"><span class="close ui-icon ui-icon-closethick">fechar</span></a></div>'
	$('#Espaco').html(closebutton+data);
	$('#Espaco').dialog({
		height:'auto',width:'auto',modal:true,
		position:'center',resizable:false,draggable:false
	});
	$('.ui-dialog').find('.ui-dialog-titlebar').remove();
}

$.fn.loadDialogT = function(data){
	$.fn.loadDialog(data);
	$('.close').click(function(event){
		event.preventDefault();
		$('#Espaco').dialog('destroy');
		$('#Player').tubeplayer('destroy');
	});
}

$.fn.loadDialogW = function(data){
	$('#Espaco').dialog('destroy');
	$('#Espaco').empty();
	$('#Espaco').html(data);
	$('#Espaco').dialog({
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

$.fn.loadMosaic = function(data){
	$(this).empty();
	$(this).html(data);
	$('.mosaic-block').mosaic();
	if(!$.e.initial)	$('.return').parent().show()
	$.fn.eventLoop();
}

$.fn.progressHandlingFunction = function(e){
    if(e.lengthComputable) $('progress').attr({value:e.loaded,max:e.total});
}

$.fn.uploadProgress = function(){
	$('#overlay').css({ height: $('#upload').height() });
	$('#overlay').show();
	myXhr = $.ajaxSettings.xhr();
	if(myXhr.upload) myXhr.upload.addEventListener('progress',$.fn.progressHandlingFunction,false);
	return myXhr;
}

$.fn.finishUpload = function(data){
	$.e.token = data;
	//$('#overlay').find('p').html('Upload concluído.');
	$('#Espaco').dialog('close');
	$.get('/',{'feed':'feed'},function(data){$('#Grade').loadMosaic(data);});
	$.get('known',{'info':'user'},function(data){$('#Esquerda').html(data);}); 
}

$.fn.animateProgress = function(){
	$('#Espaco').empty().dialog('destroy');
	$('#Espaco').dialog({resizable:false,modal:true,height:'auto',width:'auto',minHeight:48});
	$('#Espaco').html("<img src='images/progress.gif'/>");
	$('.ui-dialog-titlebar').remove();
}

$.fn.hideMenus = function(){
	$('.return').parent().show('fade');
	$('#Espaco').dialog('close');
    $('#Esquerda:visible').hide('fade');
    $('#Sair:visible').hide('fade');
    $('#Canvas:visible').hide('fade');
    $('#Grade').css({'margin-left':'0%'});
}

$.fn.showMenus = function(){
	$('.return').parent().hide('fade');
   	$('#Esquerda:hidden').show('fade');
   	$('#Sair:hidden').show('fade');
    $('#Canvas:hidden').show('fade');
    $('#Grade').css({'margin-left':'15%'});
}

$.fn.showDataContext = function(title,data){
	$.e.context = true;
	$('*').unbind();
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
	$.e.context = false;
}

$.fn.showConfigContext = function(data){
	$('#Espaco').empty().dialog('destroy');
	$('#Espaco').html(data);
	$('#Abas').css({'height':$('#Canvas').height()-70});
	$('#Abas').tabs({ ajaxOptions: { success: function(data){ $.e.config = true; $.fn.eventLoop(); } } });
	$( ".tabs-bottom .ui-tabs-nav, .tabs-bottom .ui-tabs-nav > *" )
	.removeClass( "ui-corner-all ui-corner-top" )
	.addClass( "ui-corner-bottom" );
	$('#Espaco').dialog({
		title:'Configurações do Efforia',height:$('#Canvas').height()-5,width:$('#Canvas').width()-5,
		position:['right','bottom'],modal:false,resizable:false,draggable:false
	});
}

$.fn.showContext = function(event,context,callback){
	event.preventDefault();
	$.ajax({
		url:context,
		beforeSend: $.fn.animateProgress(),
		success: function(data){ callback(data); }
	});
}

$.fn.getSearchFilters = function(action,data){
	all = '';
	query = action+'?'+data;
	filters = '&filters='
	leastone = false;
	$('.checkbox').each(function(){
		if($(this).css('background-position') == '0px -55px'){
			filters += $(this).parent().text().toLowerCase().replace(/^\s+|\s+$/g,'')+',';
			leastone = true;
		}
		all += $(this).parent().text().toLowerCase().replace(/^\s+|\s+$/g,'')+',';
	});
	if(!leastone) filters += all;
	url = query+filters;
	return url;
}
