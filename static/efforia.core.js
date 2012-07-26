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
		$.fn.loadDialogW(data);
		$('.header').remove();
		$('.right').remove();
		$('.left').css({'width':'100%','margin-left':'0%'});
		$('.submit').click(function(event){
			event.preventDefault();
			$('form').submit();
			//$.post('place',$('form').serialize(),function(data){});
		});
	});
}