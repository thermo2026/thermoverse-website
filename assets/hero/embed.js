(() => {
const media=document.querySelector('.hero-animation'),frame=media.querySelector('iframe'),button=media.querySelector('button');
let paused=matchMedia('(prefers-reduced-motion: reduce)').matches;
function update(){button.setAttribute('aria-label',paused?'Play animation':'Pause animation');button.setAttribute('aria-pressed',String(paused));button.querySelector('path').setAttribute('d',paused?'M8 5l11 7-11 7Z':'M8 6v12M16 6v12')}
button.addEventListener('click',()=>{const scene=frame.contentWindow.heroAnimation;if(!scene)return;paused=!paused;paused?scene.pause():scene.play();update()});update();
new IntersectionObserver(entries=>{frame.contentWindow.postMessage({type:'hero-visible',visible:entries[0].isIntersecting},location.origin)},{threshold:.01}).observe(media);
})();
