document.documentElement.style.overflowX = 'hidden';	 // horizontal scrollbar will be hidden
document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){

var context_menu = false;
var view = true;
var known = false;
var favor = true;
var margin = 200;
var w = window.innerWidth*0.6775;
var h = window.innerHeight;
document.getElementById('efforia').width = w;
document.getElementById('efforia').height = h;

$('.fade').mosaic();
/*$('a').click(function(event){ 
	event.preventDefault();
	$("#ferramentas").animate({left:"35%",width:"30%",right:"35%"},3000);
	$("#ferramentas").animate({top:"35%",height:"30%",bottom:"35%"},3000);
	$("#espaco").animate({height:"100%"},3000);
	$("#espaco").tubeplayer({
		width: "100%", // the width of the player
		height: "100%", // the height of the player
		showControls: 0,
		modestbranding: false,
		showinfo: false,
		allowFullScreen: "true", // true by default, allow user to go full screen
		initialVideo: this.href, // the video that is loaded into the player
		preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
		onPlay: function(id){}, // after the play method is called
		onPause: function(){}, // after the pause method is called
		onStop: function(){}, // after the player is stopped
		onSeek: function(time){}, // after the video has been seeked to a defined point
		onMute: function(){}, // after the player is muted
		onUnMute: function(){} // after the player is unmuted
	});
 
	//$("#espaco").dialog({height:'auto',width:'auto',modal:true}); 
	/*$.get("play", { name: "John", time: "2pm" }, function(data) {
		alert(data);
  		//$('#espaco').html(data);
	});
});*/

$('a[name=spread]').click(function(event){
	event.preventDefault();
	if(!context_menu){
		context_menu = true;
		$('#acima').animate({height:h*0.05},500);
		$('#abaixo').animate({height:h*0.05},500);
		$('#ferramentas').animate({top:"40%"},500);
		$('#acima').append("<a class='ui-button botao' style='width:45%;' href='spread'>Postagens</a>");
		$('#acima').append("<a class='ui-button botao' style='width:45%;' href='causes'>Causas</a>");
		$('#abaixo').append("<a class='ui-button botao' style='width:90%;' href='expose'>Conteúdo</a>");
	} else if(context_menu) { 
		context_menu = false;
		$('#acima').empty();
		$('#abaixo').empty();
		$('#acima').animate({height:5},500);
		$('#abaixo').animate({height:5},500);
		$('#ferramentas').animate({top:"45%"},500);
	}
});

$('a[name=play]').click(function(event){
	event.preventDefault();
	if(!context_menu){
		context_menu = true;
		$('#acima').animate({height:h*0.05},500);
		$('#abaixo').animate({height:h*0.05},500);
		$('#ferramentas').animate({top:"40%"},500);
		$('#acima').append("<a class='ui-button' style='width:45%;' href='apps'>Aplicativos</a>");
		$('#acima').append("<a class='ui-button' style='width:45%;' href='games'>Jogos</a>");
		$('#abaixo').append("<a class='ui-button' style='width:90%;' href='my'>Minha Coleção</a>");
	} else if(context_menu) { 
		context_menu = false;
		$('#acima').empty();
		$('#abaixo').empty();
		$('#acima').animate({height:5},500);
		$('#abaixo').animate({height:5},500);
		$('#ferramentas').animate({top:"45%"},500);
	}
});

$('a[name=explore]').click(function(event){
	event.preventDefault();
	if(!context_menu){
		context_menu = true;
		$('#acima').animate({height:h*0.05},500);
		$('#abaixo').animate({height:h*0.05},500);
		$('#ferramentas').animate({top:"40%"},500);
		$('#acima').append("<a class='ui-button' style='width:45%;' href='search'>Pessoas</a>");
		$('#acima').append("<a class='ui-button' style='width:45%;' href='search'>Locais</a>");
		$('#abaixo').append("<a class='ui-button' style='width:90%;' href='search'>Eventos</a>");
	} else if(context_menu) { 
		context_menu = false;
		$('#acima').empty();
		$('#abaixo').empty();
		$('#acima').animate({height:5},500);
		$('#abaixo').animate({height:5},500);
		$('#ferramentas').animate({top:"45%"},500);
	}
});

$('.botao').click(function(event){
	event.preventDefault();
	if(context_menu){
		$.ajax({
			url:this.href,
			success:function(data){
				$('#horizontal').html(data);
			}
		});
	}
});

$('#conteudoCentral').masonry({itemSelector:'.mosaic-block'});
$('#dialogo').dialog({height:'auto',width:'auto',modal:true});
$('#conhecidos').hide();
$('#radio').buttonsetv();
$('#radio').change(function(){
	if(!favor && known){
		$('#conhecidos:visible').hide('slide');
		$('#favoritos:hidden').show('slide');
	} else {
		$('#favoritos:visible').hide('slide');
		$('#conhecidos:hidden').show('slide');
	}
	known = !known;
	favor = !favor;
});
$( "input:submit, a, button", "#botoes" ).button();

$(".mosaic-block").bind("click",function(){
	view = false;
	$('#conteudoEsquerda:hidden').show('fade');
    	$('#conteudoDireita:hidden').show('fade');
   	$('#conteudoCanvas:hidden').show('fade');
	$('#ferramentas:hidden').show('fade');
});


var canvas = new fabric.Canvas('efforia');
var radians = 180/Math.PI; 
var cX = canvas.width/2;
var cY = canvas.height/2;
var last = 0;
var velocity = 0.001;
var acceleration = 0.1;
var holding = clicked = false;

if (!window.requestAnimationFrame) {
	window.requestAnimationFrame = (function() 
	{
		return window.webkitRequestAnimationFrame 	|| 	
			   window.mozRequestAnimationFrame 		|| 	
		       window.oRequestAnimationFrame 		|| 	
			   window.msRequestAnimationFrame	 	||
			   function(callback,element)
			   { window.setTimeout(callback,1000/60); };
  	})();
}

drawElements();
function drawElements() 
{
	fabric.loadSVGFromURL('interface.svg', function(objects,options) 
	{
		helix = new fabric.PathGroup(objects);
		scaleFactor = h/900;
		helix.scale(scaleFactor);
		canvas.add(helix);
		canvas.centerObjectH(helix).centerObjectV(helix);
		canvas.selection = false;
		canvas.forEachObject(function(obj) {
			obj.hasBorders = obj.hasControls = false;
			obj.lockScalingX = obj.lockScalingY = true;
			obj.lockMovementX = obj.lockMovementY = true;	
		});
		listenEvents();
	});
}

function listenEvents()
{
	canvas.observe('mouse:down',function(e) { holding = true; clicked = true; });
	canvas.observe('mouse:up'  ,function(e) { 
		holding = false;
		view = true; 
		if(!clicked){
			$('.mosaic-block').animate({"bottom":"+="+margin+"px"},{
				duration: 1000,
				step: function( now, fx ){
					$( ".block:gt(0)" ).css( "left", now );
				}
			}); 
		}
	});
	canvas.observe('mouse:move',function(e) 
	{
		if (holding) {
			clicked = false;
			pos = canvas.getPointer(e.memo.e);
			x = (cX)-pos.x; y = (cY)-pos.y;
			if (velocity < 0) velocity = -velocity;
			if (velocity >= last) {
				last = velocity;
				velocity = -(Math.atan(y/x)/radians);
				velocity -= acceleration;
			} else if (velocity < last) {
				last = velocity;
				velocity = Math.atan(y/x)/radians;
				velocity += acceleration;
			}
			if (x <= cX && y <= cY)	velocity = -velocity;	
			margin = -margin;
			helix.theta += velocity;
		}
	});
	date = new Date();
	time = date.getTime();  
	animateElements(time);	
}

function animateElements(lastTime)
{
	date = new Date();
    	time = date.getTime();
    	timeDiff = time - lastTime;
   	if (!holding && !clicked) {
    		angularFriction = 0.1;
    		angularVelocity = velocity*timeDiff*(1-angularFriction)/1000;
    		velocity -= angularVelocity;
        	helix.theta += velocity;
    	} else if (!holding && clicked && view) {
    		$('#conteudoEsquerda:visible').hide('fade');
		$('#conteudoDireita:visible').hide('fade');
		$('#conteudoCanvas:visible').hide('fade');
		$('#ferramentas:visible').hide('fade');
    	}
    	helix.angle = helix.theta*radians;
	canvas.renderAll();
	window.requestAnimationFrame(function() { animateElements(time); });
}

});
