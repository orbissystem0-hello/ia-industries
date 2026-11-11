#!/bin/bash
# Build ia_industries 1.0.x: models (m2) -> make8.py -> rename_1_0.py -> extra lang -> javac -> jar
set -e; cd /home/claude/build
(cd m2/out && PYTHONPATH=.. python3 ../cargo.py && PYTHONPATH=.. python3 ../warships.py)
python3 make8.py && python3 rename_1_0.py
python3 lang/gen_lang.py lang/out && cp lang/out/*.json proj10/resources/assets/ia_industries/lang/
cp icons3/icons/*.png proj10/resources/assets/ia_industries/textures/item/   # 64x64 item icons rendered from the models (icons3/mk.py)
rm -rf out10 stage10 && mkdir out10 stage10
javac -nowarn -encoding UTF-8 -cp "cp/*" -d out10 $(find proj10/src -name "*.java")
cp -r proj10/resources/. stage10/ && cp -r out10/. stage10/
mkdir -p stage10/sources && cp -r proj10/src/kr stage10/sources/kr && cp -r proj10/models_src stage10/sources/models
mkdir -p stage10/sources/icons && cp icons3/mk.py icons3/icon3.js stage10/sources/icons/
cp rename_1_0.py build_1_0.sh lang/gen_lang.py stage10/sources/ && cp make8.py stage10/sources/make_0.6.2.py && cp stage8/sources/make_0.2.0.py stage10/sources/
{ cat <<'LIC'
Create: Immersive Aircraft Industries (ia_industries) 1.0.0
Copyright (C) 2026 KAI_x_x
License: GNU General Public License v3.0 only (GPL-3.0-only), the same license as Immersive Aircraft, whose classes this mod extends.
Source code is included in this jar under sources/.
Models, textures and the icon in this mod are original work made for it.
Immersive Aircraft and Create are separate projects by their respective authors; this mod only depends on them.

================================================================================
LIC
cat /usr/share/common-licenses/GPL-3; } > stage10/LICENSE.txt
printf 'Manifest-Version: 1.0\nImplementation-Title: ia_industries\nImplementation-Version: 1.0.0\n' > mf10.txt
rm -rf dist10 && mkdir dist10 && jar cfm dist10/ia_industries-1.0.0.jar mf10.txt -C stage10 . 2>&1 | grep -v JAVA_TOOL || true
sha1sum dist10/ia_industries-1.0.0.jar
