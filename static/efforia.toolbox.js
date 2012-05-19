Array.prototype.removeItem=function(str) {
   	for(i=0; i<this.length ; i++){
     	if(escape(this[i]).match(escape(str.trim()))){
       		this.splice(i, 1);  break;
    	}
	}
	return this;
}

$(document).ready(function(){

var w = window.innerWidth;
var h = window.innerHeight;
var selection = false;
var objects = [];
var currentTime = new Date();
var openedMenu = false;
var option = 0;
var token = '';

function progressHandlingFunction(e){
    if(e.lengthComputable){
        $('progress').attr({value:e.loaded,max:e.total});
    }
}

function sendNewField(event){
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

function animateProgress(){
	$('#Espaco').empty().dialog('destroy');
	$('#Espaco').dialog({resizable:false,modal:true,height:'auto',width:'auto',minHeight:48});
	$('#Espaco').html("<img src='images/progress.gif'/>");
	$('.ui-dialog-titlebar').remove();
}

function hideMenus(){
    $('#Esquerda:visible').hide('fade');
    $('#Sair:visible').hide('fade');
    $('#Canvas:visible').hide('fade');
    $('#Navegacao:visible').hide('fade');
    $('#Menu:visible').hide();
}

function showMenus(event){
	event.preventDefault();
   	$('#Esquerda:hidden').show('fade');
   	$('#Sair:hidden').show('fade');
    $('#Canvas:hidden').show('fade');
    $('#Navegacao:hidden').show('fade');
    $('#Menu:hidden').hide();
}

function clickContent(event,element){
	event.preventDefault();
	if(selection == true){
		href = element.attr('href');
		if(element.attr('class') == 'mosaic-overlay action'){
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
			element.children().html('<form method="post" action="/'+href+
			'" style="text-align:center;">'+label+
			' <input name="title" style="width:100%;"></input><div id="botoes"><input name="create" class="ui-button ui-widget ui-state-default ui-corner-all" type="submit" value="'+value+
			'"></div></form>');
			$('input[name=create]').click(function(event){
				event.preventDefault();
				title = $('input[name=title]').val()
				if(title == '') return;
				objs = objects.join();
				$.post(href,{'objects':objs,'title':title},function(data){
					showMenus(event);
					$('#Espaco').html(data);
					$('#Espaco').dialog('open');
				});
			});
			element.attr('class','mosaic-overlay title');
		}else if(element.attr('class') == 'mosaic-overlay title'){
			return;
		}else if(element.attr('class') == 'mosaic-overlay selected'){
			objects.removeItem(href);
			element.attr('style','background:url(../images/bg-black.png); display: inline; opacity: 0;')
			element.attr('class','mosaic-overlay');
		}else{
			element.attr('style','background:url(../images/bg-red.png); display: inline; opacity: 0;')
			element.attr('class','mosaic-overlay selected');
			objects.push(href);
		}
	}
}

function eventsWithoutTab(){
	$('.eraseable').click(function(event){
		event.preventDefault();
		$(this).attr('value','');
	});
	$('.select').change(function(event){
		event.preventDefault();
		option = $("select option:selected").val();
	});
	$('#upload').click(function(event){
		event.preventDefault();
		$('input:file').click(); 
	});
	$('#causas,input[type=file]').fileUpload({
		url: 'expose',
		type: 'POST',
		xhr: function() {
			$.get('expose',$('#causas').serialize(),function(data){ });
			$('#overlay').css({ height: $('#upload').height() });
			$('#overlay').show();
			myXhr = $.ajaxSettings.xhr();
			if(myXhr.upload) myXhr.upload.addEventListener('progress',progressHandlingFunction,false);
			return myXhr;
		},
		success: function(data){
			token = data;
			$('#overlay').find('p').html('Upload concluído.');
		}
	});
	$('#causas').submit(function(event){
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
			$('#Espaco').dialog('close');
		});
	});
	$('#create').click(function(event){
		event.preventDefault();
		$('#causas').submit();
	});
	$('#overlay').hide();
	$('#spreadpost').click(function(event){
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
				loadNewGrid(data);
			}
		});
	});
}

function eventsAfterTab(data){
	$('.eraseable').click(function(event){
		event.preventDefault();
		$(this).attr('value','');
	});
	$('.select').change(function(event){
		event.preventDefault();
		option = $("select option:selected").val();
	});
	currentYear = currentTime.getFullYear()-13
	$('#upload').click(function(event){
		event.preventDefault();
		$('input:file').click(); 
	});
	$('#espalhe,input[type=file]').fileUpload({
		url: 'expose',
		type: 'POST',
		beforeSend:function(){
			if(option == 0){
				alert('Selecione uma das categorias listadas.');
				abort();
			}
		},
		xhr: function(){
			$.get('expose',$('#conteudo').serialize()+'&category='+option,function(data){ });
			$('#overlay').css({ height: $('#upload').height() });
			$('#overlay').show();
			myXhr = $.ajaxSettings.xhr();
			if(myXhr.upload) myXhr.upload.addEventListener('progress',progressHandlingFunction,false);
			return myXhr;
		},
		success: function(data){
			token = data;
			$('#overlay').find('p').html('Upload concluído.');
		} 
	});
	$('#content,#musics').click(function(event){ loadNewGrid(event,'content'); });
	$('#datepicker').datepicker({
		defaultDate:'-13y',
		dateFormat:'d MM, yy',
		changeMonth:true,
		changeYear:true,
		yearRange:"1915:"+currentYear,
		showOn: "button",
		buttonImage: "images/calendar.png",
		buttonImageOnly: true,
		onClose: function(){ this.focus(); }
	}).keydown(sendNewField);
	$('#id_username,#id_email,#id_last_name,#id_first_name').click(function(event){
		event.preventDefault();
		$(this).attr('value','');
	});
	$('#id_username,#id_email,#id_last_name,#id_first_name,#datepicker').keyup(sendNewField);
	$('#datepicker').datepicker('option',$.datepicker.regional['pt-BR'])
	$('#password').click(function(event){
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
							alert(data);
						}
					});
				});
			}
		});
	});
	$('#message').click(function(event){
		if($('#message').text() == 'Você não possui nenhum movimento. Gostaria de criar um?' ||
		   $('#message').text().indexOf('Movimentos em aberto') != -1){
			showContext(event,'movement?action=grid',loadNewGrid);	
		}else{
			showContext(event,'schedule?action=grid',loadNewGrid);
		}
		$('#message').empty();
		hideMenus(event);
		$('#Espaco').dialog('close');
		selection = true;
	});
	$('#overlay').hide();
}
/*

function showExploreResults(action,message){
	$('#Espaco').empty();
	$.post(action,message,function(data){
		$('#Grade').empty();
		$('#Grade').html(data);
		$('.mosaic-block').mosaic();
		$('a.mosaic-overlay').click(showToolbar);
	});
}*/

function showDataContext(title,data){
	$('#Espaco').empty().dialog('destroy');
	$('#Espaco').html(data);
	eventsWithoutTab();
	$("#Abas").tabs({ ajaxOptions: { success: function(data){ eventsAfterTab(data); } } });
	$( ".tabs-bottom .ui-tabs-nav, .tabs-bottom .ui-tabs-nav > *" )
	.removeClass( "ui-corner-all ui-corner-top" )
	.addClass( "ui-corner-bottom" );
	$('#Espaco').dialog({
		title:title,height:'auto',width:'auto',modal:true,
		position:'center',resizable:false,draggable:false
	});
}

function showConfigContext(data){
	$('#Espaco').empty().dialog('destroy');
	$('#Espaco').html(data);
	$('#Abas').css({'height':$('#Canvas').height()-70});
	$('#Abas').tabs({ ajaxOptions: { success: function(data){ eventsAfterTab(data); } } });
	$( ".tabs-bottom .ui-tabs-nav, .tabs-bottom .ui-tabs-nav > *" )
	.removeClass( "ui-corner-all ui-corner-top" )
	.addClass( "ui-corner-bottom" );
	$('#Espaco').dialog({
		title:'Configurações do Efforia',height:$('#Canvas').height()-5,width:$('#Canvas').width()-5,
		position:['right','bottom'],modal:false,resizable:false,draggable:false
	});
}

function showFilterContext(data){
	$('#Menu').html(data);
	$('#Espaco').dialog('close');
	$('#Espaco').empty().dialog('destroy');
}

function loadNewGrid(data){
	$('#Espaco').dialog('close');
	$('#Espaco').empty().dialog('destroy');
	hideMenus();
	$('#Grade').empty();
	$('#Grade').html(data);
	$('.mosaic-block').mosaic();
	$('.mosaic-block').css({'height':300});
	$('a.action1').click(function(event){ showMenus(event); });
	$('a.action2').click(function(event){ 
		event.preventDefault(); 
		alert('Action 2');
	});
	$('a.mosaic-overlay').click(function(event){ clickContent(event,$(this)); });
}

function showContext(event,context,callback){
	event.preventDefault();
	$.ajax({
		url:context,
		beforeSend: animateProgress(),
		success: function(data){ callback(data); }
	});
}

function getSearchFilters(action,data){
	query = action+'?'+data;
	filters = '&filters='
	$('.checkbox').each(function(){
		if($(this).css('background-position') == '0px -50px')
			filters += $(this).parent().text().toLowerCase().replace(/^\s+|\s+$/g,'')+',';
	});
	url = query+filters;
	return url;
}

$('a.mosaic-overlay').click(function(event){ clickContent(event,$(this)); });
$('a.action1').click(function(event){ showMenus(event); });

$('#Menu').hide();
$('a[name=play]').click(function(event){showContext(event,'collection',function(data){showDataContext('O que você quer tocar hoje?',data);});});
$('a[name=create]').click(function(event){showContext(event,'causes',function(data){showDataContext('O que você pretende criar hoje?',data);});});
$('a[name=spread]').click(function(event){showContext(event,'spread',function(data){showDataContext('O que você quer espalhar hoje?',data);});});
$('a[href=favorites]').click(function(event){showContext(event,'favorites',loadNewGrid);});
$('a[href=config]').click(function(event){showContext(event,'config',showConfigContext);});
$('a[href=filter]').click(function(event){
	event.preventDefault();
	if(!openedMenu){
		$('#Menu').slideDown("slow");
		openedMenu = true;	
	}else{
		$('#Menu').slideUp("slow");
		$('.lupa').focus();
		openedMenu = false;
	}
	//showContext(event,this.href,showFilterContext);
});
$('#explore').submit(function(event){ showContext(event,getSearchFilters(this.action,$(this).serialize()),loadNewGrid);});

$(':file').change(function(){
    var file = this.files[0];
    name = file.name;
    size = file.size;
    type = file.type;
});

});
