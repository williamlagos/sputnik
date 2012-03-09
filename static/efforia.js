document.documentElement.style.overflowX = 'hidden';	 // horizontal scrollbar will be hidden
document.documentElement.style.overflowY = 'hidden';

$(document).ready(function(){

var view = true;
var known = false;
var favor = true;
var margin = 200;

$('.fade').mosaic();
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

var w = window.innerWidth*0.7-10;
var h = window.innerHeight-10;
document.getElementById('efforia').width = w;
document.getElementById('efforia').height = h;

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
	fabric.Image.fromURL('images/backleft.png', function(img) 
	{
		scaleFactor = h/900;
		img.scale(scaleFactor);
		img.hasBorders = img.hasControls = false;
		img.lockScalingX = img.lockScalingY = true;
		img.lockMovementX = img.lockMovementY = true;
		canvas.add(img.set({top:(h/2),left:50}));
	});
	fabric.Image.fromURL('images/backright.png', function(img) 
	{
		scaleFactor = h/900;
		img.scale(scaleFactor);
		img.hasBorders = img.hasControls = false;
		img.lockScalingX = img.lockScalingY = true;
		img.lockMovementX = img.lockMovementY = true;
		canvas.add(img.set({top:(h/2),left:w-40}));
	});
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
