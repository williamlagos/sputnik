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

Array.prototype.removeItem = function(str) {
   	for(i=0; i<this.length ; i++){
     	if(escape(this[i]).match(escape(str.trim()))){
       		this.splice(i, 1);  break;
    	}
	}
	return this;
}

$.fn.submitTrigger = function(event){
	event.preventDefault();
	$(this).submit();
}

$.fn.changeSelection = function(event){
	event.preventDefault();
	option = $("select option:selected").val();
}

$.fn.editNewField = function(event){
	event.preventDefault();
	if(!$(this).hasClass('erased')){
		$(this).attr('value','');
		$(this).addClass('erased');
	}
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

$.fn.fileInput = function(event){
	event.preventDefault();
	$('input:file').click(); 
}

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
				$.get(href,{'view':'view'},$('#Grade').loadMosaic);
				$.fn.showMenus();
				$('#Espaco').html(data);
				$('#Espaco').dialog('open');
			});
			selection = false;
		});
		//$(this).attr('class','mosaic-overlay title');
	}
}

$.fn.clickContent = function(event){
	event.preventDefault();
	if(selection){
		time = $(this).find('.time').text();
		if($(this).attr('class') == 'mosaic-overlay selected'){
			objects.removeItem(time);
			$(this).attr('style','background:url(../images/bg-black.png); display: inline; opacity: 0;')
			$(this).attr('class','mosaic-overlay');
		}else{
			$(this).attr('style','background:url(../images/bg-red.png); display: inline; opacity: 0;')
			$(this).attr('class','mosaic-overlay selected');
			objects.push(time);
		}
	}
}

$.fn.submitCause = function(event){
	event.preventDefault();
	if(option == 0){
		alert('Selecione uma das categorias listadas.');
		return;
	}/*else if(token == ''){
		alert('Faça o upload de um vídeo antes.');
		return;
	}*/
	serialized = $('#causas').serialize()+'&category='+option+'&token='+token;
	$.post('causes',serialized,function(data){ 
		$.fn.hideMenus();
		$('#Grade').loadMosaic(data);
	});
}

$.fn.submitSpread = function(event){
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
}

$.fn.submitPlay = function(event){
	event.preventDefault();
	$.post('content',{},function(data){
		$.fn.hideMenus(); 
		$('#Grade').loadMosaic(data); 
	});
}

$.fn.submitEvent = function(event){
	event.preventDefault();
	$.post('calendar',$('#evento').serialize(),function(data){
		$.fn.hideMenus(); 
		$('#Grade').loadMosaic(data); 
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

$.fn.loadListContext = function(event){
	if($('#message').text() == 'Você não possui nenhum movimento. Gostaria de criar um?'){
		$.fn.showContext(event,'movement?action=grid',function(data){$('#Grade').loadMosaic(data);});
	}else if($('#message').text().indexOf('Movimentos em aberto') != -1){
		$.fn.showContext(event,'movement?view=grid',function(data){$('#Grade').loadMosaic(data);});
	}else if($('#message').text().indexOf('Programações disponíveis') != -1){
		$.fn.showContext(event,'schedule?view=grid',function(data){$('#Grade').loadMosaic(data);});	
	}else{
		$.fn.showContext(event,'schedule?action=grid',function(data){$('#Grade').loadMosaic(data);});
	}
	$('#message').empty();
	$.fn.hideMenus(event);
	$('#Espaco').dialog('close');
	selection = true;
}

$.fn.deleteObject = function(event){
	event.preventDefault();
	$.get('delete',{'text':$('#Espaco').find('.time').text()},function(data){
		$.get('/',{'feed':'feed'},function(data){$('#Grade').loadMosaic(data);});
		$('#Espaco').dialog('close');
	});
}

$.fn.loadTextObject = function(event){
	event.preventDefault();
	$('#Espaco').html($(this).html()+'<div style="width:50%; float:left;"><a class="spread ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em 1em;"><span class="ui-icon ui-icon-star"></span></a></div>'+
									 '<div style="width:50%; float:right; text-align:right;"><a class="deletable ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em 1em;"><span class="ui-icon ui-icon-trash"></span></a></div>');
	$('#Espaco').dialog({
		title:'Objeto',height:'auto',width:'auto',modal:true,
		position:'center',resizable:false,draggable:false
	});
	$('.spread').click(function(event){
		event.preventDefault();
		related = "<div class=\"time\" style=\"display:none;\">"+$('#Espaco').find('.time').text()+"</div>"
		$.get('spread',{},function(data){
			$('#Espaco').html(data+related);
			$('#Espaco').dialog('option','position','center');
			$('#spreadpost').click(function(event){
				event.preventDefault();
				$.post('spread',{'spread':$('#id_content').val(),'time':$('#Espaco').find('.time').text()},function(data){
					alert(data);
				});
			});
		});
	});
	$('.deletable').click($.fn.deleteObject);
}

$.fn.loadPlayObject = function(event){
	event.preventDefault();
	$('#Espaco').html('<div id="Container"><div id="Message"></div><div id="Player"></div><div id="slider-range-min"></div>'+
					  '<div style="width:50%; float:left; margin-top:10px;">'+
					  "<div style=\"float:left;\"><a onclick=\"$('#Player').tubeplayer('pause');\" class=\"pcontrols "+control+"ui-icon-pause\"></span></a></div>"+
					  "<div style=\"float:left;\"><a class=\"mute "+control+"ui-icon-volume-off\"></span></a></div></div>"+
					  "<div style=\"width:50%; float:right; text-align:right; margin-top:10px;\">"+
					  "<a class=\"fan"+control+"ui-icon-star\"></span></a>"+
					  "<a class=\"deletable"+control+"ui-icon-trash\"></span></a></div></div>");
	$('#Espaco').dialog({
		title:$(this).find('h2').text(),height:525,width:800,modal:true,
		position:'center',resizable:false,draggable:false
	});
	$('.fan').click(function(event){
		event.preventDefault();
		$.get('fan',{'text':$('#Espaco').find('.time').text()},function(data){
			$('#Grade').loadMosaic(data);
			$('#Espaco').dialog('close');
		});
	});
	$('.deletable').click($.fn.deleteObject);
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
			$('#Message').html('<h2>Reproduzir novamente?</h2>');
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

$.fn.loadListMosaic = function(event){
	event.preventDefault();
	title = $(this).find('h2').html();
	refer = $(this).attr('href');
	$.get(refer,{'view':refer,'title':title},function(data){
		$('#Grade').translate2D(0,0); $.view.marginTop = 0;
		$('#Grade').loadMosaic(data);
	});
}

$.fn.loadMoreMosaic = function(event){
	event.preventDefault();
	number = $(this).attr('name');
	$.post($(this).attr('href'),{'number':number},function(data){
		$('#Grade').translate2D(0,0); $.view.marginTop = 0;
		$('#Grade').loadMosaic(data);
		if($('.blank').text() != '') $.view.marginFactor = 0;
	});
}

$.fn.loadNewDialog = function(event){
	event.preventDefault();
	href = $(this).attr('href');
	$.ajax({
		url:href,
		beforeSend:$.fn.animateProgress,
		success:function(data){
			$.fn.loadDialogT(data);
			$('#id_username').focus();
		}
	});
}

$.fn.calculatePrice = function(event){
	event.preventDefault();
	value = ($('#id_credits').val()*price).toFixed(2);
	$('#value').html(value);
	$.fn.getRealPrice(event);
}

$.fn.getRealPrice = function(event){
	real_value = price.toFixed(2);
	$('#payment').children().find('input[name=amount]').attr('value',real_value);
	$('#payment').children().find('input[name=quantity]').attr('value',$('#id_credits').val());
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

$.fn.createEvents = function(){
	$.ajaxSetup({cache:false});
	$('.purchase').click(function(event){
		event.preventDefault();
		$.get('delivery',{'quantity':$('.title').text(),'credit':$('.description').text()},function(data){ 
			button = "<div class=\"buttons-center\"><a class=\"deliver\" style=\"width:285px;\">Calcular frete</a></div><div class=\"address\"></div>"
			$('#Espaco').loadDialog(data); 
			$('#id_mail_code').parent().append(button);
			$('.deliver').button();
			$('.deliver').click(function(event){
				event.preventDefault();
				$.get('correios',$('#defaultform').serialize(),function(data){
					$('.address').html(data);
				});
			});
		});
	});
	$('.product').click(function(event){
		event.preventDefault();
		$.get('products',{'product':$(this).find('.time').text()},function(data){ 
			$('#Espaco').loadDialogT(data);
			$('.cart').click(function(event){
				event.preventDefault();
				$.post('cart',{'time':$('#Espaco').find('.time').text()},function(data){alert(data);})
			}); 
		});
	});
	$('#Direita').click(function(event){
		event.preventDefault();
		$('#Direita').animate({'right':'-15%'});
		$('#Direita').animate({'right':'0%'});
	});
	$('#radio').buttonset();
	$('.social').click(function(event){
		event.preventDefault();
		window.location = $(this).attr('href');
	});
	$('.buyable').click(function(event){
		event.preventDefault();
		$.get('payment',{},function(data){
			$.fn.loadDialog(data);
			$('#payment').children().find('input[type=image]').attr('width','240');
			$('#payment').children().find('input[type=image]').attr('src','images/paypal.png');
			$('#payment').children().find('input[type=image]').click($.fn.getRealPrice);
			$('.calculate').click($.fn.calculatePrice);
		});
	});
	$('.creation').click(function(event){
		event.preventDefault();
		$.get('products',{'action':'creation'},function(data){
			$.fn.loadDialog(data);
			$('.submit').click(function(event){
				event.preventDefault();
				action = $('#defaultform').attr('action');
				$.post(action,$('#defaultform').serialize(),function(data){/*alert(data);*/});
			});
		});
	});
	$('.products').click(function(event){
		event.preventDefault();
		$.get('products',{},function(data){$('#Grade').loadMosaic(data);});
	});
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
	$('#message').click($.fn.loadListContext);
	$('.mosaic-overlay').click($(this).clickContent);
	$('.spreadable,.event').click($.fn.loadTextObject);
	$('.causable,.playable').click($.fn.loadPlayObject);	
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
