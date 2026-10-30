"use strict";
const alpha = document.querySelector('#alpha');
const frame = document.querySelector('#frame');
function updateBudget() {
  const a = Number(alpha.value), b = 2 ** (1-a);
  document.querySelector('#alpha-value').textContent = a.toFixed(2);
  document.querySelector('#budget').textContent = `b = ${b.toFixed(4)} · ε = ${(2-b).toFixed(4)}`;
  document.querySelector('#locked').setAttribute('width', String(400*a));
}
function updateRoute() {
  const n = Number(frame.value);
  document.querySelector('#frame-value').textContent = String(n);
  const type = [2,10,18].includes(n) ? 'onload' : [6,14,22].includes(n) ? 'offload' : 'ordinary frame';
  document.querySelector('#route').textContent = `k = ${n%8} · j = ${n%3} · ${type}`;
  document.querySelectorAll('#slots span').forEach(el => {el.style.color = Number(el.dataset.frame) === n ? '#ffcf70' : '';});
}
for (const n of [2,6,10,14,18,22]) {
  const el = document.createElement('span'); el.dataset.frame = String(n); el.textContent = String(n); document.querySelector('#slots').append(el);
}
alpha.addEventListener('input', updateBudget); frame.addEventListener('input', updateRoute);
updateBudget(); updateRoute();
