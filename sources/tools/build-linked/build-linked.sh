# Builds weight axis only VFs SpaceMono-HOI and SpaceMono-HOIItalic linked via the STAT table

mkdir VF-linked

cp SpaceMono-HOI.glyphs Build-Roman.glyphs
cp SpaceMono-HOI.glyphs Build-Italic.glyphs

python2 $(dirname ${BASH_SOURCE[0]})/delNonExp.py Build-Roman.glyphs
python2 $(dirname ${BASH_SOURCE[0]})/delNonExp.py Build-Italic.glyphs

python2 $(dirname ${BASH_SOURCE[0]})/prep-roman.py Build-Roman.glyphs
python2 $(dirname ${BASH_SOURCE[0]})/prep-italic.py Build-Italic.glyphs

# —————————————————————————————————————————————————————————————————————————————————————————————————————————————
# Build Roman —————————————————————————————————————————————————————————————————————————————————————————————————

fontmake -o variable -g Build-Roman.glyphs

rm -rf Build-Roman.glyphs

mv variable_ttf/SpaceMono-VF.ttf VF-linked/SpaceMono-Roman-VF.ttf

rm -rf master_ufo
rm -rf instance_ufo
rm -rf variable_ttf

# gftools fix-nonhinting SpaceMono-HOI-VF.ttf SpaceMono-HOI-VF.ttf
# gftools fix-dsig --autofix SpaceMono-HOI-VF.ttf
# gftools fix-gasp SpaceMono-HOI-VF.ttf

# ttx SpaceMono-HOI-VF.ttf

# rm -rf SpaceMono-HOI-VF.ttf
# rm -rf SpaceMono-HOI-VF-backup-fonttools-prep-gasp.ttf

# cat SpaceMono-HOI-VF.ttx | tr '\n' '\r' | sed -e "s~<name>.*<\/name>~$(cat $(dirname ${BASH_SOURCE[0]})/patchRoman-name.xml | tr '\n' '\r')~" | tr '\r' '\n' > SpaceMono-HOI-VF2.ttx
# cat SpaceMono-HOI-VF2.ttx | tr '\n' '\r' | sed -e "s~<STAT>.*<\/STAT>~$(cat $(dirname ${BASH_SOURCE[0]})/patchRoman-STAT.xml | tr '\n' '\r')~" | tr '\r' '\n' > SpaceMono-HOI-VF.ttx

# rm -rf SpaceMono-HOI-VF2.ttx

# ttx SpaceMono-HOI-VF.ttx

# rm -rf SpaceMono-HOI-VF.ttx

# mv SpaceMono-HOI-VF.ttf VF-linked/SpaceMono-HOI-Roman-VF.ttf


# # —————————————————————————————————————————————————————————————————————————————————————————————————————————————
# # Build Italic ————————————————————————————————————————————————————————————————————————————————————————————————

fontmake -o variable -g Build-Italic.glyphs

rm -rf Build-Italic.glyphs

mv variable_ttf/SpaceMono-ObliqueItalic-VF.ttf VF-linked/SpaceMono-Italic-VF.ttf

rm -rf master_ufo
rm -rf instance_ufo
rm -rf variable_ttf

# gftools fix-nonhinting SpaceMono-HOIItalic-VF.ttf SpaceMono-HOIItalic-VF.ttf
# gftools fix-dsig --autofix SpaceMono-HOIItalic-VF.ttf
# gftools fix-gasp SpaceMono-HOIItalic-VF.ttf

# ttx SpaceMono-HOIItalic-VF.ttf

# rm -rf SpaceMono-HOIItalic-VF.ttf
# rm -rf SpaceMono-HOIItalic-VF-backup-fonttools-prep-gasp.ttf


# cat SpaceMono-HOIItalic-VF.ttx | tr '\n' '\r' | sed -e "s~<STAT>.*<\/STAT>~$(cat $(dirname ${BASH_SOURCE[0]})/patchItalic-STAT.xml | tr '\n' '\r')~" | tr '\r' '\n' > SpaceMono-HOIItalic-VF2.ttx

# rm -rf SpaceMono-HOIItalic-VF.ttx

# mv SpaceMono-HOIItalic-VF2.ttx SpaceMono-HOIItalic-VF.ttx

# ttx SpaceMono-HOIItalic-VF.ttx

# rm -rf SpaceMono-HOIItalic-VF.ttx

# mv SpaceMono-HOIItalic-VF.ttf VF-linked/SpaceMono-HOI-Italic-VF.ttf
