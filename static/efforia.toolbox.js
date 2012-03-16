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
	$(divclass).show();
}

$('.black').hide();
$('.reference').hide();
$('#expose,#spread').click(function(event){
	event.preventDefault();
	if(context_menu){
		$.ajax({
			url:this.href,
			success:function(data){
				$('#horizontal').animate({height:h*0.30},500);
				$('#ferramentas').animate({top:'35%',width:w*0.30},500);
				$('textarea')
				$('#horizontal').html(data);
			}
		});
	}
});

$('#play').click(function(event){ 
	event.preventDefault();
	$('#horizontal').animate({height:h*0.30},500);
        $('#ferramentas').animate({top:'35%',width:w*0.30},500);
	$('.reference').show();
	$('#videos,#musics').prepend("30");
});
$('#videos,#musics').click(function(event){
	event.preventDefault();
	$('#conteudoEsquerda:visible').hide('fade');
	$('#conteudoDireita:visible').hide('fade');
	$('#conteudoCanvas:visible').hide('fade');
	$('#ferramentas:visible').hide('fade');
});

$("a.mosaic-overlay").bind("click",function(event){
	event.preventDefault();
        $('#conteudoEsquerda:hidden').show('fade');
        $('#conteudoDireita:hidden').show('fade');
        $('#conteudoCanvas:hidden').show('fade');
        $('#ferramentas:hidden').show('fade');
	$('#horizontal').animate({height:h*0.35},500);
        $('#ferramentas').animate({left:'35%',top:'32.5%',width:w*0.45},500);
	var token = $(this).attr('href');
	$('#horizontal').tubeplayer({
		width: "100%", // the width of the player
		height: "100%", // the height of the player
		showControls: 0,
		modestbranding: false,
		showinfo: false,
		allowFullScreen: "true", // true by default, allow user to go full screen
		initialVideo: token, // the video that is loaded into the player
		preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
		onPlay: function(id){}, // after the play method is called
		onPause: function(){}, // after the pause method is called
		onStop: function(){}, // after the player is stopped
		onSeek: function(time){}, // after the video has been seeked to a defined point
		onMute: function(){}, // after the player is muted
		onUnMute: function(){} // after the player is unmuted
	});
});

$('a[name=spread]').click(function(event){
	event.preventDefault();
	if(!context_menu){
		opened['spread'] = true;
		context_menu = true;
		$('#acima,#abaixo').animate({height:h*0.05},500);
		$('#ferramentas').animate({top:"40%"},500);
		$('.spread').show();
	} else if(context_menu) { 
		if(anyContextOpened('spread','.spread')){
			$('#acima,#abaixo').animate({height:5},500);
			$('#ferramentas').animate({top:"45%"},500);
		} else {
			openAnotherContext('spread','.spread');
			$('#acima,#abaixo').animate({height:h*0.05},500);
			$('#ferramentas').animate({top:"40%"},500);
		}
		
	}
});

$('a[name=play]').click(function(event){
	event.preventDefault();
	if(!context_menu){
		opened['play'] = true;
		context_menu = true;
		$('#acima,#abaixo').animate({height:h*0.05},500);
		$('#ferramentas').animate({top:"40%"},500);
		$('.play').show();
	} else if(context_menu) { 
		if(anyContextOpened('play','.play')){
			$('#acima,#abaixo').animate({height:5},500);
			$('#ferramentas').animate({top:"45%"},500);
		} else {
			openAnotherContext('play','.play');
			$('#acima,#abaixo').animate({height:h*0.05},500);
			$('#ferramentas').animate({top:"40%"},500);
		}
	}
});

$('a[name=explore]').click(function(event){
	event.preventDefault();
	if(!context_menu){
		opened['explore'] = true;
		context_menu = true;
		$('#acima,#abaixo').animate({height:h*0.05},500);
		$('#ferramentas').animate({top:"40%"},500);
		$('.explore').show();
	} else if(context_menu) { 
		if(anyContextOpened('explore','.explore')){
			$('#acima,#abaixo').animate({height:5},500);
			$('#ferramentas').animate({top:"45%"},500);
		} else {
			openAnotherContext('explore','.explore');
			$('#acima,#abaixo').animate({height:h*0.05},500);
			$('#ferramentas').animate({top:"40%"},500);
		}
	}
});

});
