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

showSpreadable:function(event){
	event.preventDefault();
	var spread_id = $('.id',this).text().trim();
	$.get('spreadable',{'id':spread_id},function(data){
		$('#Espaco').html(data).modal();
		$.fn.eventLoop();
	});
},

showEvent:function(event){
	event.preventDefault();
	var event_id = $('.id',this).text().trim();
	$.get('event',{'id':event_id},function(data){
		$('#Espaco').html(data).modal();
		$.fn.eventLoop();
	});
},

showImage:function(event){
	event.preventDefault();
	var image_id = $('.id',this).text().trim();
	$.get('image',{'id':image_id},function(data){
		$('#Espaco').html(data).modal();
		$.fn.eventLoop();
	});
},

showPageEdit:function(event){
	event.preventDefault();
	var pagedit_id = $('.id',this).text().trim();
	$.get('pageedit',{'id':pagedit_id},function(data){
		$('#Espaco').html(data).modal();
		$.fn.eventLoop();
	});
},

savePage:function(event){
	event.preventDefault();
	var pagesave_id = $('#Espaco .id').text().trim();
	$.ajax({
		url:'pageedit',
		type:'POST',
		data:{
			'id':pagesave_id,
			'title':$('#pagetitle').val(),
			'content':$('#pagetxt').val()
		},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('#Espaco').modal('hide');
			return window.location = '/';
		}
	});
},

spreadSpread:function(event){
	event.preventDefault();
	var object_id = $('#Espaco .id').text().trim();
	$.get('spreadspread',{'id':object_id},function(data){
		$('.spreadcontent').html(data);
		$('.send').removeClass('spread')
		.addClass('objectspread');
		$.fn.eventLoop();
	});
},

spreadObject:function(event){
	event.preventDefault();
	var object_id = $('#Espaco .id').text().trim();
	var object_token = $('#Espaco .token').text().trim();
	$.ajax({
		url:'spreadspread',
		type:'POST',
		data:{
			'id':object_id,
			'token':object_token,
			'content':$('#spreadtext').val(),
		},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('#Espaco').modal('hide');
			window.location = '/';
		}
	});
},

showSpreaded:function(event){
	event.preventDefault();
	var spreaded_id = $('.spreadedid',this).text().trim();
	var spreaded_token = $('.spreadedtoken',this).text().trim();
	$.ajax({
		url:'spreaded',
		data:{ 
			'spreaded_id':spreaded_id,
			'spreaded_token':spreaded_token
		},
		beforeSend: function(){ $('.send').button('loading'); },
		success:function(data){ 
			$('#Grade').Mosaic(data);
			$.fn.eventLoop();
		}
	});
},

}