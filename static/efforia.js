var view = true;
var known = false;
var favor = true;
var margin = 200;
var w = window.innerWidth*0.83875;
var h = window.innerHeight*0.95;
document.documentElement.style.overflowX = 'hidden';
document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){
	
document.onselectstart = function () { return false; } // ie
document.onmousedown = function () { return false; } // mozilla

document.getElementById('efforia').width = w;
document.getElementById('efforia').height = h;

$('#conhecidos').hide();
$('.fade').mosaic();
$('.mosaic-block').css({height:h*0.2});
$('.mosaic-small-block').css({height:h*0.05});
$('#conteudoCentral').masonry({itemSelector:'.mosaic-block'});
$('#dialogo').dialog({height:'auto',width:'auto',modal:true});
$("input:submit, button", "#botoes" ).button();
$('#radio').buttonsetv();

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
});

$('.mosaic-block').bind("click",function(){ view = false; });

var widthNow = $('body').width();
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
	w = window.innerWidth*0.83875;
	h = window.innerHeight*0.95;
	$('#conteudoCanvas,.canvas-container,.lower-canvas,#efforia').css({'height':h,'width':w});
	cX = canvas.width/2;
	cY = canvas.height/2;
	canvas.clear();
	scaleFactor = h/900;
	helix.scale(scaleFactor);
	scaleFactor = w/800;
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
		helix = new fabric.PathGroup(objects);
		scaleFactor = h/900;
		helix.scale(scaleFactor);
		w = window.innerWidth*0.6775;
		scaleFactor = w/1100;
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
			$('.mosaic-block').animate({"bottom":"-="+margin+"px"},1000); 
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
				margin = -200;
				last = velocity;
				velocity = -(Math.atan(y/x)/radians);
				velocity -= acceleration;
			// Sentido horario
			} else if (velocity < last) {
				margin = 200;
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
    		$('#horizontal').tubeplayer('destroy');
    		$('#horizontal').empty();
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
