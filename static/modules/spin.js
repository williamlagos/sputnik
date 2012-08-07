$.fn.createElements = function(){
	fabric.loadSVGFromURL('interface.svg', function(objects,options) 
	{
		canvas.forEachObject(function(obj) {
			obj.hasBorders = obj.hasControls = false;
			obj.lockScalingX = obj.lockScalingY = true;
			obj.lockMovementX = obj.lockMovementY = true;	
		});
		canvas.selection = false;
		$.e.helix = new fabric.PathGroup(objects);
		scaleFactor = $.e.h/900;
		$.e.helix.scale(scaleFactor);
		$.e.widthNow = $('body').width();
		if($.e.widthNow < 1280) $('body').css({'font-size':'0.8em'});
		else if($.e.widthNow > 1280) $('body').css({'font-size':'1.0em'});
		canvas.add($.e.helix);
		canvas.centerObjectH($.e.helix).centerObjectV($.e.helix);
		listenEvents();
	});
}

function listenEvents()
{
	canvas.observe('mouse:down',function(e) { $.e.holding = true; $.e.clicked = true; });
	canvas.observe('mouse:up'  ,function(e) { 
		$.e.holding = false;
		$.e.value = true; 
		if(!$.e.clicked){
			$.e.marginTop += margin;
			$.e.marginMax = -$('.mosaic-block').height()*$.e.marginFactor;
			$('#Grade').translate2D(0,$.e.marginTop);
			if($.e.marginTop > 0 && margin > 0){
				$('#Grade').translate2D(0,$.e.marginTop); $.e.marginTop = 0;
				setTimeout(function(){$('#Grade').translate2D(0,$.e.marginTop);},1000);
			}else if($.e.marginMax-$.e.marginTop > 0 && margin < 0){
				$('#Grade').translate2D(0,$.e.marginTop); $.e.marginTop = $.e.marginMax;
				setTimeout(function(){$('#Grade').translate2D(0,$.e.marginTop);},1000);
			}
		}
	});
	canvas.observe('mouse:move',function(e) 
	{
		if ($.e.holding) {
			$.e.clicked = false;
			pos = canvas.getPointer(e.memo.e);
			x = ($.e.cX)-pos.x; y = ($.e.cY)-pos.y;
			if ($.e.velocity < 0) $.e.velocity = -$.e.velocity;
			// Sentido antihorario
			if ($.e.velocity >= $.e.last) {
				margin = -$('.mosaic-block').height()*2;
				$.e.last = $.e.velocity;
				$.e.velocity = -(Math.atan(y/x)/$.e.radians);
				$.e.velocity -= $.e.acceleration;
			// Sentido horario
			} else if ($.e.velocity < $.e.last) {
				margin = $('.mosaic-block').height()*2;
				$.e.last = $.e.velocity;
				$.e.velocity = Math.atan(y/x)/$.e.radians;
				$.e.velocity += $.e.acceleration;
			}
			if (x <= $.e.cX && y <= $.e.cY)	$.e.velocity = -$.e.velocity;	
			$.e.helix.theta += $.e.velocity;
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
   	if (!$.e.holding && !$.e.clicked) {
		angularFriction = 0.1;
		angularVelocity = $.e.velocity*timeDiff*(1-angularFriction)/1000;
		$.e.velocity -= angularVelocity;
    	$.e.helix.theta += $.e.velocity;
	} else if (!$.e.holding && $.e.clicked && $.e.value) {
		$.fn.hideMenus();
	}
	$.e.helix.angle = $.e.helix.theta*$.e.radians;
	canvas.renderAll();
	window.requestAnimationFrame(function() { animateElements(time); });
}

$.fn.createElements();
