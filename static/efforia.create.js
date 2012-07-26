$.fn.createSelection = function(event){
	event.preventDefault();
	if(selection == true){
		href = $(this).attr('href');
		if(objects.length < 1) return;
		label = ''; value = '';
		if(href == 'movement'){
			label = 'Nome do seu movimento:';
			value = 'Criar movimento';
		}else if(href == 'schedule'){
			label = 'Nome da sua programação:';
			value = 'Criar programação';
		}
		$(this).children().html('<form method="post" action="/'+href+
		'" style="text-align:center;">'+label+
		' <input name="title" style="width:90%;"></input><div id="botoes"><input name="create" class="ui-button ui-widget ui-state-default ui-corner-all" type="submit" value="'+value+
		'"></div></form>');
		$('input[name=title]').focus();
		$('input[name=create]').click(function(event){
			event.preventDefault();
			title = $('input[name=title]').val()
			if(title == '') return;
			objs = objects.join();
			$.post(href,{'objects':objs,'title':title},function(data){
				$.get(href,{'view':'view'},function(data){$('#Grade').loadMosaic(data)});
				$.fn.showMenus();
				$.fn.showDataContext('',data);
				$('#Espaco').css({'background':'#222','border-radius':'50px','height':$('#Canvas').height()-5});
			});
			selection = false;
		});
		//$(this).attr('class','mosaic-overlay title');
	}
}

$.fn.submitCause = function(event){
	event.preventDefault();
	if(token == ''){
		alert('Selecione um vídeo para acompanhar a causa primeiro.');
		return;
	}
	serialized = $('#causas').serialize()+'&category='+option+'&token='+token;
	$.post('causes',serialized,function(data){ 
		$.fn.hideMenus();
		$('#Grade').loadMosaic(data);
	});
}

$.fn.loadListContext = function(event){
	if($('.message').text() == 'Você não possui nenhum movimento. Gostaria de criar um?'){
		$.fn.showContext(event,'movement?action=grid',function(data){$('#Grade').loadMosaic(data);});
	}else if($('.message').text().indexOf('Movimentos em aberto') != -1){
		$.fn.showContext(event,'movement?view=grid',function(data){$('#Grade').loadMosaic(data);});
	}else if($('.message').text().indexOf('Programações de vídeos disponíveis') != -1){
		$.fn.showContext(event,'schedule?view=grid',function(data){$('#Grade').loadMosaic(data);});	
	}else{
		alert('Hi!');
		$.fn.showContext(event,'schedule?action=grid',function(data){$('#Grade').loadMosaic(data);});
	}
	$.fn.hideMenus();
	$('#Espaco').dialog('close');
	selection = true;
}

$.fn.loadListMosaic = function(event){
	event.preventDefault();
	title = $(this).find('h2').html();
	refer = $(this).attr('href');
	$.get(refer,{'view':refer,'title':title},function(data){
		$('#Grade').translate2D(0,0); $.view.marginTop = 0;
		$('#Grade').loadMosaic(data);
	});
}

$.fn.openCausableSpread = function(event){
	event.preventDefault();
	object = $(this).find('.time').text();
	$.get('causes',{'view':'grid','object':object},function(data){$('#Grade').loadMosaic(data);});
}