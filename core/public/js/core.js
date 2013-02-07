$.fn.changeOption = function(event){
	event.preventDefault();
	var next = $(this).attr('next');
	$.get($(this).attr('href'),{},function(data){
		$('.form').html(data);
		$('.send')
		.removeClass('uploadspread postspread eventspread videospread listspread')
		.addClass(next);
		$.fn.eventLoop();
	});
}

$.fn.showContext = function(event){
	event.preventDefault();
	$.ajax({
		url:$(this).attr('href'),
		beforeSend:function(){ /*$('#Espaco').Progress();*/ },
		success:function(data){
			$('#Espaco').html(data).modal()
			//$('.action0').html('Favoritos');
			//$('.action1').html('Páginas');
			//$('.action2').html('Voltar').attr('class','backmenu');
			$.get($('.active').attr('href'),{},function(data){
				$('.form').html(data);
				$('#spreadtext').wysihtml5({'lists':'false'});
				$.fn.eventLoop();
			});
			//$.fn.eventLoop();
		}
	});
}

$.fn.newSelection = function(event){ 
	$.e.selection = true; 
	$(this).showMosaic(event); 
}

$.fn.logout = function(event){
	event.preventDefault();
	$.get('leave',{},function(data){
		console.log(data);
		window.location = '/';
	});
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
			$.ajax({
				url:href,
				type:'POST',
				data:{'objects':objs,'title':title},
				beforeSend: function(){ $('#Espaco').Progress(); },
				success: function(data){
					$.get(href,{'view':'view','title':title},function(data){
						$('#Grade').Mosaic(data);
						//$('#Espaco').empty().modal('hide');
						$.fn.eventLoop();
						$.e.selection = false;
					});
				}
			});
		});
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
	$.post('profile',{'name':name,'value':value},function(data){
		$(data).parent().parent().find('#statechange').html('<img src="static/img/ok.png"></img>');
		$.get('leave',{},function(data){ $('.brand').redirect(event); });
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
		$('#Espaco').modal('hide');
	});
}

$.fn.creditInfo = function(event){
	event.preventDefault();
	$('#Espaco').load('templates/tutorial.html #credit',function(){
		$('#Espaco').css({'background':'#222','border-radius':'50px'});
		$('#Espaco').show();
		$.fn.eventLoop();
	});
}

$.fn.navigationInfo = function(event){
	event.preventDefault();
	$('#Espaco').load('templates/tutorial.html #navigation',function(){
		$('#Espaco').css({'background':'#222','border-radius':'50px'});
		$('#Espaco').show();
		$.fn.eventLoop();
	});
}

$.fn.finishTutorial = function(event){
	event.preventDefault();
	$.post('userid',{},function(data){});
	$.fn.getInitialFeed();
}

$.fn.getInitialFeed = function(){
	var first = '';
	/*$.get('userid',{'first_turn':'first_turn'},function(data){ 
		if(data == 'yes'){
			$('#Espaco').Context('',$.e.h-50,$('#Canvas').width());
			$('#Espaco').load('static/tutorial.html #process',function(){
				$('#Espaco').css({'background':'#222','border-radius':'50px'});
				$('#Espaco').show();
				$.fn.eventLoop();
			});
		}else{*/
			$.ajax({
				url:'/',
				data:{'feed':'feed'},
				beforeSend:function(){ 
					//$('#Espaco').Progress();
				},
				success:function(data){
					$.e.initial = true; 
					$('#Grade').Mosaic(data);
					$('#Grade').css({'height':window.innerHeight});
					$.fn.eventLoop();
					$.e.initial = false; 
					//$('#Espaco').empty().modal('hide');
					if($(window).innerWidth() < 980){
						$('body').css({'font-size':'0.8em'});
						$('.block').each(function(index){
							$(this).removeClass('block').addClass('mini');
						});
					}
				}
			});
		/*}
	});*/ 	
}

$.fn.unFan = function(event){
	event.preventDefault();
	$.ajax({
		type:'POST',
		url:'fan',
		data:{'id':$(this).find('.id').text()},
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){
			$.fn.getInitialFeed();
			$.fn.eventLoop();
			$.get('known',{'info':'user'},function(data){ $('#Esquerda').html(data); $.fn.eventLoop(); });
		}
	});
}

$.fn.profileFan = function(event){
	event.preventDefault();
	$.ajax({
		url:'fan',
		data:{'text':$('#fan').text()},
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){
			$.fn.getInitialFeed();
			$.fn.eventLoop();
			$.get('known',{'info':'user'},function(data){ $('#Esquerda').html(data); $.fn.eventLoop(); });
		}
	});
}

$.fn.loadProfileObject = function(event){
	event.preventDefault();
	$.get('known',{'info':$(this).find('.name').text()},function(data){ 
		$('.profilehead').html(data);
		$.fn.eventLoop();
	});
	$.ajax({
		url:'known',
		data:{'activity':$(this).find('.name').text()},
		beforeSend:function(){ $('#Espaco').Progress(); },
		success:function(data){	$('#Espaco').empty().modal('hide'); $('#Grade').Mosaic(data); $.fn.eventLoop(); }
	});
	$.fn.showMenus();
}

$.fn.loadMosaic = function(data){
	$('#Grade').Mosaic(data);
	$('#Espaco').empty().modal('hide');
	$.fn.hideMenus();
	if(!$.e.initial) $('.return').parent().show()
	$.fn.eventLoop();
}

$.fn.loadMoreMosaic = function(event){
	event.preventDefault();
	number = $(this).attr('name');
	$.post($(this).attr('href'),{'number':number},function(data){
		$('#Grade').translate(0,0); $.e.marginTop = 0;
		$('#Grade').loadMosaic(data);
		//if($('.blank').text() != '') $.e.marginFactor = 0;
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
	$('#Espaco').empty().modal('hide');
	$('#Player').tubeplayer('destroy');
}

$.fn.backToHome = function(event){
	event.preventDefault();
	$('#Pagina').hide();
	$('body').css({'background':'#222'});
	$('#Pagina,.footer').css({'color':'white'})
	setTimeout(function(){
		$('#Central').translate(0,0);
	});
}

$.fn.showMessage = function(event){
	event.preventDefault();
	$('#Direita').animate({'right':'-15%'});
	$('#Direita').animate({'right':'0%'});
}

$.fn.gotoSocial = function(event){
	$(this).redirect(event);
}

$.fn.showMosaic = function(event){
	event.preventDefault();
	$.ajax({
		url:$(this).attr('href'),
		beforeSend:$('#Espaco').Progress(),
		success:function(data){ 
			$('#Grade').loadMosaic(data); 
			$.fn.hideMenus();
			$.fn.eventLoop();
		}
	});
}

$.fn.showPlaceView = function(event){
	event.preventDefault();
	$.get('place',{},function(data){
		$('#Espaco').Dialog(data);
		$('.submit').css({'width':50});
		$.fn.eventLoop();
	});
}

$.fn.showLoginView = function(event){
	event.preventDefault();
	$.ajax({url:'login',beforeSend:$.fn.animateProgress,success:function(data){
		$('#Espaco').Dialog(data);
		$('#id_password').on('keypress',function(event){ if(event.which == 13) $('form').submit(); });
		$('.submit').css({'width':50});
		$.fn.eventLoop();
	}});
}
	
$.fn.showRegisterView = function(event){
	event.preventDefault();
	birthday = '<div><label>Aniversário</label><input id="birthday" type="text" class="date"></input></div>'
	$.ajax({url:'register',beforeSend:$.fn.animateProgress,success:function(data){
		$('#Espaco').Dialog(data);
		//$('#Espaco').find('#etiquetas').append(birthday);
		$('#id_birthday').datepicker($.e.birthdayOpt);
		$('#id_birthday').datepicker('option',$.datepicker.regional['pt-BR']);
		$('.submit').css({'width':50});
		$.fn.eventLoop();
	}});		
}

$.fn.slideWhoPage = function(event){
	event.preventDefault();
	$('#Central').translate($.e.w,0);
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
	$('#Central').translate(0,$.e.h);
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
	$('#Central').translate(-$.e.w,0);
	setTimeout(function(){
		$('#Pagina').load('templates/start.html #how',function(){
			$('.back').click($.fn.backToHome);
			$('body').css({'background':'white'});
			$('#Pagina,.footer').css({'color':'black'});
			$('#Pagina').show();
		});
	},1000);
}

$.fn.hideMenus = function(){
	$('#Canvas').css({'opacity':0,'display':'none'});
	$('.back').parent().show('fade');
}

$.fn.showMenus = function(){
	$('.back').parent().hide('fade');
    $('#Canvas').css({'opacity':1,'display':''});
}

$.fn.showAbout = function(event){
	event.preventDefault();
	$('#Central').translate(0,$.e.h);
	setTimeout(function(){
		$('#Pagina').load('templates/pages.html #about',function(){
			$('.back').click($.fn.backToHome);
			$('body').css({'background':'white'});
			$('#Pagina,.footer').css({'color':'black'});
			$('#Pagina').show();
		});
	},1000);
}

$.fn.showTerms = function(event){
	event.preventDefault();
	$('#Central').translate(0,$.e.h);
	setTimeout(function(){
		$('#Pagina').load('templates/pages.html #terms',function(){
			$('.back').click($.fn.backToHome);
			$('body').css({'background':'white'});
			$('#Pagina,.footer').css({'color':'black'});
			$('#Pagina').show();
		});
	},1000);
}

$.fn.showCopyright = function(event){
	event.preventDefault();
	$('#Central').translate(0,$.e.h);
	setTimeout(function(){
		$('#Pagina').load('templates/pages.html #copyright',function(){
			$('.back').click($.fn.backToHome);
			$('body').css({'background':'white'});
			$('#Pagina,.footer').css({'color':'black'});
			$('#Pagina').show();
		});
	},1000);
}

$.fn.showRules = function(event){
	event.preventDefault();
	$('#Central').translate(0,$.e.h);
	setTimeout(function(){
		$('#Pagina').load('templates/pages.html #rules',function(){
			$('.back').click($.fn.backToHome);
			$('body').css({'background':'white'});
			$('#Pagina,.footer').css({'color':'black'});
			$('#Pagina').show();
		});
	},1000);
}

$.fn.showContact = function(event){
	event.preventDefault();
	$('#Central').translate(0,$.e.h);
	setTimeout(function(){
		$('#Pagina').load('templates/pages.html #contact',function(){
			$('.back').click($.fn.backToHome);
			$('body').css({'background':'white'});
			$('#Pagina,.footer').css({'color':'black'});
			$('#Pagina').show();
		});
	},1000);
}
