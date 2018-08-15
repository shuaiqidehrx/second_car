window.onload=function(){
    var list=document.getElementById("list");
    var box1=document.getElementById("box1");
    var speed =5;
    var leftnew = 0;
    // var time=null;
    // var b1=document.getElementById("b1");
    // var b2=this.document.getElementById("b2");
    // list.innerHTML+=list.innerHTML
    // 定位取值
    f1=setInterval(f,20);
    function f(){
        leftnew+=speed;
        if (leftnew>905){
        speed=-5;
        return;}
        if(leftnew<0){
            speed=5;
            return;
        }
        list.style.left=leftnew+'px';
        box1.onmouseover=function(){
            clearInterval(f1)}
        box1.onmouseout=function(){
            setInterval(f,20)
        }
        
    }




}