$(document).ready(function(){
	
var known = false;
var favor = true;
var marginMax = 0;
var w = window.innerWidth*0.85;
var h = window.innerHeight-40;
document.getElementById('efforia').width = w;
document.getElementById('efforia').height = h;

$('a').click(function(){ this.blur(); });
$.get('/',{'feed':'feed'},function(data){
	$.e.initial = true; 
	$('#Grade').loadMosaic(data);
	$('#Grade').css({'height':h});
	$('.mosaic-block').mosaic();
	$.fn.eventLoop();
	if($('.blank').text() != '') $.e.marginFactor = 0;
	$.e.initial = false;
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

$.fn.createElements = function(){
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
		$.e.value = true; 
		if(!clicked){
			$.e.marginTop += margin;
			marginMax = -$('.mosaic-block').height()*$.e.marginFactor;
			$('#Grade').translate2D(0,$.e.marginTop);
			if($.e.marginTop > 0 && margin > 0){
				$('#Grade').translate2D(0,$.e.marginTop); $.e.marginTop = 0;
				setTimeout(function(){$('#Grade').translate2D(0,$.e.marginTop);},1000);
			}else if(marginMax-$.e.marginTop > 0 && margin < 0){
				$('#Grade').translate2D(0,$.e.marginTop); $.e.marginTop = marginMax;
				setTimeout(function(){$('#Grade').translate2D(0,$.e.marginTop);},1000);
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
	} else if (!holding && clicked && $.e.value) {
		$.fn.hideMenus();
	}
	helix.angle = helix.theta*radians;
	canvas.renderAll();
	window.requestAnimationFrame(function() { animateElements(time); });
}

$.fn.createElements();
});
