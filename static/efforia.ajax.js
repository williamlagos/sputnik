$(document).ready(function(){
$('.dialogo').click(function(event){
	event.preventDefault();
	$.ajax({
		url:this.href,
		success: function(data){
			$('#caixa').dialog('destroy');
			$('#caixa').empty();
			$('#caixa').html(data);
			$('#caixa').dialog({title:'Entrar no Efforia',height:'auto',width:'auto',modal:true});
		}
	});
});
/*$('.popup').click(function(event){
	event.preventDefault();
	$(".popup").popupwindow();
});*/
});
