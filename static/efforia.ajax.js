$(document).ready(function(){
$('.dialogo').click(function(event){
	event.preventDefault();
	$.ajax({
		url:this.href,
		success: function(data){
			$('#caixa').dialog({height:'auto',width:'auto',modal:true});
			$('#caixa').html(data);
		}
	});
});
/*$('.popup').click(function(event){
	event.preventDefault();
	$(".popup").popupwindow();
});*/
});
