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

function animateToolbox(context){
	$('#ferramentas').animate({
		left:'30%',
		width:w*0.4
	},500);
	height = $(context).outerHeight(true)/h;
	topT = ((100-(height*100))/2)-15;
	$('#ferramentas').animate({top:topT+'%'},500);
}

function animateProgress(){
	$('#horizontal').empty();
	//animateToolbox(motion[0],motion[1]);
	$('#horizontal').html("<p></p><img src='images/progress.gif'/><p>Carregando...</p>");	
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
	$('#horizontal').empty();
	//animateToolbox(context);
	$(divclass).show();
}

function showToolbar(event){
	event.preventDefault();
	$('#horizontal').empty();
    $('#conteudoEsquerda:hidden').show('fade');
    $('#conteudoDireita:hidden').show('fade');
    $('#conteudoCanvas:hidden').show('fade');
    $('#ferramentas:hidden').show('fade');
    animateToolbox('#ferramentas');
	var token = $(this).attr('href');
	$('#horizontal').tubeplayer({
		width: "100%",height: "100%",
		showControls:false, modestbranding:false, showinfo:false,
		iframed:true, allowFullScreen:"true", 
		initialVideo: token, 
	});
}

function showSpreadResults(action,message){
	$('#horizontal').empty();
	$.post(action,message,function(data){
		$('#horizontal').empty();
		//animateToolbox();
		$('#horizontal').html(data);
		$(".slider").mb_vSlider({
			easing:"easeOutExpo",
			slideTimer:1000,
			height:h*0.36,
			width:w*0.38
		});
	});
}

function showExploreResults(action,message){
	$('#horizontal').empty();
	$.post(action,message,function(data){
		$('#conteudoGrid').empty();
		$('#conteudoGrid').html(data);
		$('.mosaic-block').mosaic();
		$('a.mosaic-overlay').click(showToolbar);
	});
}

function showSpreadContext(data,context){
	$('#horizontal').empty();
	ctx = spreadctx[context];
	$('#horizontal').html(data);
	//$('input[name=content]').attr('style','width:100%; height:'+h*0.025+'px;');
	animateToolbox(ctx);
	$('#upload').click(function(event){
		$('input:file').click();
	});
	$('#espalhe').submit(function(event){
		event.preventDefault();
		showSpreadResults('spread',$("#espalhe").serialize());
	});
}

function showPlayContext(event){
	event.preventDefault();
	if(context_menu){
		$.ajax({
			url:this.href,
			beforeSend: animateProgress(),
			success:function(data){
				$('#horizontal').empty();
				animateToolbox(40,15);
	    		$('#horizontal').html(data);
	    		$('#content,#musics').prepend("25");
				$('#content,#musics').click(function(event){ loadNewGrid(event,'content'); });
			}
		});
	}
}

function showExploreContext(data,context){
	$('#horizontal').empty();
	animateToolbox(40,15);
	$('#horizontal').html('<h3>O que você quer explorar hoje?</h3>'+data);
	$('input[name=name]').attr('style','width:100%; height:'+h*0.025+'px;');
	$('form').submit(function(event){
		event.preventDefault();
		showExploreResults('search',$('form').serialize());
	});
}

function loadNewGrid(event,id){
	event.preventDefault();
	$('#horizontal').empty();
	$('#conteudoEsquerda:visible').hide('fade');
	$('#conteudoDireita:visible').hide('fade');
	$('#conteudoCanvas:visible').hide('fade');
	$('#ferramentas:visible').hide('fade');
	$.ajax({
		url:id,
		beforeSend: animateProgress(),
		success:function(data){
			$('#conteudoGrid').empty();
			$('#conteudoGrid').html(data);
			$('.mosaic-block').mosaic();
			$('a.mosaic-overlay').click(showToolbar);
		}
	});
}

function showContext(event,context,divclass){
	event.preventDefault();
	if(!context_menu) {
		opened[context] = true;
		context_menu = true;
		$('#acima,#abaixo').animate({height:$(divclass).height()},500);
		$('#ferramentas').animate({top:"42.5%"},500);
		$(divclass).show();
	} else if(context_menu) {
		$('.black').hide();
		if(!anyContextOpened(context,divclass)) {
			$('#acima,#abaixo').animate({height:5},500);
			$('#ferramentas').animate({top:"45%"},500);
			$('#acima,#abaixo').animate({height:$(divclass).height()},500);
			$('#ferramentas').animate({top:"42.5%"},500);
			openAnotherContext(context,divclass);
		} else {
			$('#horizontal').empty();
			animateToolbox(30,0.5);
			$('#acima,#abaixo').animate({height:5},500);
			context_menu = false;
		}
	}
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

$('a[name=play]').click(function(event){showContext(event,'play','.play');});
$('a[name=store]').click(function(event){showContext(event,'store','.store');});
$('a[name=spread]').click(function(event){showContext(event,'spread','.spread');});
$('a[name=explore]').click(function(event){showContext(event,'explore','.explore');});

});
