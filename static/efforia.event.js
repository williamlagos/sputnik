var w = window.innerWidth;
var h = window.innerHeight;
var currentTime = new Date();
var erasedField = false;
var option = 0;
var token = '';
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

$.fn.clickContent = function(event){
	event.preventDefault();
	if(selection == true){
		href = $(this).attr('href');
		if($(this).attr('class') == 'mosaic-overlay action'){
			if(objects.length < 1) return;
			label = '';
			value = '';
			if(href == 'movement'){
				label = 'Nome do seu movimento:';
				value = 'Criar um movimento';
			}else if(href == 'schedule'){
				label = 'Nome da sua programação:';
				value = 'Criar uma programação';
			}
			$(this).children().html('<form method="post" action="/'+href+
			'" style="text-align:center;">'+label+
			' <input name="title" style="width:100%;"></input><div id="botoes"><input name="create" class="ui-button ui-widget ui-state-default ui-corner-all" type="submit" value="'+value+
			'"></div></form>');
			$('input[name=create]').click(function(event){
				event.preventDefault();
				title = $('input[name=title]').val()
				if(title == '') return;
				objs = objects.join();
				$.post(href,{'objects':objs,'title':title},function(data){
					$.fn.showMenus();
					$('#Espaco').html(data);
					$('#Espaco').dialog('open');
				});
			});
			$(this).attr('class','mosaic-overlay title');
		}else if($(this).attr('class') == 'mosaic-overlay title'){
			return;
		}else if($(this).attr('class') == 'mosaic-overlay selected'){
			objects.removeItem(href);
			$(this).attr('style','background:url(../images/bg-black.png); display: inline; opacity: 0;')
			$(this).attr('class','mosaic-overlay');
		}else{
			$(this).attr('style','background:url(../images/bg-red.png); display: inline; opacity: 0;')
			$(this).attr('class','mosaic-overlay selected');
			objects.push(href);
		}
	}
}

$.fn.submitCause = function(event){
	event.preventDefault();
	if(option == 0){
		alert('Selecione uma das categorias listadas.');
		return;
	}else if(token == ''){
		alert('Faça o upload de um vídeo antes.');
		return;
	}
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
	if($('#message').text() == 'Você não possui nenhum movimento. Gostaria de criar um?' ||
	   $('#message').text().indexOf('Movimentos em aberto') != -1){
		$.fn.showContext(event,'movement?action=grid',function(data){$('#Grade').loadMosaic(data);});	
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
	$('#Espaco').html($(this).html()+'<div style="width:50%; float:left;"><a class="ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em 1em;"><span class="ui-icon ui-icon-star"></span></a></div>'+
									 '<div style="width:50%; float:right; text-align:right;"><a class="deletable ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em 1em;"><span class="ui-icon ui-icon-trash"></span></a></div>');
	$('#Espaco').dialog({
		title:'Objeto',height:'auto',width:'auto',modal:true,
		position:'center',resizable:false,draggable:false
	});
	$('.deletable').click($.fn.deleteObject);
}

$.fn.loadPlayObject = function(event){
	event.preventDefault();
	$('#Espaco').html($(this).html()+'<div id="Container"><div id="Message"></div><div id="Player"></div><div id="slider-range-min"></div>'+
					  '<div style="width:50%; float:left; margin-top:10px;">'+
					  "<div style=\"float:left;\"><a onclick=\"$('#Player').tubeplayer('pause');\" class=\"pcontrols "+control+"ui-icon-pause\"></span></a></div>"+
					  "<div style=\"float:left;\"><a onclick=\"$('#Player').tubeplayer('stop');\" class=\""+control+"ui-icon-stop\"></span></a></div>"+
					  "<div style=\"float:left;\"><a class=\"mute "+control+"ui-icon-volume-off\"></span></a></div></div>"+
					  "<div style=\"width:50%; float:right; text-align:right; margin-top:10px;\">"+
					  "<a class=\"fan"+control+"ui-icon-star\"></span></a>"+
					  "<a class=\"deletable"+control+"ui-icon-trash\"></span></a></div></div>");
	$('#Espaco').dialog({
		title:'Objeto',height:650,width:800,modal:true,
		position:'center',resizable:false,draggable:false
	});
	$('.fan').click(function(event){
		event.preventDefault();
		$.get('fan',{'text':$('#Espaco').find('.time').text()},function(data){
			$('#Grade').loadMosaic(data);
			$('#Espaco').dialog('close');
		});
	})
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
		initialVideo: $(this).attr('href'), // the video that is loaded into the player
		preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
		onPlay: function(id){
			$('.pcontrols').parent().html("<a onclick=\"$('#Player').tubeplayer('pause');\" class=\"pcontrols "+control+"ui-icon-pause\" ></span></a>");
		}, // after the play method is called
		onPause: function(){
			$('.pcontrols').parent().html("<a onclick=\"$('#Player').tubeplayer('play');\" class=\"pcontrols "+control+"ui-icon-play\" ></span></a>");
		}, // after the pause method is called
		onMute: function(){
			$('.mute').parent().html("<a onclick=\"$('#Player').tubeplayer('unmute');\" class=\"unmute "+control+"ui-icon-volume-on\" ></span></a>");
		},
		onUnMute: function(){
			$('.unmute').parent().html("<a onclick=\"$('#Player').tubeplayer('mute');\" class=\"mute "+control+"ui-icon-volume-off\" ></span></a>");
		},
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
}

$.fn.loadListMosaic = function(event){
	event.preventDefault();
	title = $(this).find('h2').html();
	refer = $(this).attr('href');
	$.get(refer,{'view':refer,'title':title},function(data){
		$('#Grade').translate2D(0,0); marginTop = 0;
		$('#Grade').loadMosaic(data);
	});
}

$.fn.loadMoreMosaic = function(event){
	event.preventDefault();
	number = $(this).attr('name');
	$.post($(this).attr('href'),{'number':number},function(data){
		$('#Grade').translate2D(0,0); marginTop = 0;
		$('#Grade').loadMosaic(data);
		if($('.blank').text() != '') marginFactor = 0;
	});
}

$.fn.loadNewDialog = function(event){
	event.preventDefault();
	href = $(this).attr('href');
	$.ajax({
		url:href,
		beforeSend:$.fn.animateProgress,
		success:$.fn.loadDialog
	});
}

$.fn.createEvents = function(){
	$('#overlay').hide();
	$('#id_username,#id_email,#id_last_name,#id_first_name').addClass('eraseable');
	$('.login').click($.fn.loadNewDialog);
	$('.register').click($.fn.loadNewDialog);
	$('.eraseable').click($(this).editNewField);
	$('.select').change($.fn.changeSelection);
	$('.return').click($.fn.showMenus);
	$('#spreadpost').click($.fn.submitSpread);
	$('#causas').click($(this).submitTrigger);
	$('#upload').click($.fn.fileInput);
	$('#causas').submit($.fn.submitCause);
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
	$('a[href=favorites]').click(function(event){$.fn.showContext(event,'favorites',function(data){$('#Grade').loadMosaic(data); $.fn.hideMenus(); });});
	$('input[type=file]').fileUpload({
		url:'expose',
		type:'POST',
		beforeSend:$.fn.verifyValues,
		xhr:$.fn.uploadProgress,
		success:$.fn.finishUpload
	});
}
/*$(document).ready(function(){
var currentTime = new Date();
$('.dialogo').click(function(event){
	event.preventDefault();
	$.ajax({
		url:this.href,
		success: function(data){
			$('#caixa').dialog('destroy');
			$('#caixa').empty();
			$('#caixa').html(data);
			$('#caixa').dialog({title:'Entrar no Efforia',height:'auto',width:'auto',modal:true});
			currentYear = currentTime.getFullYear()-13
			$('#datepicker').datepicker({
				defaultDate:'-13y',
				dateFormat:'mm/dd/yy',
				changeMonth:true,
				changeYear:true,
				yearRange:"1915:"+currentYear,
				showOn: "button",
				buttonImage: "images/calendar.png",
				buttonImageOnly: true,
				onClose: function(){ this.focus(); }
			});
		}
	});
});
$('.popup').click(function(event){
	event.preventDefault();
	$(".popup").popupwindow();
});
});*/
