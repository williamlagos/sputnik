document.documentElement.style.overflowX = 'hidden';
document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){
	
var view = true;
var known = false;
var favor = true;
var marginFactor = 8;
var marginTop = 0;
var marginMax = 0;
var w = window.innerWidth*0.85;
var h = window.innerHeight-40;
document.getElementById('efforia').width = w;
document.getElementById('efforia').height = h;

$('a').click(function(){ this.blur(); });
$.get('/',{'feed':'feed'},function(data){ 
	$('#Grade').loadMosaic(data);
	$('#Grade').css({'height':h});
	$('.mosaic-block').mosaic();
	$('.mosaic-block').bind("click",function(){ view = false; });
	if($('.blank').text() != '') marginFactor = 0;
	$('.spreadable,.event').click(function(event){
		event.preventDefault();
		$('#Espaco').html($(this).html()+'<div style="width:50%; float:left;"><a class="ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em 1em;"><span class="ui-icon ui-icon-star"></span></a></div>'+
										 '<div style="width:50%; float:right; text-align:right;"><a class="ui-button ui-widget ui-state-default ui-corner-all" style="padding: .4em 1em;"><span class="ui-icon ui-icon-trash"></span></a></div>');
		$('#Espaco').dialog({
			title:'Objeto',height:'auto',width:'auto',modal:true,
			position:'center',resizable:false,draggable:false
		});
	});
	$('.causable,.playable').click(function(event){
		event.preventDefault();
		$('#Espaco').html('<div id="Player"></div>');
		$('#Espaco').dialog({
			title:'Objeto',height:500,width:800,modal:true,
			position:'center',resizable:false,draggable:false
		});
		$("#Player").tubeplayer({
			width: 770, // the width of the player
			height: 400, // the height of the player
			showinfo: false,
			autoHide: true,
			iframed: true,
			showControls: 0,
			allowFullScreen: "true", // true by default, allow user to go full screen
			initialVideo: $(this).attr('href'), // the video that is loaded into the player
			preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
			onPlay: function(id){}, // after the play method is called
			onPause: function(){}, // after the pause method is called
			onStop: function(){}, // after the player is stopped
			onSeek: function(time){}, // after the video has been seeked to a defined point
			onMute: function(){}, // after the player is muted
			onUnMute: function(){}, // after the player is unmuted
			onPlayerEnded: function(){ $('#Player').empty(); }
		});
	});	
	$('.movement,.schedule').click(function(event){
		event.preventDefault();
		title = $(this).find('h2').html();
		refer = $(this).attr('href');
		$.ajax({
			url:refer,
			data:{'view':refer,'title':title},
			success:function(data){ $('#Grade').loadMosaic(data); }
		});
	});
	$('.loadable').click(function(event){
		event.preventDefault();
		number = $(this).attr('name');
		$.post($(this).attr('href'),{'number':number},function(data){
			$('#Grade').css({marginTop:'0px'});
			$('#Grade').loadMosaic(data);
			if($('.blank').text() != '') marginFactor = 0;
		});
	}); 
});

$("input:submit, button", "#botoes" ).button();

var widthNow = $('html').width();
var heightNow = $('html').height();
var helix = null;
var canvas = new fabric.Canvas('efforia');
var radians = 180/Math.PI; 
var cX = canvas.width/2;
var cY = canvas.height/2;
var last = 0;
var velocity = 0.001;
var acceleration = 0.1;
var holding = clicked = false;

if(widthNow < 1280) $('body').css({'font-size':'0.8em'});

if (!window.requestAnimationFrame) {
	window.requestAnimationFrame = (function() 
	{
		return window.webkitRequestAnimationFrame 	|| 	
			   window.mozRequestAnimationFrame 		|| 	
		       window.oRequestAnimationFrame 		|| 	
			   window.msRequestAnimationFrame	 	||
			   function(callback,element)
			   { 
			   		window.setTimeout(callback,1000/60); 
			   };
  	})();
}

$(window).resize(function() {
	w = window.innerWidth*0.85;
	h = window.innerHeight-40;
	$('#conteudoCanvas,.canvas-container,.lower-canvas,#efforia').css({'height':h,'width':w});
	cX = canvas.width/2;
	cY = canvas.height/2;
	canvas.clear();
	scaleFactor = h/900;
	helix.scale(scaleFactor);
	widthNow = $('body').width();
	if(widthNow < 1280) $('body').css({'font-size':'0.8em'});
	else if(widthNow > 1280) $('body').css({'font-size':'1.0em'});
	canvas.add(helix);
	canvas.centerObjectH(helix).centerObjectV(helix);
});

drawElements();
function drawElements() 
{
	fabric.loadSVGFromURL('interface.svg', function(objects,options) 
	{
		canvas.forEachObject(function(obj) {
			obj.hasBorders = obj.hasControls = false;
			obj.lockScalingX = obj.lockScalingY = true;
			obj.lockMovementX = obj.lockMovementY = true;	
		});
		canvas.selection = false;
		helix = new fabric.PathGroup(objects);
		scaleFactor = h/900;
		helix.scale(scaleFactor);
		widthNow = $('body').width();
		if(widthNow < 1280) $('body').css({'font-size':'0.8em'});
		else if(widthNow > 1280) $('body').css({'font-size':'1.0em'});
		canvas.add(helix);
		canvas.centerObjectH(helix).centerObjectV(helix);
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
			marginTop += margin;
			marginMax = -$('.mosaic-block').height()*marginFactor;
			$('#Grade').css({'-webkit-transform':'translate(0px,'+marginTop+'px)'});
			if(marginTop > 0 && margin > 0){
				$('#Grade').css({'webkit-transform':'translate(0px,'+marginTop+'px)'}); marginTop = 0;
				setTimeout(function(){$('#Grade').css({'webkit-transform':'translate(0px,'+marginTop+'px)'});},1000);
			}else if(marginMax-marginTop > 0 && margin < 0){
				$('#Grade').css({'webkit-transform':'translate(0px,'+marginTop+'px)'}); marginTop = marginMax;
				setTimeout(function(){$('#Grade').css({'webkit-transform':'translate(0px,'+marginTop+'px)'});},1000);
			}
		}
	});
	canvas.observe('mouse:move',function(e) 
	{
		if (holding) {
			clicked = false;
			pos = canvas.getPointer(e.memo.e);
			x = (cX)-pos.x; y = (cY)-pos.y;
			if (velocity < 0) velocity = -velocity;
			// Sentido antihorario
			if (velocity >= last) {
				margin = -$('.mosaic-block').height()*2;
				last = velocity;
				velocity = -(Math.atan(y/x)/radians);
				velocity -= acceleration;
			// Sentido horario
			} else if (velocity < last) {
				margin = $('.mosaic-block').height()*2;
				last = velocity;
				velocity = Math.atan(y/x)/radians;
				velocity += acceleration;
			}
			if (x <= cX && y <= cY)	velocity = -velocity;	
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
		$.fn.hideMenus();
    	}
    	helix.angle = helix.theta*radians;
	canvas.renderAll();
	window.requestAnimationFrame(function() { animateElements(time); });
}

});
