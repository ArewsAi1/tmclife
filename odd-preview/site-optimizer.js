(function(){
  function normalizePath(value){
    try{return new URL(value,location.href).pathname.replace(/^\//,'').replace(/\/$/,'').toLowerCase();}catch(_){return '';}
  }

  function normalizeTopNavigation(){
    var routes={
      'home':'https://www.ogdendeckdepot.com/',
      'shop now':'https://ogdendeckdepot.shop.ruckdelivery.com/?utm_source=ogdendeckdepot&utm_medium=header_nav&utm_campaign=shop&utm_content=header_shop_button',
      'our products':'https://www.ogdendeckdepot.com/products-ogden-deck-depot.html',
      'about':'https://www.ogdendeckdepot.com/about.html',
      'service area':'https://www.ogdendeckdepot.com/service-areas.html',
      'blog':'https://www.ogdendeckdepot.com/blog.html',
      'write a review':'https://bit.ly/3bNtmAJ',
      'other construction products':'https://www.ogdendeckdepot.com/other-products.html',
      'media room':'https://www.ogdendeckdepot.com/contact.html'
    };
    document.querySelectorAll('.nav > ul > li > a,.wsite-menu-default > li > a').forEach(function(link){
      var key=(link.textContent||'').trim().replace(/\s+/g,' ').toLowerCase();
      if(routes[key]){
        link.setAttribute('href',routes[key]);
        link.onclick=null;
        link.removeAttribute('data-membership-required');
      }
    });
  }

  function normalizeAllInternalLinks(){
    var canonical={
      'index.html':'/',
      'home.html':'/',
      'products.html':'/products-ogden-deck-depot.html',
      'decking-composite.html':'/composite-decking-ogden.html',
      'deck-footings-ogden.html':'/ogden-deck-depot-helical-pier-pylon-deck-footing.html',
      'deck-lumber.html':'/lumber-yard-929035.html',
      'deck-supplier-ogden-ut-gmb-stack.html':'/service-areas.html',
      'ogden-ut.html':'/service-areas.html',
      'other-construction-products.html':'/other-products.html',
      'pergolas--awnings.html':'/other-products.html',
      'deck-features-and-accessories.html':'/other-products.html',
      'simpson-strong-tie.html':'/simpson-strong-tie-lu210-mount-joist-hanger-206311-927519-771247-485754-191033.html',
      'trex-rainescape-ogden-depot.html':'/zip-up-underdeck-ceilings-lighting-ogden.html',
      'media-room.html':'/contact.html',
      'material-sales-lead-form.html':'/contact.html',
      'form-submission.html':'/forms.html'
    };
    document.querySelectorAll('a[href]').forEach(function(link){
      var raw=link.getAttribute('href')||'';
      if(!raw||raw.charAt(0)==='#'||raw.indexOf('tel:')===0||raw.indexOf('mailto:')===0||raw.indexOf('javascript:')===0)return;
      try{
        var url=new URL(raw,location.href);
        if(url.hostname==='ogdendeckdepot.com')url.hostname='www.ogdendeckdepot.com';
        if(url.hostname!=='www.ogdendeckdepot.com')return;
        var key=url.pathname.replace(/^\//,'').toLowerCase();
        if(canonical[key])url.pathname=canonical[key];
        url.protocol='https:';
        link.setAttribute('href',url.toString());
        link.onclick=null;
        link.removeAttribute('data-membership-required');
      }catch(_){}
    });
  }

  function pruneLegacyNavigation(){
    var links=document.querySelectorAll('.nav a,.wsite-menu a');
    links.forEach(function(link){
      var path=normalizePath(link.getAttribute('href')||'');
      if(path==='blog.html'||path==='blog'){
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

    document.querySelectorAll('.nav > ul > li').forEach(function(topItem){
      var topLink=topItem.querySelector(':scope > a');
      if(!topLink)return;
      var text=(topLink.textContent||'').trim().toLowerCase();
      var path=normalizePath(topLink.getAttribute('href')||'');
      if(text.indexOf('our products')===-1&&path!=='products-ogden-deck-depot.html')return;
      topItem.querySelectorAll('.wsite-menu .wsite-menu .wsite-menu-wrap').forEach(function(deepMenu){deepMenu.remove();});
      topItem.querySelectorAll('.wsite-menu .wsite-menu-item-wrap-has-children').forEach(function(item){item.classList.remove('wsite-menu-item-wrap-has-children');});
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

  function restoreContactPage(){
    var currentPath=normalizePath(location.href);
    if(currentPath!=='contact.html'&&currentPath!=='contact')return;
    var content=document.querySelector('#wsite-content,.main-wrap .container,.wsite-section-elements');
    if(!content)return;
    Array.from(content.querySelectorAll('h1,h2,h3,div.paragraph,p')).forEach(function(el){
      if((el.textContent||'').trim().toLowerCase()==='under construction')el.textContent='Contact Ogden Deck Depot';
    });
    if(document.getElementById('odd-contact-form'))return;
    var section=document.createElement('section');
    section.id='odd-contact-form';
    section.className='odd-contact-card';
    section.innerHTML='<h2>Tell Us What You Need</h2><p>Ask about decking, railing, lumber, hardware, delivery, product availability, or contractor pricing. You can also call <a href="tel:+14352225819">(435) 222-5819</a>.</p><form><div class="odd-form-grid"><label>Name<input name="name" autocomplete="name" required></label><label>Phone<input name="phone" type="tel" autocomplete="tel"></label><label>Email<input name="email" type="email" autocomplete="email"></label><label>City<input name="city" autocomplete="address-level2"></label></div><label>What can we help with?<select name="project_type"><option value="Decking materials">Decking materials</option><option value="Railing">Railing</option><option value="Lumber and framing">Lumber and framing</option><option value="Hardware and fasteners">Hardware and fasteners</option><option value="Delivery or contractor pricing">Delivery or contractor pricing</option><option value="Other">Other</option></select></label><label>Details<textarea name="message" rows="5"></textarea></label><input name="website" tabindex="-1" autocomplete="off" class="odd-hp" aria-hidden="true"><input type="hidden" name="lead_type" value="contact-page"><input type="hidden" name="source_url" value="'+location.href.replace(/"/g,'&quot;')+'"><button type="submit">Send Request</button><p class="odd-form-status" role="status" aria-live="polite"></p></form>';
    content.appendChild(section);
    var form=section.querySelector('form');
    form.addEventListener('submit',async function(event){
      event.preventDefault();
      var status=section.querySelector('.odd-form-status');
      var button=form.querySelector('button');
      status.textContent='Sending...';button.disabled=true;
      try{
        var response=await fetch('/api/lead',{method:'POST',body:new FormData(form)});
        var result=await response.json();
        if(!response.ok||!result.ok)throw new Error(result.error||'Unable to send request.');
        status.textContent=result.message||'Thanks — your request was received.';form.reset();
      }catch(error){status.textContent=(error&&error.message)||'Please call (435) 222-5819.';}
      finally{button.disabled=false;}
    });
  }

  function run(){normalizeTopNavigation();normalizeAllInternalLinks();pruneLegacyNavigation();improveControls();restoreContactPage();document.documentElement.classList.add('odd-optimized');}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run,{once:true});else run();
})();
