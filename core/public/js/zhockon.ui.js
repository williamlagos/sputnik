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
}

$.fn.Dialog = function(data){
	$(this).dialog('destroy');
	$(this).empty();
	cancelbutton = '<a class="cancel ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em 1em; float:right; margin:1px;">Cancelar</a>';
	$(this).html(data);
	$('form').append(cancelbutton);
	$(this).dialog({
		height:'auto',width:'auto',modal:true,
		position:'center',resizable:false,draggable:false
	});
	$('.ui-dialog').find('.ui-dialog-titlebar').remove();
}

$.fn.Mosaic = function(data){
	$(this).empty();
	$(this).html(data);
	$('.mosaic-block').mosaic();	
}

$.fn.Progress = function(){
	$(this).empty().dialog('destroy');
	$(this).dialog({resizable:false,modal:true,height:'auto',width:'auto',minHeight:48});
	$(this).html("<img src='static/img/progress.gif'/>");
	$('.ui-dialog-titlebar').remove();
}

$.fn.Context = function(data,height,width){
	$(this).empty().dialog('destroy');
	$(this).html(data);	
	$(this).dialog({
		title:'Context',height:height,width:width,
		position:['right','bottom'],resizable:false,draggable:false
	});
	$(this).css({'height':height,'background':'black'});
	$('.ui-dialog-titlebar').remove();
}

$.fn.Tabs = function(events,height){
	$(this).tabs({ ajaxOptions: { success: events } });
	$( ".tabs-bottom .ui-tabs-nav, .tabs-bottom .ui-tabs-nav > *" )
	.removeClass( "ui-corner-all ui-corner-top" )
	.addClass( "ui-corner-bottom" );
	$('.ui-tabs-nav').append('<a class="cancel ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em 1em; float:right; border-bottom-right-radius:50px;">Cancelar</a>');
	$('.ui-tabs-nav').css({'border-bottom-left-radius':'50px','border-bottom-right-radius':'50px'});
	$('.ui-tabs-selected').css({'border-bottom-left-radius':'50px'});
	$('.ui-dialog').find('.ui-dialog-titlebar').remove();
	$(this).css({'height':height,'background':'#222'});
}