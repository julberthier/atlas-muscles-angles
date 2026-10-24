import json, os
D = r'C:\Users\boboo\Desktop\atlas-muscles-angles\voix'
p = r'C:\Users\boboo\Desktop\muscles-angles.html'
T = json.load(open(os.path.join(D, 'textes.json'), encoding='utf-8'))
A = lambda k, i: {'a': [k, i]}
SP = lambda k, f: {'sp': [k, f]}
CUES = {
 'dos': [("Tirage vertical :", A('dos', 0)), ("C'est le grand dorsal qui mène", SP('dos', 0)), ("Tirage horizontal, à hauteur", A('dos', 1)),
         ("Ce sont le trapèze moyen", SP('dos', 5)), ("Pull-over, bras tendus", A('dos', 2)), ("c'est la partie basse du grand dorsal", SP('dos', 1)),
         ("Et rowing buste penché", A('dos', 3)), ("Là, ce sont le deltoïde postérieur", SP('dos', 8)), ("Deuxième point clé", A('dos', 1))],
 'pec': [("Banc incliné, entre", A('pec', 0)), ("c'est la portion claviculaire", SP('pec', 0)), ("Banc plat :", A('pec', 1)), ("la portion sternale", SP('pec', 1)),
         ("Développé décliné", A('pec', 2)), ("la portion abdominale", SP('pec', 2))],
 'del': [("L'antérieur lève", A('del', 0)), ("Le moyen l'écarte", A('del', 1)), ("Le postérieur le ramène", A('del', 2)), ("L'antérieur travaille déjà", SP('del', 0)),
         ("l'écarté latéral est irremplaçable", A('del', 1)), ("Oiseau, face pull", A('del', 2)), ("quatre petits muscles forment la coiffe", A('del', 4)),
         ("l'omoplate bascule avec lui", A('del', 1)), ("dans le plan de l'omoplate", A('del', 3))],
 'bras': [("Bras au-dessus de la tête, la longue tête du triceps", A('tri', 0)), ("l'extension bras le long du corps", A('tri', 1)),
          ("Bras derrière le buste", A('bic', 0)), ("Au pupitre", A('bic', 2))],
 'avb': [("Les fléchisseurs du poignet", A('avb', 0)), ("Les extenseurs partent", A('avb', 1)), ("Et le brachioradial", A('avb', 2)),
         ("au curl en pronation", A('avb', 3)), ("Pouce vers le haut", A('avb', 2)), ("paume vers le bas, le brachioradial", A('avb', 3))],
 'abs': [("Au crunch", A('abs', 0)), ("Au relevé de genoux", A('abs', 1)), ("Sur les côtés, les obliques", A('abs', 2)), ("le transverse.", A('abs', 3)),
         ("le carré des lombes", A('abs', 4))],
 'fes': [("Son faisceau supérieur", SP('fes', 0)), ("Son faisceau inférieur", SP('fes', 1)), ("le moyen fessier stabilise", SP('fes', 2)),
         ("Pour l'extension de hanche, hip thrust", A('fes', 0)), ("le squat profond le charge étiré", A('fes', 2)), ("Pour l'abduction", A('fes', 1))],
 'cuisses': [("le squat fait grossir les vastes", A('quad', 2)), ("leg extension avec le dossier incliné", A('quad', 1)), ("les adducteurs forment", A('add', 0)),
             ("au squat profond et au squat sumo", A('add', 2))],
 'jambes': [("comme au soulevé de terre roumain", A('ham', 0)), ("comme au leg curl ou au nordic", A('ham', 1)), ("le leg curl assis", A('ham', 2)),
            ("Debout, genou tendu", A('calf', 0)), ("Assis, genou fléchi", A('calf', 1))],
 'bio': [("la tension dépend de la longueur", {'go': '#bio-i'}), ("Un muscle est le plus fort à mi-longueur", {'sar': 272}), ("Très raccourci", {'sar': 150}),
         ("Très étiré", {'sar': 390}), ("Deuxième principe", {'go': '#bio-ii', 'dc': 0}), ("Il change selon l'outil", {'dc': 1}),
         ("Troisième principe", {'go': '#bio-vi'}), ("Et rappelle-toi qu'en freinant", {'go': '#bio-v'})],
}
out = {}
for k, cues in CUES.items():
    al = json.load(open(os.path.join(D, k + '.align.json'), encoding='utf-8'))
    txt = T[k]
    assert al['c'] == txt, k + ' : alignement ≠ texte'
    lst = []
    for phrase, act in cues:
        i = txt.find(phrase)
        assert i >= 0, (k, phrase)
        lst.append([al['t'][i], act])
    lst.sort(key=lambda x: x[0])
    out[k] = lst
s = open(p, encoding='utf-8').read()


def R(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


# ancres de la biomécanique
for n, idv in [('I', 'bio-i'), ('II', 'bio-ii'), ('V', 'bio-v'), ('VI', 'bio-vi')]:
    a = '<div class="card">\n    <h3><span class="n">' + n + '</span>'
    if s.count(a) == 1:
        s = s.replace(a, '<div class="card" id="' + idv + '">\n    <h3><span class="n">' + n + '</span>')
    else:
        raise SystemExit('ancre ' + n + ' : ' + str(s.count(a)))
# repères + moteur de synchronisation
R('/* ============ VOIX OFF ============ */', '/* ============ VOIX OFF ============ */\nvar VOCUES=' + json.dumps(out, ensure_ascii=False) + ';')
R('''    box._pause=function(){''', '''    /* synchronisation : pendant la lecture, la voix pilote le schéma (angle, faisceau mis en avant, graphiques) */
    var sync=box.querySelector(".vo-sync"),cues=VOCUES[k]||[],ci=0,raf=0,lastEx=null;
    function act(c,quiet){var x=c[1];
      if(x.a){var bx=document.getElementById(x.a[0]+"-angles"),bt=bx&&bx.children[x.a[1]];if(bt&&!bt.classList.contains("on"))bt.click();
        var ex=document.querySelector('.explorer[data-key="'+x.a[0]+'"]');if(!quiet&&ex&&ex!==lastEx){lastEx=ex;var sc=ex.closest(".scene"),r=ex.getBoundingClientRect(),sr=sc.getBoundingClientRect();if(r.top<sr.top||r.top>sr.top+sr.height*.45)sc.scrollTo({top:sc.scrollTop+r.top-sr.top-12,behavior:"smooth"});}}
      if(x.sp&&window.__spot)window.__spot(x.sp[0],x.sp[1]);
      if(x.sar!==undefined){var sl=document.getElementById("sar-sl");if(sl){sl.value=x.sar;sl.dispatchEvent(new Event("input"));}}
      if(x.dc!==undefined){var pb=document.querySelectorAll("#dc-btns .pill")[x.dc];if(pb)pb.click();}
      if(x.go&&!quiet){var el=document.querySelector(x.go);if(el){var sc2=el.closest(".scene"),r2=el.getBoundingClientRect(),s2=sc2.getBoundingClientRect();sc2.scrollTo({top:sc2.scrollTop+r2.top-s2.top-12,behavior:"smooth"});}}}
    function resync(){var ct=a.currentTime;ci=0;while(ci<cues.length&&cues[ci][0]<=ct)ci++;
      for(var j=ci-1;j>=0;j--){if(cues[j][1].a){act(cues[j],true);break;}}}
    function loop(){if(!a||a.paused)return;if(sync.checked){var ct=a.currentTime;while(ci<cues.length&&cues[ci][0]<=ct){act(cues[ci]);ci++;}}raf=requestAnimationFrame(loop);}
    btn.addEventListener("click",function(){if(a&&!a.paused){if(!a._wired){a._wired=1;a.addEventListener("seeked",resync);a.addEventListener("play",function(){resync();cancelAnimationFrame(raf);loop();});a.addEventListener("ended",function(){ci=0;lastEx=null;});}
      resync();cancelAnimationFrame(raf);loop();}});
    box._pause=function(){''')
# case à cocher dans le lecteur
import re
s = s.replace('<button class="vo-tx" aria-expanded="false">Texte</button></div>',
              '<label class="vo-sl" title="La voix pilote le schéma et les graphiques"><input type="checkbox" class="vo-sync" checked> Schéma synchronisé</label><button class="vo-tx" aria-expanded="false">Texte</button></div>')
R('.vo-tx{', '''.vo-sl{display:flex;align-items:center;gap:6px;font-family:'IBM Plex Mono',monospace;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);white-space:nowrap;cursor:pointer}
.vo-sl input{accent-color:var(--hl);width:16px;height:16px}
@media(max-width:720px){.vo{flex-wrap:wrap}.vo-meta{flex:1 1 calc(100% - 60px)}.vo-sl{order:5}}
.vo-tx{''')
# module : mise en avant d'un faisceau
R('''window.__ensureViewer=async key=>{''', '''window.__spot=(key,f)=>{const v=viewers[key];if(v)v.spot(f);};
window.__ensureViewer=async key=>{''')
R('''  boneGhost(on){''', '''  spot(f){this.hover=f;this.applyStates();clearTimeout(this._spotT);this._spotT=setTimeout(()=>{if(this.hover===f){this.hover=-1;this.applyStates();}},3200);}
  boneGhost(on){''')
open(p, 'w', encoding='utf-8').write(s)
print(json.dumps({k: [round(c[0], 1) for c in v] for k, v in out.items()}))
