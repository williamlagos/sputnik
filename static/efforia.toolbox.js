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

function progressHandlingFunction(e){
    if(e.lengthComputable){
        $('progress').attr({value:e.loaded,max:e.total});
    }
}

function animateProgress(){
	$('#Espaco').html("<p></p><img src='images/progress.gif'/><p>Carregando...</p>");
	$('#Progresso').show();	
}

function hideMenus(event){
	event.preventDefault();
    $('#Esquerda:visible').hide('fade');
    $('#Canvas:visible').hide('fade');
    $('#Navegacao:visible').hide('fade');
}

function showMenus(event){
	event.preventDefault();
   	$('#Esquerda:hidden').show('fade');
    $('#Canvas:hidden').show('fade');
    $('#Navegacao:hidden').show('fade');
}

function clickContent(event,element){
	event.preventDefault();
	if(selection == true){
		token = element.attr('href');
		if(element.attr('class') == 'mosaic-overlay action'){
			if(objects.length < 1) return;
			element.children().html('<form method="post" action="/schedule" style="text-align:center;">Nome para a sua programação:<input name="title" style="width:100%;"></input><div id="botoes"><input name="create" class="ui-button ui-widget ui-state-default ui-corner-all" type="submit" value="Criar nova programação"></div></form>');
			$('input[name=create]').click(function(event){
				event.preventDefault();
				title = $('input[name=title]').val()
				if(title == '') return;
				objs = objects.join();
				$.post(token,{'objects':objs,'title':title},function(data){
					showMenus(event);
					$('#Espaco').html(data);
					$('#Espaco').dialog('open');
				});
			});
			element.attr('class','mosaic-overlay title');
		}else if(element.attr('class') == 'mosaic-overlay title'){
			return;
		}else if(element.attr('class') == 'mosaic-overlay selected'){
			objects.removeItem(token);
			element.attr('style','background:url(../images/bg-black.png); display: inline; opacity: 0;')
			element.attr('class','mosaic-overlay');
		}else{
			element.attr('style','background:url(../images/bg-red.png); display: inline; opacity: 0;')
			element.attr('class','mosaic-overlay selected');
			objects.push(token);
		}
	}
}

function createTabs(){
	$( "#Espaco" ).tabs({
		ajaxOptions: {
			success: function(data){
				currentYear = currentTime.getFullYear()-13
				$('#upload').click(function(event){ $('input:file').click(); });
				$('#content,#musics').click(function(event){ loadNewGrid(event,'content'); });
				$('#datepicker').datepicker({
					defaultDate:'-13y',
					dateFormat:'d MM, yy',
					changeMonth:true,
					changeYear:true,
					yearRange:"1915:"+currentYear
				});
				$('#id_username,#id_email,#id_last_name,#id_first_name').click(function(event){
					event.preventDefault();
					$(this).attr('value','');
				});
				$('#datepicker').datepicker('option',$.datepicker.regional['pt-BR'])
				$('#password').click(function(event){
					$.ajax({
						url:'password',
						success:function(data){
							$('#passwordchange').html(data);
							$('#password').attr('value','Alterar senha');
						}
					});
				});
				$('#message').click(function(event){
					$('#message').empty();
					$('#message').html('Selecione os programas listados na sua coleção para criar uma programação.');
					showContext(event,'schedule?action=grid',loadNewGrid);
					hideMenus(event);
					$('#Espaco').dialog('close'); 
					selection = true;
				});
				/*$('#espalhe').submit(function(event){
					event.preventDefault();
					showSpreadResults('spread',$("#espalhe").serialize());
				});
				$('form').submit(function(event){
					event.preventDefault();
					showExploreResults('search',$('form').serialize());
				});*/
			}
		}
	});
	$( ".tabs-bottom .ui-tabs-nav, .tabs-bottom .ui-tabs-nav > *" )
	.removeClass( "ui-corner-all ui-corner-top" )
	.addClass( "ui-corner-bottom" );
}

function showSpreadResults(action,message){
	$('#Espaco').empty();
	$.post(action,message,function(data){
		$('#Espaco').empty();
		$('#Espaco').html(data);
		$(".slider").mb_vSlider({
			easing:"easeOutExpo",
			slideTimer:1000,
			height:h*0.36,
			width:w*0.38
		});
	});
}

function showExploreResults(action,message){
	$('#Espaco').empty();
	$.post(action,message,function(data){
		$('#Grade').empty();
		$('#Grade').html(data);
		$('.mosaic-block').mosaic();
		$('a.mosaic-overlay').click(showToolbar);
	});
}

function showSpreadContext(data){
	$('#Espaco').html(data);
	createTabs();
	$('#Espaco').dialog({
		title:'O que você quer espalhar hoje?',
		height:'auto',width:'auto',modal:true,position:'center'
	});
}

function showPlayContext(data){
	$('#Espaco').html(data);
	createTabs();
	$('#Espaco').dialog({
		title:'O que você quer tocar hoje?',
		height:'auto',width:'auto',modal:true,position:'center'
	});
}

function showExploreContext(data,context){
	$('#Espaco').html(data);
	createTabs();
	$('#Espaco').dialog({
		title:'O que você quer explorar hoje?',
		height:'auto',width:'auto',modal:true,position:'center'
	});
}

function showCreateContext(data){
	$('#Espaco').html(data);
	createTabs();
	$('#Espaco').dialog({
		title:'O que você pretende criar hoje?',
		height:'auto',width:'auto',modal:true,position:'center'
	});
}

function showConfigContext(data){
	$('#Espaco').html(data);
	createTabs();
	$('#Espaco').dialog({
		title:'Configurações do Efforia',
		height:$('#Canvas').height()-5,width:$('#Canvas').width()-5,
		position:['right','bottom'],modal:false,
		resizable:false,draggable:false
	});
}

function loadNewGrid(data){
	$('#Grade').empty();
	$('#Grade').html(data);
	$('.mosaic-block').mosaic();
	$('a.mosaic-overlay').click(function(event){ clickContent(event,$(this)); });
}

function showContext(event,context,callback){
	event.preventDefault();
	$.ajax({
		url:context,
		beforeSend: animateProgress(),
		success: function(data){
			$('#Progresso').hide();
			callback(data); 
		}
	});
}

$('.black').hide();
$('a.mosaic-overlay').click(function(event){ clickContent(event,$(this)); });

$('a[name=play]').click(function(event){showContext(event,'collection',showPlayContext);});
$('a[name=create]').click(function(event){showContext(event,'causes',showCreateContext);});
$('a[name=spread]').click(function(event){showContext(event,'spread',showSpreadContext);});
$('a[href=favorites]').click(function(event){showContext(event,'favorites',loadNewGrid);});
$('a[href=config]').click(function(event){showContext(event,'config',showConfigContext);});

});
