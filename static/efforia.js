function init() {
	(function() {
		if (!window.requestAnimationFrame ) {
			window.requestAnimationFrame = (function() {
				return window.webkitRequestAnimationFrame ||
        		window.mozRequestAnimationFrame ||
        		window.oRequestAnimationFrame ||
        		window.msRequestAnimationFrame ||
        		function(callback,element) {
          			window.setTimeout(callback,1000/60);
        		};
      		})();
    	}
		var canvas = new fabric.Canvas('efforia');
		setTimeout(drawShape(),1000);
		function drawShape() {
			fabric.loadSVGFromURL('/static/interface.svg', function(objects,options) {
				var helix = new fabric.PathGroup(objects,options);
				helix.set({
              		//left: coords[i].x,
              		//top: coords[i].y,
              		//angle: 30,
              		//fill: '#ff5555'
            	});
				canvas.add(helix);
  				canvas.centerObjectH(helix).centerObjectV(helix);
  				//canvas.centerObjectH(helix);
  				animate();
			});
		}
		var angle = 0;
		function animate() {
			angle += 2;
      		if (angle === 360) {
        		angle = 0;
      		}
      		canvas.item(0).setAngle(angle);
      		canvas.renderAll();
        	window.requestAnimationFrame(animate);
      	} 
	})();
}