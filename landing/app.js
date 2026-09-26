const hires = [
 ['necromancer','레거시 고고학자','전임자는 퇴사했다. 이유는 Git에 남았다.','현재 호출부와 Git 이력으로 이상한 코드가 남아 있는 이유를 추적합니다.','이 호환성 분기 지워도 됨?'],
 ['receipt','수정 검증관','고쳤다고? 전후 증거부터.','수정 전 실패와 수정 후 통과를 실제 실행으로 확인합니다.','이 수정으로 진짜 중복 저장이 막히는지 확인해줘.'],
 ['landlord','구조 관리인','이 추상화 유지비는 누가 냄?','추상화와 의존성의 실제 소비자, 유지 비용을 검토합니다.','이 추상화가 지금 프로젝트에 필요한지 봐줘.'],
 ['mother-in-law','클릭 꼬투리 QA','저장 누르고 또 누르면?','중복 동작, 응답 순서, 복구 등 실제 사용자 흐름을 검증합니다.','저장 버튼을 두 번 눌러도 괜찮은지 확인해줘.'],
 ['exorcist','가설 퇴마사','캐시 탓이라는 귀신부터 잡자.','경쟁하는 원인 가설을 구분할 수 있는 실험을 설계합니다.','이 버그가 캐시 때문인지 실험으로 구분해줘.'],
 ['hostage-negotiator','범위 협상가','버튼 하나만 고치기로 했잖아요.','작은 수정 요청이 불필요한 리팩터링으로 커지는 것을 막습니다.','이 버튼 수정이 요청한 범위를 벗어나는지 봐줘.'],
 ['con-artist','테스트 사기 감별사','테스트가 mock한테 속고 있습니다.','격리된 복사본에서 동작을 망가뜨려도 테스트가 통과하는지 확인합니다.','저장 로직이 깨져도 이 테스트가 통과하는지 감사해줘.'],
 ['friday','배포 생존 담당','월요일의 내가 복구할 수 있음?','배포 전 버전 호환성, 마이그레이션, 롤백 가능성을 검토합니다.','이 배포 롤백 가능한지 봐줘.']
];
const roster=document.querySelector('.roster');
hires.forEach(([id,name,quote],i)=>{const b=document.createElement('button');b.className='hire';b.type='button';b.setAttribute('aria-pressed',String(i===0));b.innerHTML=`<span class="number">0${i+1}</span><span><strong>${name}</strong><span class="codename">${id}</span><span class="quote">${quote}</span></span><span class="arrow" aria-hidden="true">↗</span>`;b.addEventListener('click',()=>select(i));roster.append(b)});
function select(i){const [id,, ,description,prompt]=hires[i];roster.querySelectorAll('button').forEach((b,n)=>b.setAttribute('aria-pressed',String(i===n)));document.querySelector('#skill-description').textContent=description;document.querySelector('#skill-prompt').textContent=`$${id}\n${prompt}`;document.querySelector('#example-link').href=`https://github.com/SoonGwan/questionable-hires/blob/main/examples/${id}.md`}
select(0);
document.querySelector('#copy').addEventListener('click',async()=>{const status=document.querySelector('#copy-status');try{await navigator.clipboard.writeText('npx skills add SoonGwan/questionable-hires');status.textContent='복사했습니다. 터미널에 붙여넣으세요.'}catch{status.textContent='복사하지 못했습니다. 위 명령을 직접 선택해 복사해주세요.'}});
if(!matchMedia('(prefers-reduced-motion: reduce)').matches&&'IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target)}}),{threshold:.08});document.querySelectorAll('.section-heading,.manifesto h2,.principles,.evidence-link,.install h2').forEach(el=>{el.classList.add('reveal');observer.observe(el)});document.querySelector('.hero h1').animate([{opacity:0,transform:'translateY(22px)'},{opacity:1,transform:'translateY(0)'}],{duration:800,easing:'cubic-bezier(.22,1,.36,1)'});}
