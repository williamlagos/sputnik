var context_menu = false;
var opened = {
	'explore':false,
	'spread':false,
	'store':false,
	'play':false
};

var motion = [30,10]

var spreadctx = {
	'expose':'#conteudo',
	'causes':'#causas',
	'spread':'#espalhe',
};

$(document).ready(function(){

var w = window.innerWidth;
var h = window.innerHeight;

function progressHandlingFunction(e){
    if(e.lengthComputable){
        $('progress').attr({value:e.loaded,max:e.total});
    }
}

/*function animateToolbox(context){
	$('#Navegacao').animate({
		left:'30%',
		width:w*0.4
	},500);
	height = $(context).outerHeight(true)/h;
	topT = ((100-(height*100))/2)-15;
	$('#Navegacao').animate({top:topT+'%'},500);
}*/

function animateProgress(){
	$('#Espaco').html("<p></p><img src='images/progress.gif'/><p>Carregando...</p>");
	$('#Progresso').show();	
}

function anyContextOpened(context,divclass){
	sameOpened = false;
	for(var key in opened){
		if(opened[key] == true){
			if(key == context){
				sameOpened = true; 
				break;
			}
			opened[key] = false;
		}
	}
	return sameOpened;
}

function openAnotherContext(context,divclass){
	opened[context] = true;
	$('#Espaco').empty();
	//animateToolbox(context);
	$(divclass).show();
}

function showToolbar(event){
	event.preventDefault();
    $('#Esquerda:hidden').show('fade');
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
	});
}

function showSpreadResults(action,message){
	$('#Espaco').empty();
	$.post(action,message,function(data){
		$('#Espaco').empty();
		//animateToolbox();
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
	$('#Espaco').dialog({
		title:'O que você quer espalhar hoje?',
		height:'auto',width:'auto',modal:true
	});
	$('#upload').click(function(event){
		$('input:file').click();
	});
	$('#espalhe').submit(function(event){
		event.preventDefault();
		showSpreadResults('spread',$("#espalhe").serialize());
	});
}

function showPlayContext(data){
	$('#Espaco').html(data);
	$('#Espaco').dialog({
		title:'O que você quer tocar hoje?',
		height:'auto',width:'auto',modal:true
	});
	$('#content,#musics').prepend("25");
	$('#content,#musics').click(function(event){ loadNewGrid(event,'content'); });
}

function showExploreContext(data,context){
	$('#Espaco').html(data);
	$('#Espaco').dialog({
		title:'O que você quer explorar hoje?',
		height:'auto',width:'auto',modal:true
	});
	$('input[name=name]').attr('style','width:100%; height:'+h*0.025+'px;');
	$('form').submit(function(event){
		event.preventDefault();
		showExploreResults('search',$('form').serialize());
	});
}

function loadNewGrid(event,id){
	event.preventDefault();
	$('#Espaco').empty();
	$('#Esquerda:visible').hide('fade');
	$('#Canvas:visible').hide('fade');
	$('#Navegacao:visible').hide('fade');
	$.ajax({
		url:id,
		beforeSend: animateProgress(),
		success:function(data){
			$('#Grade').empty();
			$('#Grade').html(data);
			$('.mosaic-block').mosaic();
			$('a.mosaic-overlay').click(showToolbar);
		}
	});
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
	/*if(!context_menu) {
		opened[context] = true;
		context_menu = true;
		$('#Abas').animate({height:$(divclass).height()},500);
		$('#Navegacao').animate({top:"42.5%"},500);
		$(divclass).show();
	} else if(context_menu) {
		$('.black').hide();
		if(!anyContextOpened(context,divclass)) {
			$('#Abas').animate({height:5},500);
			$('#Navegacao').animate({top:"45%"},500);
			$('#Abas').animate({height:$(divclass).height()},500);
			$('#Navegacao').animate({top:"42.5%"},500);
			openAnotherContext(context,divclass);
		} else {
			$('#Espaco').empty();
			//animateToolbox(30,0.5);
			$('#Abas').animate({height:5},500);
			context_menu = false;
		}
	}*/
}

$('.black').hide();
$('a.mosaic-overlay').click(showToolbar);

$('#expose,#spread,#causes').click(function(event){
	event.preventDefault();
	var id = this.id;
	if(context_menu){
		$.ajax({
			url:this.href,
			beforeSend: animateProgress(),
			success: function(data){
				showSpreadContext(data,id);
			}
		});
	}		
});

$('#activity,#events').click(function(event){
	event.preventDefault();
	var id = this.id;
	if(id=="activity"){
		$.ajax({
			url: this.href,
			beforeSend: animateProgress(),
			success: function(data){
				showExploreContext(data,id);
			}
		});
	} else if(id=="events") {
		loadNewGrid(event,id);
	}	
});

$('#play').click(showPlayContext);

$('a[name=play]').click(function(event){showContext(event,'collection',showPlayContext);});
$('a[name=store]').click(function(event){showContext(event,'store','.store');});
$('a[name=spread]').click(function(event){showContext(event,'spread',showSpreadContext);});
$('input[name=explore]').click(function(event){showContext(event,'activity',showExploreContext);});

/* Favorites and known buttons
$('#radio').change(function(){
	if(!favor && known){
		$('#conhecidos:visible').hide('slide');
		$('#favoritos:hidden').show('slide');
		favor = true; known = false;
	} else if(favor && !known){
		$('#favoritos:visible').hide('slide');
		$('#conhecidos:hidden').show('slide');
		known = true; favor = false;
	}
});*/

});
