const button=document.querySelector('.menu-toggle');
const menu=document.querySelector('.menu');
if(button&&menu){button.addEventListener('click',()=>menu.classList.toggle('open'));}
