/* Namespace Spread */ spread = {

submitPage:function(event){
	event.preventDefault();
	$.ajax({
		url:'pages',
		type:'POST',
		data:{
			'content':$('#pagetxt').val(),
			'title':$('#pagetitle').val()
		},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('#Espaco').modal('hide');
			$('#Grade').html(data);
		}
	})
},

submitSpread:function(event){
	event.preventDefault();
	$.ajax({
		url:'spread',
		type:'POST',
		data:{'content':$('#spreadtext').val()},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$.fn.hideMenus();
			$.get('twitter_post',{'content':$('#spreadtext').val()},function(data){});
			$.get('facebook_post',{'content':$('#spreadtext').val()},function(data){});
			$('#Grade').loadMosaic(data);
		}
	});
},

submitEvent:function(event){
	event.preventDefault();
	$.post('calendar',$('#evento').serialize(),function(data){
		$.get('facebook_event',$('#evento').serialize(),function(data){});
		$.fn.hideMenus(); 
		$('#Grade').loadMosaic(data); 
	});
},

submitImage:function(event){
	event.preventDefault();
},

loadListMosaic:function(event){
	event.preventDefault();
	title = $('.listspread').text();
	refer = 'schedule';
	$.get(refer,{'action':'select','view':refer,'title':title},function(data){
		$('#Grade').translate(0,0); $.e.marginTop = 0;
		$('#Grade').loadMosaic(data);
	});
},

loadTextObject:function(event){
	event.preventDefault();
	var spread_id = $('.id',this).text().trim();
	$.get('spreadable',{'id':spread_id},function(data){
		$('#Espaco').empty().html(data).modal();
	});
	$.fn.eventLoop();
},

openSpreadableSpread:function(event){
	event.preventDefault();
	object = $(this).find('.time').text();
	$.ajax({
		url:'spread',
		data:{'view':'grid','object':object},
		beforeSend: function(){ $('.send').button('loading'); },
		success:function(data){ $('#Grade').loadMosaic(data); }
	});
},

openEventSpread:function(event){
	event.preventDefault();
	object = $('.eventspread').find('.time').text();
	$.ajax({
		url:'calendar',
		data:{'view':'grid','object':object},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){$('#Grade').loadMosaic(data);}
	});
},

showSpread:function(event){
	event.preventDefault();
	related = "<div class=\"time\" style=\"display:none;\">"+$('#Espaco').find('.time').text()+"</div>"
	$.ajax({
		url:'spread',
		data:{'spread':'spread'},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('#Espaco').Window(data+related);
			$('.spreadspread').button();
			$.fn.eventLoop();
		}
	});
},

spreadSpreadable:function(event){
	event.preventDefault();
	$.post('spread',{'spread':$('#id_content').val(),'time':$('#Espaco').find('.time').text()},function(data){
		$('#Grade').Mosaic(data);
		$('#Espaco').dialog('close');
		$.fn.hideMenus();
	});
},

}