(function(){
  function normalizePath(value){
    try{return new URL(value,location.href).pathname.replace(/^\//,'').toLowerCase();}catch(_){return '';}
  }

  function pruneLegacyNavigation(){
    var links=document.querySelectorAll('.nav a,.wsite-menu a');
    links.forEach(function(link){
      var path=normalizePath(link.getAttribute('href')||'');
      if(path==='blog.html'){
        var item=link.closest('li');
        if(item){
          var submenu=item.querySelector(':scope > .wsite-menu-wrap');
          if(submenu) submenu.remove();
          item.classList.remove('wsite-menu-item-wrap-has-children');
          link.removeAttribute('aria-haspopup');
        }
      }
    });

    document.querySelectorAll('.wsite-menu').forEach(function(menu){
      var seen=new Set();
      Array.from(menu.children).forEach(function(item){
        var link=item.querySelector(':scope > a');
        if(!link)return;
        var key=(normalizePath(link.getAttribute('href')||'')+'|'+(link.textContent||'').trim().toLowerCase());
        if(key!=='|'&&seen.has(key)) item.remove();
        else seen.add(key);
      });
    });
  }

  function improveControls(){
    document.querySelectorAll('a[target="_blank"]').forEach(function(link){
      var rel=new Set((link.getAttribute('rel')||'').split(/\s+/).filter(Boolean));
      rel.add('noopener');rel.add('noreferrer');link.setAttribute('rel',Array.from(rel).join(' '));
    });
    document.querySelectorAll('iframe').forEach(function(frame){frame.setAttribute('loading','lazy');frame.setAttribute('title',frame.getAttribute('title')||'Embedded content');});
    document.querySelectorAll('input,textarea,select').forEach(function(field){if(!field.getAttribute('autocomplete')&&field.type==='email')field.setAttribute('autocomplete','email');});
  }

  function run(){pruneLegacyNavigation();improveControls();document.documentElement.classList.add('odd-optimized');}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run,{once:true});else run();
})();
