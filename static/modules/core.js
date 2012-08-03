$.fn.newItem = function(event){
	event.preventDefault();
	refer = $(this).attr('href');
	$.fn.showContext(event,refer,function(data){ $('#Grade').loadMosaic(data); $('#Espaco').dialog('destroy'); });
}

$.fn.createSelection = function(event){
	event.preventDefault();
	if(selection == true){
		href = $(this).attr('href');
		if($.e.objects.length < 1) return;
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
			objs = $.e.objects.join();
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

$.fn.changeSelection = function(event){
	event.preventDefault();
	$.e.option = $("select option:selected").val();
}

$.fn.sendNewField = function(event){
	event.preventDefault();
	if(event.which != $.ui.keyCode.ENTER) return;
	name = $(this).attr('name');
	value = $(this).val();
	serialized = {};
	serialized['key'] = [name,value] 
	$.post('profile',serialized,function(data){
		$(data).parent().parent().find('#statechange').html('<img src="images/ok.png"></img>');
	});
}

$.fn.submitPasswordChange = function(event){
	$.ajax({
		url:'password',
		success:function(data){
			$('#passwordchange').html(data);
			$('#password').attr('value','Alterar senha');
			$('#password').click(function(event){
				event.preventDefault();
				$.ajax({
					url:'password',
					type:'POST',
					data:$('#passwordform').serialize(),
					beforeSend:function(){
						if($('#id_new_password1').val() != $('#id_new_password2').val()){
							alert('A senha nova está diferente de sua confirmação. Digite novamente.');
							abort();
						}
					},
					success:function(data){
						if(data == 'Senha incorreta.'){
							$('#passwordform').find('#statechange').html('<img src="images/nok.png"></img>');
						}else{
							$('#passwordform').find('#statechange').html('<img src="images/ok.png"></img>');	
						}
					}
				});
			});
		}
	});
}

$.fn.deleteObject = function(event){
	event.preventDefault();
	$.get('delete',{'text':$('#Espaco').find('.time').text()},function(data){
		$.get('/',{'feed':'feed'},function(data){$('#Grade').loadMosaic(data);});
		$('#Espaco').dialog('close');
	});
}

$.fn.loadProfileObject = function(event){
	event.preventDefault();
	$.get('known',{'info':$(this).find('.name').text()},function(data){ 
		$('#Esquerda').html(data);
		$('.fan').click(function(event){
			event.preventDefault();
			$.get('fan',{'text':$('#fan').text()},function(data){
				$('#Grade').loadMosaic(data);
				$.fn.hideMenus();
			});
		});
	});
	$.get('known',{'activity':$(this).find('.name').text()},function(data){	$('#Grade').loadMosaic(data); });
	$.fn.showMenus();
}

$.fn.loadMosaic = function(data){
	$('#Grade').Mosaic(data);
	if(!$.e.initial) $('.return').parent().show()
	$.fn.eventLoop();
}

$.fn.loadMoreMosaic = function(event){
	event.preventDefault();
	number = $(this).attr('name');
	$.post($(this).attr('href'),{'number':number},function(data){
		$('#Grade').translate2D(0,0); $.e.marginTop = 0;
		$('#Grade').loadMosaic(data);
		if($('.blank').text() != '') $.e.marginFactor = 0;
	});
}

$.fn.loadNewDialog = function(event){
	event.preventDefault();
	href = $(this).attr('href');
	$.ajax({
		url:href,
		beforeSend:$.fn.animateProgress,
		success:function(data){
			$('#Espaco').Dialog(data);
			$('#id_username').focus();
		}
	});
}

$.fn.closeDialog = function(event){
	event.preventDefault();
	$('#Espaco').dialog('destroy');
	$('#Player').tubeplayer('destroy');
}

$.fn.backToHome = function(event){
	event.preventDefault();
	$('#Pagina').hide();
	$('body').css({'background':'#222'});
	$('#Pagina,#Rodape').css({'color':'white'})
	setTimeout(function(){
		$('#Central').translate2D(0,0);
	});
}

$.fn.registerPlace = function(event){
	event.preventDefault();
	$.get('place',{},function(data){
		$('#Espaco').Dialog(data);
		$('.header').remove();
		$('.right').remove();
		$('.left').css({'width':'100%','margin-left':'0%'});
		$('.submit').css({'width':'auto'});
		$('.submit').click(function(event){
			event.preventDefault();
			$('form').submit();
		});
	});
}

$.fn.showMessage = function(event){
	event.preventDefault();
	$('#Direita').animate({'right':'-15%'});
	$('#Direita').animate({'right':'0%'});
}

$.fn.gotoSocial = function(event){
	$(this).redirect();
}

$.fn.showFavorites = function(event){
	event.preventDefault();
	$.get('favorites',{},function(data){ 
		$('#Grade').loadMosaic(data); 
		$.fn.hideMenus(); 
	});
}

$.fn.showContext = function(event){
	event.preventDefault();
	$.get($(this).attr('href'),{},function(data){
		$('#Espaco').Context(data,$('#Canvas').height()-5,$('#Canvas').width()-5);
		$('#Abas').Tabs(function(){
			if($('#Canvas').is(':hidden')){$('.ui-dialog').css({'left':0,'width':$('#Grade').width()-5});}
			$('#id_username,#id_email,#id_last_name,#id_first_name').addClass('eraseable');
			$('#overlay').hide();
			$.fn.eventLoop();
		},$('#Canvas').height());
	});
}

$.fn.showLoginView = function(event){
	event.preventDefault();
	$.ajax({url:'login',beforeSend:$.fn.animateProgress,success:function(data){
		$('#Espaco').Dialog(data);
		$('.submit').click(function(event){
			event.preventDefault();
			$('form').submit();
		});
		$('.cancel').click(function(event){
			event.preventDefault();
			$('#Espaco').dialog('close');
			$('#Espaco').empty();
		});
	}});
}
	
$.fn.showRegisterView = function(event){
	event.preventDefault();
	$.ajax({url:'register',beforeSend:$.fn.animateProgress,success:function(data){
		$('#Espaco').Dialog(data);
		$('.submit').click(function(event){
			event.preventDefault();
			$('form').submit();
		});
		$('.cancel').click(function(event){
			event.preventDefault();
			$('#Espaco').dialog('close');
			$('#Espaco').empty();
		});
	}});		
}

$.fn.slideWhoPage = function(event){
	event.preventDefault();
	$('#Central').translate2D($.e.w,0);
	setTimeout(function(){
		$('#Pagina').load('templates/start.html #who',function(){
			$('.back').click($.fn.backToHome);
			$('body').css({'background':'#c00'});
			$('#Pagina').show();
		});
	},1000);
}

$.fn.slideWhatPage = function(event){
	event.preventDefault();
	$('#Central').translate2D(0,$.e.h);
	setTimeout(function(){
		$('#Pagina').load('templates/start.html #what',function(){
			$('.back').click($.fn.backToHome);
			$('body').css({'background':'black'});
			$('#Pagina').show();
		});
	},1000);
}

$.fn.slideHowPage = function(event){		
	event.preventDefault();
	$('#Central').translate2D(-$.e.w,0);
	setTimeout(function(){
		$('#Pagina').load('templates/start.html #how',function(){
			$('.back').click($.fn.backToHome);
			$('body').css({'background':'white'});
			$('#Pagina,#Rodape').css({'color':'black'});
			$('#Pagina').show();
		});
	},1000);
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