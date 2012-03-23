var context_menu = false;
var opened = {
	'explore':false,
	'spread':false,
	'store':false,
	'play':false
};

$(document).ready(function(){

var w = window.innerWidth*0.6775;
var h = window.innerHeight;

function anyContextOpened(context,divclass){
	anyOpened = false;
	if(opened[context]) {
		anyOpened = true;
		$('.black').hide();
		opened[context] = false;
		context_menu = false;
	}
	return anyOpened;
}

function openAnotherContext(context,divclass){
	opened[context] = true;
	$('.black').hide();
	$('#horizontal').empty();
	$('#horizontal').animate({height:5},500);
	$(divclass).show();
}

function showToolbar(event){
	event.preventDefault();
	$('#horizontal').empty();
    $('#conteudoEsquerda:hidden').show('fade');
    $('#conteudoDireita:hidden').show('fade');
    $('#conteudoCanvas:hidden').show('fade');
    $('#ferramentas:hidden').show('fade');
	$('#horizontal').animate({height:h*0.35},500);
    $('#ferramentas').animate({left:'35%',top:'32.5%',width:w*0.45},500);
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
		alert(message)
		$('#horizontal').empty();
		$('#horizontal').animate({height:h*0.40},500);
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

function showSpreadContext(event){
	event.preventDefault();
	if(context_menu){
		$.ajax({
			url:this.href,
			success:function(data){
				$('#horizontal').empty();
				$('#horizontal').animate({height:h*0.15},500);
        		$('#ferramentas').animate({left:'37.5%',top:'37.5%',width:w*0.4},500);
				$('#horizontal').html('<h3>O que você quer espalhar hoje?</h3>'+data);
				$('input[name=content]').attr('style','width:100%; height:'+h*0.025+'px;');
				$('#espalhe').submit(function(event){
					event.preventDefault();
					showSpreadResults('spread',$("#espalhe").serialize());
				});
			}
		});
	}
}

function showPlayContext(event){
	event.preventDefault();
	if(context_menu){
		$.ajax({
			url:this.href,
			success:function(data){
				$('#horizontal').empty();
				$('#horizontal').animate({height:h*0.15},500);
	    		$('#ferramentas').animate({left:'37.5%',top:'37.5%',width:w*0.4},500);
	    		$('#horizontal').html(data);
	    		$('#content,#musics').prepend("25");
				$('#content,#musics').click(loadNewGrid);
			}
		});
	}
	/*$(".slider").mb_vSlider({
		easing:"easeOutExpo",
		slideTimer:1000,
		height:h*0.135,
		width:w*0.39
	});*/
}

function showExploreContext(event){
	event.preventDefault();
	//loadNewGrid(event,people);
	if(context_menu){
		$.ajax({
			url:this.href,
			success:function(data){
				$('#horizontal').empty();
				$('#horizontal').animate({height:h*0.15},500);
        		$('#ferramentas').animate({left:'37.5%',top:'37.5%',width:w*0.4},500);
				$('#horizontal').html('<h3>O que você quer explorar hoje?</h3>'+data);
				$('input[name=name]').attr('style','width:100%; height:'+h*0.025+'px;');
				$('form').submit(function(event){
					event.preventDefault();
					showExploreResults('search',$('form').serialize());
				});
			}
		});
	}
}

function loadNewGrid(event){
	event.preventDefault();
	$('#horizontal').empty();
	$('#conteudoEsquerda:visible').hide('fade');
	$('#conteudoDireita:visible').hide('fade');
	$('#conteudoCanvas:visible').hide('fade');
	$('#ferramentas:visible').hide('fade');
	$.ajax({
		url:this.href,
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
	if(!context_menu){
		opened[context] = true;
		context_menu = true;
		$('#acima,#abaixo').animate({height:$(divclass).height()},500);
		$('#ferramentas').animate({top:"42.5%"},500);
		$(divclass).show();
	} else if(context_menu) { 
		if(anyContextOpened(context,divclass)){
			$('#acima,#abaixo').animate({height:5},500);
			$('#ferramentas').animate({top:"45%"},500);
		} else {
			openAnotherContext(context,divclass);
			$('#acima,#abaixo').animate({height:$(divclass).height()},500);
			$('#ferramentas').animate({top:"42.5%"},500);
		}
		
	}
}

$('.black').hide();
$('a.mosaic-overlay').click(showToolbar);

$('#expose,#spread,#causes').click(showSpreadContext);
$('#play').click(showPlayContext);
$('#search').click(showExploreContext);

$('a[name=play]').click(function(event){showContext(event,'play','.play');});
$('a[name=store]').click(function(event){showContext(event,'store','.store');});
$('a[name=spread]').click(function(event){showContext(event,'spread','.spread');});
$('a[name=explore]').click(function(event){showContext(event,'explore','.explore');});

});
