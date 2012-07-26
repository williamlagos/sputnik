var w = window.innerWidth;
var h = window.innerHeight;
var currentTime = new Date();
var erasedField = false;
var selection = false;
var price = 1.19;
var value = 0.0;
var option = 0;
var token = '';
var objects = [];
var control = " ui-button ui-widget ui-state-default ui-corner-all\" style=\"padding: .4em 1em;\"><span class=\"ui-icon "
var currentYear = currentTime.getFullYear()-13
var birthdayOpt = {
	defaultDate:'-13y',
	dateFormat:'d MM, yy',
	changeMonth:true,
	changeYear:true,
	yearRange:"1915:"+currentYear,
	showOn: "button",
	buttonImage: "images/calendar.png",
	buttonImageOnly: true,
	onClose: function(){ this.focus(); }
}
var eventOption = {
	changeMonth:true,
	changeYear:true,
	showOn: "button",
	buttonImage: "images/calendar.png",
	buttonImageOnly: true,
	onClose: function(){ this.focus(); }
}

$.fn.newItem = function(event){
	event.preventDefault();
	refer = $(this).attr('href');
	$.fn.showContext(event,refer,function(data){ $('#Grade').loadMosaic(data); $('#Espaco').dialog('destroy'); });
}

$.fn.selectVideo = function(event){
	event.preventDefault();
	$.fn.hideMenus();
	$.post('collection',{},function(data){
		$('#Grade').empty();
		$('#Grade').html(data);
		$('.mosaic-block').mosaic();
		$('.playable').click(function(event){
			event.preventDefault();
			token = $(this).parent().attr('href');
			$.fn.showMenus();
			$('#Espaco').dialog('open');
		});
	});
}

$.fn.openDeliverable = function(event){
	event.preventDefault();
	$.get('delivery',{'quantity':$('.title').text(),'credit':$('.description').text()},function(data){ 
		button = "<div class=\"buttons-center\"><a class=\"deliver\" style=\"width:285px;\">Calcular frete</a></div><div class=\"address\"></div>"
		$.fn.showDataContext('Comprar um produto',data);
		$('#Esquerda,#Abas').show('fade');
		$('#Espaco').css({'background':'#222','border-radius':'50px','height':$('#Canvas').height()-5});
		$('#etiquetas').css({'text-align':'center'});
		$('.header').html('Compra de Produto');
		$('.tutor').html('Aqui é possível comprar produtos com os créditos do Efforia. Eles podem ser adquiridos na barra lateral ou no painel de controle do site, localizado logo ao lado da barra de busca.')
		$('.tutor').css({'margin-top':'5%','width':'80%'}) 
		$('#id_mail_code').parent().append(button);
		$('.deliver').button();
		$('.deliver').click(function(event){
			event.preventDefault();
			$.get('correios',$('#defaultform').serialize(),function(data){
				$('.address').html(data);
			});
		});
	});
}

$.fn.openProduct = function(event){
	event.preventDefault();
	$.get('products',{'product':$(this).find('.time').text()},function(data){ 
		$('#Espaco').loadDialogT(data);
		$('.cart').click(function(event){
			event.preventDefault();
			$.post('cart',{'time':$('#Espaco').find('.time').text()},function(data){alert(data);})
		}); 
	});
}

$.fn.showMessage = function(event){
	event.preventDefault();
	$('#Direita').animate({'right':'-15%'});
	$('#Direita').animate({'right':'0%'});
}

$.fn.gotoSocial = function(event){
	event.preventDefault();
	window.location = $(this).attr('href');
}

$.fn.buyMoreCredits = function(event){
	event.preventDefault();
	$.get('payment',{},function(data){
		$.fn.loadDialogT(data);
		$('#payment').children().find('input[type=image]').attr('width','240');
		$('#payment').children().find('input[type=image]').attr('src','images/paypal.png');
		$('#payment').children().find('input[type=image]').click($.fn.getRealPrice);
		$('.calculate').click($.fn.calculatePrice);
	});
}

$.fn.createNewProduct = function(event){
	event.preventDefault();
	$.get('products',{'action':'creation'},function(data){
		$.fn.showDataContext('Criar um produto',data);
		$('#Esquerda,#Abas').show('fade');
		$('#Espaco').css({'background':'#222','border-radius':'50px','height':$('#Canvas').height()-5});
		$('.header').html('Publicação de um Produto')
		$('.tutor').html('Aqui é possível incluir seus produtos dentro do portal Efforia. Com isso, eles aproveitam as facilidades de frete e de divulgação nas redes sociais que o Efforia oferece.')
		$('.tutor').css({'margin-top':'35%','width':'80%'})
		$('.submit').click(function(event){
			event.preventDefault();
			action = $('#defaultform').attr('action');
			$.post(action,$('#defaultform').serialize(),function(data){/*alert(data);*/});
		});
	});
}

$.fn.showProducts = function(event){
	event.preventDefault();
	$.get('products',{},function(data){$('#Grade').loadMosaic(data);});
}

$.fn.createEvents = function(){
	$.ajaxSetup({cache:false});
	$('.place').click($.fn.registerPlace);
	$('.spreadablespread').click($.fn.openSpreadableSpread);
	$('.eventspread').click($.fn.openEventSpread);
	$('.causablespread').click($.fn.openCausableSpread);
	$('.new').click($.fn.newItem);
	$('#selectupload').click($.fn.selectVideo);
	$('.purchase').click($.fn.openDeliverable);
	$('.product').click($.fn.openProduct);
	$('#Direita').click($.fn.showMessage);
	$('#radio').buttonset();
	$('.social').click($.fn.gotoSocial);
	$('.buyable').click($.fn.buyMoreCredits);
	$('.creation').click($.fn.createNewProduct);
	$('.products').click($.fn.showProducts);
	$('#overlay').hide();
	$('#upload').click($.fn.fileInput);
	$('#id_username,#id_email,#id_last_name,#id_first_name').addClass('eraseable');
	$('#payment').children().find('input[type=image]').attr('width','240');
	$('#payment').children().find('input[type=image]').attr('src','images/paypal.png');
	$('#payment').children().find('input[type=image]').click($.fn.getRealPrice);
	$('.calculate').click($.fn.calculatePrice);
	$('.register').click($.fn.loadNewDialog);
	$('.eraseable').click($(this).editNewField);
	$('.select').change($.fn.changeSelection);
	$('.selection').click($(this).createSelection);
	$('.return').click($.fn.showMenus);
	$('#spreadpost').click($.fn.submitSpread);
	$('#causeupload').click($(this).submitTrigger);
	$('#causeupload').submit($.fn.submitCause);
	$('#content').click($.fn.submitPlay);
	$('#eventpost').click($.fn.submitEvent);
	$('#datepicker').datepicker(birthdayOpt).keydown($.fn.sendNewField);
	$('#start_time,#end_time').datepicker(eventOption);
	$('#id_username,#id_email,#id_last_name,#id_first_name,#datepicker').keyup($.fn.sendNewField);
	$('#datepicker').datepicker('option',$.datepicker.regional['pt-BR'])
	$('#password').click($.fn.submitPasswordChange);
	$('.message').click($.fn.loadListContext);
	$('.mosaic-overlay').click($(this).clickContent);
	$('.spreadable,.event').click($.fn.loadTextObject);
	$('.causable').click(function(event){
		event.preventDefault();
		if(!selection){
			object = $(this).find('.time').text();
			data = '<div id="Container"><div id="Message"></div><div id="Player"></div><div id="slider-range-min"></div>'+
							  '<div style="width:50%; float:left; margin-top:10px;">'+
							  "<div style=\"float:left;\"><a onclick=\"$('#Player').tubeplayer('pause');\" class=\"pcontrols "+control+"ui-icon-pause\"></span></a></div>"+
							  "<div style=\"float:left;\"><a class=\"mute "+control+"ui-icon-volume-off\"></span></a></div></div>"+
							  "<div style=\"width:50%; float:right; text-align:right; margin-top:10px;\">"+
							  "<a class=\"spread"+control+"ui-icon-star\"></span></a>"+
							  "<a class=\"deletable"+control+"ui-icon-trash\"></span></a></div></div>"
			$.fn.loadDialogT(data);
			$('.spread').click(function(event){
				event.preventDefault();
				related = "<div class=\"time\" style=\"display:none;\">"+time+"</div>"
				$.get('spread',{'spread':'cause'},function(data){
					$.fn.showDataContext('',data+related);
					$('#Espaco').css({'background':'#222','border-radius':'50px'});
					$('#spreadpost').click(function(event){
						event.preventDefault();
						$.post('spread',{'spread':$('#id_content').val(),'time':object},function(data){
							alert(data);
							$('#Espaco').dialog('close');
						});
					});
				});
			});
			$('.deletable').click($.fn.deleteObject);
			$('#Espaco').css({'width':800,'height':500});
			$("#Player").tubeplayer({
				width: 770, // the width of the player
				height: 400, // the height of the player
				autoPlay: true,
				showinfo: false,
				autoHide: true,
				iframed: true,
				showControls: 0,
				allowFullScreen: "true", // true by default, allow user to go full screen
				initialVideo: $(this).parent().attr('href'), // the video that is loaded into the player
				preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
				onPlay: function(id){$('.pcontrols').parent().html("<a onclick=\"$('#Player').tubeplayer('pause');\" class=\"pcontrols "+control+"ui-icon-pause\" ></span></a>");},
				onPause: function(){$('.pcontrols').parent().html("<a onclick=\"$('#Player').tubeplayer('play');\" class=\"pcontrols "+control+"ui-icon-play\" ></span></a>");},
				onMute: function(){$('.mute').parent().html("<a onclick=\"$('#Player').tubeplayer('unmute');\" class=\"unmute "+control+"ui-icon-volume-on\" ></span></a>");},
				onUnMute: function(){$('.unmute').parent().html("<a onclick=\"$('#Player').tubeplayer('mute');\" class=\"mute "+control+"ui-icon-volume-off\" ></span></a>");},
				onStop: function(){}, // after the player is stopped
				onSeek: function(time){}, // after the video has been seeked to a defined point
				onPlayerPlaying: function(){},
				onPlayerEnded: function(){ 
					$('#Player').hide();
					$('.message').html('<h2>Reproduzir novamente?</h2>');
				}
			});
			$('.mute').click(function(event){
				event.preventDefault();
				$('#Player').tubeplayer('mute');
			});
			$('.unmute').click(function(event){
				event.preventDefault();
				$('#Player').tubeplayer('unmute');
			});
			$('#Espaco').bind('dialogclose',function(event,ui){ $('#Player').tubeplayer('destroy'); });
			$('#Espaco').dialog('option','position','center');
		}
	});
	$('.playable').click($.fn.loadPlayObject);	
	$('.movement,.schedule').click($.fn.loadListMosaic);
	$('.loadable').click($.fn.loadMoreMosaic);
	$('.profile').click($.fn.loadProfileObject);
	$('.mosaic-block').click(function(){ $.view.value = false; });
	$('.video').click(function(event){
		event.preventDefault();
		$.get('expose',$('#conteudo').serialize()+'&category='+option,function(data){
			$('#conteudo').parent().html(data);
			$('#overlay').hide();
			$('#upload').click($.fn.fileInput);
			$('.videoupload').click(function(event){
				event.preventDefault();
				$('#conteudo').submit();
			});
		});
	});
	$('.login').click(function(event){
		event.preventDefault();
		$.ajax({url:'login',beforeSend:$.fn.animateProgress,success:function(data){
			$.fn.loadDialogW(data);
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
	});
	$('.register').click(function(event){
		event.preventDefault();
		$.ajax({url:'register',beforeSend:$.fn.animateProgress,success:function(data){
			$.fn.loadDialogW(data);
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
	});
	$('.who').click(function(event){
		event.preventDefault();
		$('#Central').translate2D(w,0);
		setTimeout(function(){
			$('#Pagina').load('templates/start.html #who',function(){
				$('.back').click($.fn.backToHome);
				$('body').css({'background':'#c00'});
				$('#Pagina').show();
			});
		},1000);
	});
	$('.what').click(function(event){
		event.preventDefault();
		$('#Central').translate2D(0,h);
		setTimeout(function(){
			$('#Pagina').load('templates/start.html #what',function(){
				$('.back').click($.fn.backToHome);
				$('body').css({'background':'black'});
				$('#Pagina').show();
			});
		},1000);
	});
	$('.how').click(function(event){		
		event.preventDefault();
		$('#Central').translate2D(-w,0);
		setTimeout(function(){
			$('#Pagina').load('templates/start.html #how',function(){
				$('.back').click($.fn.backToHome);
				$('body').css({'background':'white'});
				$('#Pagina,#Rodape').css({'color':'black'});
				$('#Pagina').show();
			});
		},1000);
	});
	$('input[type=file]').fileUpload({
		url:'expose',
		type:'POST',
		beforeSend:$.fn.verifyValues,
		xhr:$.fn.uploadProgress,
		success:$.fn.finishUpload
	});
}
