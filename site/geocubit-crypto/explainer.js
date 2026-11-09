"use strict";
const byId=(id)=>document.getElementById(id);
const layers={
 physical:{tag:"DEFINITION / MEASUREMENT",index:"01 / 07",title:"Local cubit & calibration",summary:"A locally measured acoustic wavelength defines a state-dependent engineering length, not a shared secret.",formula:"C₀ = v(local) / (16 × fcal)",use:"Physical array spacing, local calibration, traceable uncertainty and normalized coordinates.",limit:"Cosmological nonlocal agreement, device identity or cryptographic hardness.",next:"The proposed remote invariant is the signed *definition and representation*, not a measured identical length."},
 canonical:{tag:"PROTOCOL DESIGN",index:"02 / 07",title:"Canonical geometric context",summary:"A deterministic binary encoding of manifold, frame, calibration and protocol version makes different devices agree on identical transcript bytes.",formula:"context = encode(profile, atlas, frame, epoch, uncertainty)",use:"Domain separation, integrity of geometric claims, reproducible hashing and consensus.",limit:"Secret entropy from public geometry, automatic equality of distinct calibration frames.",next:"Canonicalization must define equivalent quaternion signs, fixed-point precision, byte order, limits and rejection cases."},
 crypto:{tag:"STANDARDIZED PRIMITIVES",index:"03 / 07",title:"Post-quantum cryptography",summary:"Independently reviewed cryptographic algorithms establish and authenticate the session, while geometric context is bound as authenticated data.",formula:"K = KMAC256(KEM_secret, transcript, 256, label)",use:"Authenticated session keys, signed policy, key confirmation and AEAD records.",limit:"Security from a 64-bit routing header, CRC, geometry-only puzzle, or unreviewed hand-built primitive.",next:"ML-KEM encapsulation, ML-DSA authentication and robust randomness are algorithm/library dependencies, not browser demonstrations."},
 hyperbolic:{tag:"ESTABLISHED GEOMETRY",index:"04 / 07",title:"Hyperbolic address space",summary:"Negative-curvature manifolds and reduced group words can represent hierarchical network structure. They need not be cryptographically hard.",formula:"address = canonicalize(path in H³, profile, epoch)",use:"Routing, structured indexes, sparse hierarchy and authenticated geometric commitments.",limit:"One-wayness from curvature or group noncommutativity alone.",next:"The hyperbolic path identifier is hashed and authenticated using standard primitives; security claims require reductions or adversarial cryptanalysis."},
 clock:{tag:"EXPERIMENTAL CLOCK",index:"05 / 07",title:"Geometric intrinsic clock",summary:"The Engine's finite phase schedule can label logical computation steps within a separately authenticated epoch.",formula:"phase(n) = (n mod 8, n mod 3); period = 24",use:"Deterministic phase scheduling, authenticated state-transition labels, testable clocks and history checkpointing.",limit:"Replay resistance, global synchronization, or cryptographic unpredictability from cyclic phase.",next:"Add random session nonces, monotonic counters, a stable epoch and drift/uncertainty bounds."},
 simulation:{tag:"UNPROVEN HARDNESS",index:"06 / 07",title:"Forced-simulation research",summary:"Sequential geometric iteration may generate an auditable workload; no known security reduction establishes universal resistance to shortcuts.",formula:"stateₙ₊₁ = F(stateₙ, challenge), prove/check(stateₙ)",use:"Benchmarking verifiable-delay candidates, anti-spam proof-of-work experiments and bounded procedural tests.",limit:"Guaranteed sequential complexity, generic factoring hardness, P ≠ NP or post-quantum security.",next:"Compare against established VDF/time-lock designs and adversaries with parallel, optimized and quantum hardware."},
 waves:{tag:"CHANNEL EXPERIMENT",index:"07 / 07",title:"Longitudinal wave embedding",summary:"An acoustic or electromagnetic signal can carry already-authenticated symbols or supplemental channel measurements.",formula:"signal(t) = carrier(t) × authenticated modulation",use:"Offline beacons, relative phase calibration, ranging and physical presence research.",limit:"Confidentiality, tamperproof identity or nonlocal propagation by default.",next:"Measure eavesdropping, propagation, multipath, BER, spoofing, replay, side channels and jamming."}
};
function chooseLayer(key){
 const d=layers[key];if(!d)return;
 document.querySelectorAll("[data-layer]").forEach(b=>{const active=b.dataset.layer===key;b.classList.toggle("active",active);b.setAttribute("aria-pressed",String(active));});
 byId("layer-tag").textContent=d.tag;
 byId("layer-tag").className="tag "+(["crypto"].includes(key)?"teal":(["simulation","waves"].includes(key)?"amber":"neutral"));
 [["layer-index","index"],["layer-title","title"],["layer-summary","summary"],["layer-formula","formula"],["layer-use","use"],["layer-limit","limit"],["layer-next","next"]].forEach(([id,prop])=>byId(id).textContent=d[prop]);
}
document.querySelectorAll("[data-layer]").forEach(b=>b.addEventListener("click",()=>chooseLayer(b.dataset.layer)));
function recalibrate(){
 const speed=Number(byId("speed").value),distance=Number(byId("distance").value),cubit=speed/640;
 byId("speed-label").textContent=speed.toFixed(2)+" m/s";byId("distance-label").textContent=distance.toFixed(2)+" m";
 byId("cubit-value").textContent=cubit.toFixed(5)+" m";byId("normalized-value").textContent=(distance/cubit).toFixed(3);
}
["speed","distance"].forEach(id=>byId(id).addEventListener("input",recalibrate));recalibrate();
const phaseTrack=byId("phase-track");
for(let i=0;i<8;i++){const item=document.createElement("span");item.textContent=String(i);phaseTrack.appendChild(item);}
function setTick(n){
 const k=Math.max(0,Math.min(119,n));byId("tick").value=String(k);
 byId("tick-label").textContent=String(k);byId("spinor-value").textContent=(k%8)+" / 8";
 byId("triad-value").textContent=(k%3)+" / 3";byId("frame-value").textContent=String(k%24).padStart(2,"0")+" / 24";
 [...phaseTrack.children].forEach((node,i)=>node.classList.toggle("active",i===k%8));
}
byId("tick").addEventListener("input",e=>setTick(Number(e.target.value)));
byId("tick-forward").addEventListener("click",()=>setTick(Number(byId("tick").value)+1));
byId("tick-back").addEventListener("click",()=>setTick(Number(byId("tick").value)-1));
byId("tick-reset").addEventListener("click",()=>setTick(0));setTick(0);
const handshake=[
 {title:"ClientHello: state what you support",description:"Alice declares supported versions and suites and supplies an unpredictable nonce and the canonical commitment to her local geometric context.",code:"A → B: version, suites, ctxHashA, nonceA",check:"Supported version, signature algorithms and all negotiation bytes must be covered by the eventual authenticated transcript."},
 {title:"Signed ServerHello: authenticate the responder",description:"Bob selects a mutually supported suite, sends a fresh ephemeral ML-KEM encapsulation public key, a nonce and his signed geometric context.",code:"B → A: chosenSuite, nonceB, ctxHashB,\n       kemPublicEphemeral, certB, signatureB",check:"Alice validates credential policy, signature, ML-KEM key format, freshness and downgrade protection. No context field is secretly trusted."},
 {title:"ClientKey: establish and confirm the secret",description:"Alice encapsulates to Bob's authenticated KEM public key, signs the complete prior transcript when mutual authentication is required and confirms possession of the derived secret.",code:"A → B: kemCiphertext, certA?, signatureA?,\n       MAC_finishedA(transcriptHash)",check:"Bob verifies the signature, decapsulates with its ephemeral secret, derives session keys and validates Finished A without leaking failure details."},
 {title:"ServerFinished: complete mutual key confirmation",description:"Bob authenticates his view of the complete transcript using a distinct direction-specific confirmation key, then binds the epoch and counter allocation.",code:"B → A: MAC_finishedB(transcriptHash,\n       sessionEpoch, counterStart)",check:"Reject mismatched transcripts, replayed nonces, unsupported suites or ambiguous epochs. Confirmation uses separated keys and a canonical schema."},
 {title:"AEAD records: protect the real data",description:"Both peers encrypt records under distinct direction-specific keys, track sequence numbers, authenticate geometric metadata as associated data, and rekey before nonce exhaustion.",code:"record = AEAD_Encrypt(key_dir, nonce_seq,\n        payload, AD=encode(epoch,seq,ctxHash))",check:"Enforce per-key unique nonces, replay windows and ordered ratchets. Persistent counter state must survive crash recovery."}
];
let hs=0;function setHandshake(n){
 hs=Math.max(0,Math.min(4,n));const d=handshake[hs];
 [["hs-count","STEP "+(hs+1)+" / 5"],["hs-title",d.title],["hs-description",d.description],["hs-code",d.code],["hs-check",d.check]].forEach(([id,v])=>byId(id).textContent=v);
 document.querySelectorAll("[data-step]").forEach(b=>{const a=Number(b.dataset.step)===hs;b.classList.toggle("active",a);b.setAttribute("aria-pressed",String(a));});
 byId("hs-previous").disabled=hs===0;byId("hs-next").disabled=hs===4;
}
document.querySelectorAll("[data-step]").forEach(b=>b.addEventListener("click",()=>setHandshake(Number(b.dataset.step))));
byId("hs-previous").addEventListener("click",()=>setHandshake(hs-1));
byId("hs-next").addEventListener("click",()=>setHandshake(hs+1));setHandshake(0);
const threats={
 quantum:{status:"QUANTUM ADVERSARY",title:"Harvest-now, decrypt-later",description:"A powerful future quantum attacker may decrypt recordings from RSA/ECDH-only key establishment.",control:"Authenticated post-quantum key establishment, ephemeral KEM key lifecycle, long-term credential rotation and a migration policy.",residual:"Quantum-resistance of mathematical primitives does not prevent software vulnerabilities, credential theft or side channels."},
 mitm:{status:"ACTIVE NETWORK ATTACKER",title:"Man-in-the-middle and downgrade",description:"An attacker substitutes geometric context, public keys, algorithm lists or endpoint identities.",control:"Validate authenticated credential chains, sign full handshake transcripts, bind suite negotiation, enforce key confirmation.",residual:"Key distribution, compromised roots and social engineering remain separate threats."},
 replay:{status:"REPLAY / ROLLBACK",title:"A 24-phase clock repeats",description:"An adversary replays a previously valid phase, packet or authenticated message after a cycle or reboot.",control:"Random session identifiers, persistent epochs, monotonic counters, AEAD nonce uniqueness, anti-replay windows.",residual:"Crash recovery and replica consistency require storage and distributed-system design."},
 device:{status:"COMPROMISED ENDPOINT",title:"Stolen credentials or firmware",description:"An attacker extracts long-term keys, subverts random-number generation or replaces signed firmware.",control:"Protected key storage, secure boot, measured updates, revocation, transparency logs and key rotation.",residual:"Cryptography cannot fully protect data while an authorized endpoint is under attacker control."},
 physical:{status:"ACOUSTIC / EM ADVERSARY",title:"Spoofed or jammed carrier",description:"A nearby observer can record, echo, synthesize or jam a longitudinal-wave signal.",control:"Treat the carrier as untrusted; AEAD all content and bind any physical measurements with challenge-response and uncertainty.",residual:"Ranging, proximity and channel secrecy require separate validated physical assumptions."},
 precision:{status:"ENCODING ATTACK",title:"One geometry, multiple byte strings",description:"Floating-point NaNs, negative zero, quaternion antipodes, roundoff or profile mismatch yield inconsistent commitments.",control:"Reject noncanonical values, use fixed-point encodings, explicit width/endian, schema IDs and cross-language test vectors.",residual:"Representation equivalences and coordinate-frame conversions must be proven to commute with the chosen canonicalizer."}
};
function setThreat(key){const d=threats[key];if(!d)return;
 for(const [id,value] of Object.entries({"threat-status":d.status,"threat-title":d.title,"threat-description":d.description,"threat-control":d.control,"threat-residual":d.residual}))byId(id).textContent=value;
 document.querySelectorAll("[data-threat]").forEach(b=>{const a=b.dataset.threat===key;b.classList.toggle("active",a);b.setAttribute("aria-pressed",String(a));});
}
document.querySelectorAll("[data-threat]").forEach(b=>b.addEventListener("click",()=>setThreat(b.dataset.threat)));setThreat("quantum");
function fieldBytes(value){
 const bytes=new TextEncoder().encode(value), header=new Uint8Array(4);new DataView(header.buffer).setUint32(0,bytes.length,false);
 const out=new Uint8Array(header.length+bytes.length);out.set(header);out.set(bytes,4);return out;
}
async function computeHash(){
 const output=byId("hash-result"),geometry=fieldBytes(byId("geometry-input").value),message=fieldBytes(byId("message-input").value);
 const combined=new Uint8Array(geometry.length+message.length);combined.set(geometry);combined.set(message,geometry.length);
 if(!globalThis.crypto?.subtle){output.textContent="Web Crypto unavailable here (use HTTPS or localhost).";return;}
 try{const hash=await crypto.subtle.digest("SHA-256",combined);output.textContent=[...new Uint8Array(hash)].map(v=>v.toString(16).padStart(2,"0")).join("");}
 catch(err){output.textContent="Digest unavailable in this browser context.";}
}
let generation=0;async function safeHash(){const n=++generation; const output=byId("hash-result");output.textContent="Computing…";await computeHash();if(n!==generation)output.textContent="Inputs changed; recomputing…";}
["geometry-input","message-input"].forEach(id=>byId(id).addEventListener("input",safeHash));safeHash();
