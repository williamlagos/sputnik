var w = window.innerWidth*0.6775;
var h = window.innerHeight;

$(document).ready(function(event){
	event.preventDefault();
	$('#horizontal').draggable();
	$('#conteudoDireita').droppable({
			drop: function( event, ui ) {
				$( this )
					.addClass( "ui-state-highlight" )
					$('#conteudoDireita').html( "Dropped!" );
			}
	});
});

