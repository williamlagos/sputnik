/* Namespace Spread */ spread = {

submitSpread:function(event){
	event.preventDefault();
	$.ajax({
		url:'spread',
		type:'POST',
		data:$('#espalhe').serialize(),
		beforeSend:function(){
			if($('#id_content').val() == ''){
				alert('O conteúdo da postagem está vazio. Digite alguma coisa.')
				abort();
			}
		},
		success:function(data){
			$.fn.hideMenus();
			$('#Grade').loadMosaic(data);
		}
	});
},

submitEvent:function(event){
	event.preventDefault();
	$.post('calendar',$('#evento').serialize(),function(data){
		$.fn.hideMenus(); 
		$('#Grade').loadMosaic(data); 
	});
},

loadTextObject:function(event){
	event.preventDefault();
	data = $(this).html()+'<div style="width:50%; float:left;"><a class="spread ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em 1em;"><span class="ui-icon ui-icon-star"></span></a></div>'+
									 '<div style="width:50%; float:right; text-align:right;"><a class="deletable ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em 1em;"><span class="ui-icon ui-icon-trash"></span></a></div>'
	$('#Espaco').Window(data);
	$('.spread').click(function(event){
		event.preventDefault();
		related = "<div class=\"time\" style=\"display:none;\">"+$('#Espaco').find('.time').text()+"</div>"
		$.get('spread',{},function(data){
			$.fn.showDataContext('',data+related);
			$('#Espaco').css({'background':'#222','border-radius':'50px'});
			$('#spreadpost').click(function(event){
				event.preventDefault();
				$.post('spread',{'spread':$('#id_content').val(),'time':$('#Espaco').find('.time').text()},function(data){
					alert(data);
					$('#Espaco').dialog('close');
				});
			});
		});
	});
	$('.deletable').click($.fn.deleteObject);
},

openSpreadableSpread:function(event){
	event.preventDefault();
	object = $('.spreadablespread').find('.time').text();
	$.get('spread',{'view':'grid','object':object},function(data){$('#Grade').loadMosaic(data);});
},

openEventSpread:function(event){
	event.preventDefault();
	object = $('.eventspread').find('.time').text();
	$.get('calendar',{'view':'grid','object':object},function(data){$('#Grade').loadMosaic(data);});
},

}