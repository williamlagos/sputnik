document.documentElement.style.overflowX = 'hidden';
document.documentElement.style.overflowY = 'hidden';
var w = window.innerWidth;
var h = window.innerHeight;
var openedMenu = false;
var option = 0;
var token = '';
$.view = { 
	value:true, 
	marginFactor:10,
	marginTop:0
}

$.fn.loadDialog = function(data){
	$('#Espaco').dialog('destroy');
	$('#Espaco').empty();
	$('#Espaco').html(data);
	$('#Espaco').dialog({
		height:'auto',width:'auto',modal:true,
		position:'center',resizable:false,draggable:false
	});
}

$.fn.loadDialogT = function(data){
	$.fn.loadDialog(data);
	$('.ui-dialog').find('.ui-dialog-titlebar').remove();
}

$.fn.loadMosaic = function(data){
	$(this).empty();
	$(this).html(data);
	$('.mosaic-block').mosaic();
	$.fn.createEvents();
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
	token = data;
	//$('#overlay').find('p').html('Upload concluído.');
	$('#Espaco').dialog('close');
	$.get('/',{'feed':'feed'},function(data){$('#Grade').loadMosaic(data);});
	$.get('known',{'info':'user'},function(data){alert(data);$('#Esquerda').html(data);}); 
}

$.fn.verifyValues = function(xhr){
	/*if(option == 0){
		alert('Selecione uma das categorias listadas.');
		xhr.abort();
	}*/
}

$.fn.animateProgress = function(){
	$('#Espaco').empty().dialog('destroy');
	$('#Espaco').dialog({resizable:false,modal:true,height:'auto',width:'auto',minHeight:48});
	$('#Espaco').html("<img src='images/progress.gif'/>");
	$('.ui-dialog-titlebar').remove();
}

$.fn.hideMenus = function(){
	$('#Espaco').dialog('close');
    $('#Esquerda:visible').hide('fade');
    $('#Sair:visible').hide('fade');
    $('#Canvas:visible').hide('fade');
    $('#Grade').css({'margin-left':'0%'});
}

$.fn.showMenus = function(){
   	$('#Esquerda:hidden').show('fade');
   	$('#Sair:hidden').show('fade');
    $('#Canvas:hidden').show('fade');
    $('#Grade').css({'margin-left':'15%'});
}

$.fn.showDataContext = function(title,data){
	$('#Espaco').empty().dialog('destroy');
	$('#Espaco').html(data);
	$.fn.createEvents();
	$("#Abas").tabs({ ajaxOptions: { success: function(data){ $.fn.createEvents(); } } });
	$( ".tabs-bottom .ui-tabs-nav, .tabs-bottom .ui-tabs-nav > *" )
	.removeClass( "ui-corner-all ui-corner-top" )
	.addClass( "ui-corner-bottom" );
	$('#Espaco').dialog({
		title:title,height:'auto',width:'auto',modal:true,
		position:'center',resizable:false,draggable:false
	});
}

$.fn.showConfigContext = function(data){
	$('#Espaco').empty().dialog('destroy');
	$('#Espaco').html(data);
	$('#Abas').css({'height':$('#Canvas').height()-70});
	$('#Abas').tabs({ ajaxOptions: { success: function(data){ $.fn.createEvents(); } } });
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

$(document).ready(function(){

$.fn.createEvents();

$('.mosaic-block').mosaic();
$('.mosaic-overlay').click(function(event){ $.fn.clickContent(event,$(this)); });
$('.return').click(function(event){ $.fn.showMenus(); });

$('#Menu').hide();
$('a[name=play]').click(function(event){$.fn.showContext(event,'collection',function(data){$.fn.showDataContext('O que você quer tocar hoje?',data);});});
$('a[name=create]').click(function(event){$.fn.showContext(event,'causes',function(data){$.fn.showDataContext('O que você pretende criar hoje?',data);});});
$('a[name=spread]').click(function(event){$.fn.showContext(event,'spread',function(data){$.fn.showDataContext('O que você quer espalhar hoje?',data);});});
$('a[href=config]').click(function(event){$.fn.showContext(event,'config',$.fn.showConfigContext);});
$('a[href=filter]').click(function(event){
	event.preventDefault();
	if(!openedMenu){
		$('#Menu').slideDown("slow");
		openedMenu = true;	
	}else{
		$('#Menu').slideUp("slow");
		$('.lupa').focus();
		openedMenu = false;
	}
});
$('#explore').submit(function(event){
	event.preventDefault(); 
	$.get($.fn.getSearchFilters(this.action,$(this).serialize()),{},function(data){
		$.fn.hideMenus();
		$('#Grade').loadMosaic(data);
	});
});

});
