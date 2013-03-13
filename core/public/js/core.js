$.fn.doNothing = function(event){
	event.preventDefault();
}

$.fn.Mosaic = function(data){
	$(this).empty().html(data);
	if($('.masonry').length > 0) $('#Grade').masonry('destroy');
	$('#Grade').imagesLoaded(function(){
		$('#Grade').masonry({
			itemSelector: '.block',
			position: 'relative',
			isAnimated: true,
			isFitWidth: true,
			gutterWidth: 5,
			columnWidth: function(containerWidth){
				return $('.span3').width();
			}
		});
	});
}

$.fn.Window = function(data){
	$(this).empty().html(data);
	$(this).modal();
}

$.fn.changeOption = function(event){
	event.preventDefault();
	var next = $(this).attr('next');
	$.get($(this).attr('href'),{},function(data){
		$('.form').html(data);
		$('.send')
		.removeClass('uploadspread postspread eventspread videospread imagespread pagespread '+ 
					 'procfg imgcfg controlcfg placecfg socialcfg '+
					 'projectcreate movementcreate grabcreate')
		.addClass(next);
		$.e.uploadOpt['url'] = $('#image').attr('action');
		$('.datepicker').datepicker($.e.datepickerOpt);
		$('.upload,.file').fileUpload($.e.uploadOpt);
		if($('.wysiwygtxt').length > 0) $.fn.activateEditor();
		$.fn.eventLoop();
	});
}

$.fn.showContext = function(event){
	event.preventDefault();
	$.ajax({
		url:$(this).attr('href'),
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('#Espaco').html(data).modal();
			$.get($('.active').attr('href'),{},function(data){
				$('.form').html(data);
				$('.datepicker').datepicker($.e.datepickerOpt);
				$('.upload,.file').fileUpload($.e.uploadOpt);
				if($('.wysiwygtxt').length > 0) $.fn.activateEditor();
				$.fn.eventLoop();
			});
		}
	});
}

$.fn.activateInterface = function(){
	$.get('options',{'interface':'interface'},function(data){
		if(data == 1) $('#Canvas').hide();
		else spin.createHelix();
	});
}

$.fn.activateEditor = function(){
	$.get('options',{'typeditor':'typeditor'},function(data){
		if(data == 1) $.e.editorOpt = $.f.simpleEditor;
		else $.e.editorOpt = $.f.advancedEditor;
		$('.wysiwygtxt').wysihtml5($.e.editorOpt);
	});
}

$.fn.activateMonetize = function(){
	$.get('options',{'monetize':'monetize'},function(data){
		if(data == 1) console.log('Deactivated');
		else console.log('Activated');
	});
}

$.fn.submitPlace = function(event){
	event.preventDefault();
	$.ajax({
		url:'place',
		type:'POST',
		data:$('#place').serialize(),
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('#Espaco').modal('hide');
		}
	});
}

$.fn.submitControl = function(event){
	event.preventDefault();
	$.ajax({
		url:'appearance',
		type:'POST',
		data:{
			'interface':$('.interface .active').val(),
			'typeditor':$('.typeditor .active').val(),
			'language':$('.language .active').val(),
			'monetize':$('.monetize .active').val(),
		},
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			window.location = '/';
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
				beforeSend: function(){ $('.send').button('loading'); },
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

$.fn.submitChanges = function(event){
	event.preventDefault();
	$.ajax({
		url:'profile',
		type:'POST',
		data:$('#profile').serialize(),
		beforeSend:function(){ $('.send').button('loading'); },
		success:function(data){
			$('#Espaco').modal('hide');
			return window.location = '/';
		}
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
						$('.send').button('loading');
					},
					success:function(data){
						$('#Espaco').modal('hide');
						return window.location = '/';
					}
				});
			});
		}
	});
}

$.fn.deleteObject = function(event){
	event.preventDefault();
	var object_id = $('#Espaco .id').text().trim();
	var object_token = $('#Espaco .token').text().trim();
	$.get('delete',{'id':object_id,'token':object_token},function(data){
		$('#Espaco').modal('hide');
		window.location = '/';
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

$.fn.authenticate = function(event){
	event.preventDefault();
	$.get('enter', $('.navbar-form').serialize(), function(data) {
		return window.location = '/';
	});
}

$.fn.getInitialFeed = function(){
	$.ajax({
		url:'/',
		data:{'feed':'feed'},
		beforeSend:function(){ 
			$('.send').button('loading');
		},
		success:function(data){
			$.e.initial = true; 
			$('#Grade').Mosaic(data);
			$.fn.eventLoop();
			$.e.initial = false;
		}
	}); 	
}

$.fn.unFan = function(event){
	event.preventDefault();
	$.ajax({
		type:'POST',
		url:'fan',
		data:{'id':$(this).find('.id').text()},
		beforeSend:function(){ $('.send').button('loading'); },
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
		beforeSend:function(){ $('.send').button('loading'); },
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
		beforeSend:function(){ $('.send').button('loading'); },
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

$.fn.showPage = function(event){
	event.preventDefault();
	$.get('pageview',{'title':$(this).text()},function(data){
		$('.main').html(data);
	});
}
