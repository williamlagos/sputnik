$(document).ready(function(){

$('.superior').bind("click",function(){ $('.superior:visible').hide('fade'); });
$('.inferior').bind("click",function(){ $('.superior:hidden' ).show('fade'); });

$('#conteudoCentral').bind('mouseenter',function(){
	$('#conteudoEsquerda:visible').hide('fade');
        $('#conteudoDireita:visible').hide('fade');
});

$('#conteudoCentral').bind('mouseleave',function(){
	$('#conteudoEsquerda:hidden').show('fade');
        $('#conteudoDireita:hidden').show('fade');
});

});
