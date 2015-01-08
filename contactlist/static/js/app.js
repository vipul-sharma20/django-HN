$(document).ready(function() {
   $(".likes").click(function(){
    var catid;
    catid = $(this).attr("aid");
     $.get('/accounts/articles/like/'+catid+'/', {article_id: catid}, function(data){
               $("."+catid).html(data);
           });
});
   $(".comments").submit(function(){
       var id;
       id = $('.which').attr
       $.get('/accounts/articles/comments/)
});
