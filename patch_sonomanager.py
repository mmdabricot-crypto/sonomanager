#!/usr/bin/env python3
"""
DABRIKSON — SonoManager Patch Script
Ajoute la page Références techniques dans index.html

Usage:
    python3 patch_sonomanager.py

Prérequis:
    - index.html dans le même dossier que ce script
    - references.html dans le même dossier (sera copié aussi)

Le script crée index.html modifié + une sauvegarde index.html.bak
"""

import os, re, shutil, sys

SRC = "index.html"
BAK = "index.html.bak"
DST = "index.html"

# ── Vérifications ────────────────────────────────────────────────────────────
if not os.path.exists(SRC):
    print(f"❌ Fichier '{SRC}' introuvable dans le dossier courant.")
    print(f"   Placez ce script dans le même dossier que index.html et relancez.")
    sys.exit(1)

# Sauvegarde
shutil.copy(SRC, BAK)
print(f"✅ Sauvegarde créée : {BAK}")

with open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

original = content
errors = []

# ════════════════════════════════════════════════════════════════════════════
# PATCH 1 — Ajouter le module "Références" dans le tableau MODULES
# ════════════════════════════════════════════════════════════════════════════
MODULE_OLD = "  {id:'snapshots', icon:'📁', name:'Snapshots Wing', desc:'Bibliothèque de configurations', color:'#A32D2D', bg:'linear-gradient(135deg,#A32D2D,#5a1010)',\n    stats:()=>[`${(S.snapshots||[]).length} snapshot${(S.snapshots||[]).length>1?'s':''}`,]},\n];"

MODULE_NEW = "  {id:'snapshots', icon:'📁', name:'Snapshots Wing', desc:'Bibliothèque de configurations', color:'#A32D2D', bg:'linear-gradient(135deg,#A32D2D,#5a1010)',\n    stats:()=>[`${(S.snapshots||[]).length} snapshot${(S.snapshots||[]).length>1?'s':''}`,]},\n  {id:'references', icon:'⚡', name:'Références', desc:'Câblage audio & électrique', color:'#2C2C2A', bg:'linear-gradient(135deg,#2C2C2A,#1a1a18)',\n    stats:()=>['XLR · Jack · SpeakON','P17 · Socapex · NF C15-100']},\n];"

if MODULE_OLD in content:
    content = content.replace(MODULE_OLD, MODULE_NEW)
    print("✅ PATCH 1 : Module 'Références' ajouté dans MODULES")
else:
    # Tentative plus souple
    alt = "    stats:()=>[`${(S.snapshots||[]).length} snapshot${(S.snapshots||[]).length>1?'s':''}`,]},\n];"
    if alt in content:
        content = content.replace(
            alt,
            "    stats:()=>[`${(S.snapshots||[]).length} snapshot${(S.snapshots||[]).length>1?'s':''}`,]},\n  {id:'references', icon:'⚡', name:'Références', desc:'Câblage audio & électrique', color:'#2C2C2A', bg:'linear-gradient(135deg,#2C2C2A,#1a1a18)',\n    stats:()=>['XLR · Jack · SpeakON','P17 · Socapex · NF C15-100']},\n];"
        )
        print("✅ PATCH 1 : Module 'Références' ajouté (méthode alt)")
    else:
        errors.append("PATCH 1 : Impossible de localiser la fin du tableau MODULES")
        print("⚠️  PATCH 1 échoué — voir INSTRUCTIONS MANUELLES en bas")

# ════════════════════════════════════════════════════════════════════════════
# PATCH 2 — Ajouter le panel HTML avant <div id="modal-root">
# ════════════════════════════════════════════════════════════════════════════
PANEL_OLD = '<div id="modal-root"></div>'

PANEL_NEW = """    <!-- ══ RÉFÉRENCES TECHNIQUES ══ -->
    <div class="panel" id="panel-references">
      <iframe
        src="references.html"
        style="width:100%;height:calc(100vh - 60px);border:none;border-radius:var(--radius-lg)"
        title="Références techniques DABRIKSON"
        loading="lazy">
      </iframe>
    </div>

<div id="modal-root"></div>"""

if PANEL_OLD in content:
    content = content.replace(PANEL_OLD, PANEL_NEW, 1)
    print("✅ PATCH 2 : Panel HTML 'panel-references' ajouté")
else:
    errors.append("PATCH 2 : Balise <div id=\"modal-root\"> introuvable")
    print("⚠️  PATCH 2 échoué — voir INSTRUCTIONS MANUELLES en bas")

# ════════════════════════════════════════════════════════════════════════════
# PATCH 3 — Ajouter la gestion navigation dans _showPanelNow
# ════════════════════════════════════════════════════════════════════════════
NAV_OLD = "  if(name==='snapshots')renderSnapshots();"
NAV_NEW = "  if(name==='snapshots')renderSnapshots();\n  if(name==='references'){/* iframe se charge automatiquement */}"

if NAV_OLD in content:
    content = content.replace(NAV_OLD, NAV_NEW, 1)
    print("✅ PATCH 3 : Navigation 'references' ajoutée dans _showPanelNow")
else:
    errors.append("PATCH 3 : Ligne 'renderSnapshots()' introuvable dans _showPanelNow")
    print("⚠️  PATCH 3 échoué — voir INSTRUCTIONS MANUELLES en bas")

# ════════════════════════════════════════════════════════════════════════════
# Écriture du fichier final
# ════════════════════════════════════════════════════════════════════════════
if content != original:
    with open(DST, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n✅ index.html mis à jour avec succès !")
else:
    print(f"\n⚠️  Aucune modification appliquée.")

# ════════════════════════════════════════════════════════════════════════════
# Instructions manuelles si patches échoués
# ════════════════════════════════════════════════════════════════════════════
if errors:
    print("\n" + "="*60)
    print("INSTRUCTIONS MANUELLES pour les patches échoués :")
    print("="*60)
    for e in errors:
        print(f"\n❌ {e}")

    print("""
────────────────────────────────────────────────────────────
PATCH 1 MANUEL — Dans le tableau MODULES, après le dernier
objet (snapshots), avant le '];', ajouter :

  {id:'references', icon:'⚡', name:'Références',
   desc:'Câblage audio & électrique',
   color:'#2C2C2A',
   bg:'linear-gradient(135deg,#2C2C2A,#1a1a18)',
   stats:()=>['XLR · Jack · SpeakON','P17 · Socapex · NF C15-100']},

────────────────────────────────────────────────────────────
PATCH 2 MANUEL — Avant <div id="modal-root"></div>, ajouter :

    <div class="panel" id="panel-references">
      <iframe
        src="references.html"
        style="width:100%;height:calc(100vh - 60px);border:none;border-radius:var(--radius-lg)"
        title="Références techniques DABRIKSON"
        loading="lazy">
      </iframe>
    </div>

────────────────────────────────────────────────────────────
PATCH 3 MANUEL — Dans la fonction _showPanelNow, après :
  if(name==='snapshots')renderSnapshots();
Ajouter :
  if(name==='references'){/* iframe se charge automatiquement */}
────────────────────────────────────────────────────────────
""")
else:
    print("\n🎉 Tous les patches appliqués. Uploadez index.html + references.html sur GitHub !")
    print("   → sonomanager-dabrikson.vercel.app sera mis à jour automatiquement.")
