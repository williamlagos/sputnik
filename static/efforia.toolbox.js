$(document).ready(function(){

var w = window.innerWidth;
var h = window.innerHeight;
var selection = false;

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
    /*$('#Esquerda:hidden').show('fade');
    $('#Canvas:hidden').show('fade');
    $('#Navegacao:hidden').show('fade');
	var token = $(this).attr('href');
	$('#Espaco').tubeplayer({
		width: "100%",height: "100%",
		showControls:false, modestbranding:false, showinfo:false,
		iframed:true, allowFullScreen:"true", 
		initialVideo: token, 
	});
	$('#Espaco').dialog({
		title:'O que você quer tocar hoje?',
		height:'auto',width:'auto',modal:true
	});*/
}

function clickContent(event,element){
	event.preventDefault();
	if(selection == true){
		element.attr('style','background:url(../images/bg-red.png); display: inline; opacity: 0;')
		/*alert(element.html());
		alert(element.children().html());
		alert(element.children().children().html());*/
	}
}

function createTabs(){
	$( "#tabs" ).tabs({
		ajaxOptions: {
			success: function(data){
				$('#upload').click(function(event){ $('input:file').click(); });
				$('#content,#musics').click(function(event){ loadNewGrid(event,'content'); });
				$('#message').click(function(event){
					$('#message').empty();
					$('#message').html('Selecione os programas listados na sua coleção para criar uma programação.');
					$('#message').click(function(event){
						$('#Espaco').dialog('close'); 
						hideMenus(event);
						selection = true;
					});
				});
				$('#espalhe').submit(function(event){
					event.preventDefault();
					showSpreadResults('spread',$("#espalhe").serialize());
				});
				/*$('form').submit(function(event){
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
	$('#Espaco').dialog({
		title:'Configurações do Efforia',
		height:$('#Canvas').height()-5,width:$('#Canvas').width()-5,
		position:['right','bottom'],modal:false
	});
}

function loadNewGrid(data){
	$('#Esquerda:visible').hide('fade');
	$('#Canvas:visible').hide('fade');
	$('#Navegacao:visible').hide('fade');
	$('#Grade').empty();
	$('#Grade').html(data);
	$('.mosaic-block').mosaic();
	$('a.mosaic-overlay').click(showToolbar);
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
