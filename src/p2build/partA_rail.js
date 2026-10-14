
const chapters = [...document.querySelectorAll('.chapter')].map(el=>({
  id: el.id,
  title: el.querySelector('.chapter-head h2')?.textContent || el.id,
  num: el.querySelector('.chapter-num')?.textContent || ''
}));

const railList = document.getElementById('railList');
railList.innerHTML = chapters.map(c=>`<li><a href="#${c.id}" data-id="${c.id}">${c.num} ${c.title}</a></li>`).join('');

const mobNav = document.getElementById('mobNav');
mobNav.innerHTML = chapters.map(c=>`<option value="${c.id}">${c.num} · ${c.title}</option>`).join('');
mobNav.addEventListener('change', ()=>{
  document.getElementById(mobNav.value)?.scrollIntoView({behavior:'smooth', block:'start'});
});

const railLinks = [...railList.querySelectorAll('a')];
const observer = new IntersectionObserver((entries)=>{
  entries.forEach(entry=>{
    const link = railLinks.find(a=>a.dataset.id===entry.target.id);
    if(!link) return;
    if(entry.isIntersecting){
      railLinks.forEach(a=>a.classList.remove('active'));
      link.classList.add('active');
      mobNav.value = entry.target.id;
    }
  });
}, {rootMargin:'-10% 0px -70% 0px', threshold:0});
chapters.forEach(c=>{ const el=document.getElementById(c.id); if(el) observer.observe(el); });
