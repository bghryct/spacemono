cp SpaceMono-HOI-V2.glyphs SpaceMono-HOI-Build.glyphs

python2 tools/fontmakeConvert.py SpaceMono-HOI-Build.glyphs

fontmake -o variable -g SpaceMono-HOI-Build.glyphs

rm -rf master_ufo
rm -rf SpaceMono-HOI-Build.glyphs

cd variable_ttf

gftools fix-nonhinting SpaceMono-VF.ttf SpaceMono-VF.ttf
gftools fix-dsig --autofix SpaceMono-VF.ttf
gftools fix-gasp SpaceMono-VF.ttf

ttx SpaceMono-VF.ttf

rm -rf SpaceMono-VF.ttf
rm -rf SpaceMono-VF-backup-fonttools-prep-gasp.ttf

cd ..

cat variable_ttf/SpaceMono-VF.ttx | tr '\n' '\r' | sed -e "s,<coord axis=\"ital\"[^v]* value=\"0.7\"\/>,<coord axis=\"ital\" max=\"1.0\" min=\"0.0\" value=\"0.7\"\/>,g" | sed -e "s,<coord axis=\"ITA2\"[^v]* value=\"0.7\"\/>,<coord axis=\"ITA2\" max=\"1.0\" min=\"0.0\" value=\"0.7\"\/>,g" | sed -e "s,<coord axis=\"ITA3\"[^v]* value=\"0.7\"\/>,<coord axis=\"ITA3\" max=\"1.0\" min=\"0.0\" value=\"0.7\"\/>,g" |tr '\r' '\n' > SpaceMono-VF-1.ttx
cat SpaceMono-VF-1.ttx | tr '\n' '\r' | sed -e "s,<coord axis=\"ital\"[^v]* value=\"1.0\"\/>,<coord axis=\"ital\" max=\"1.0\" min=\"0.7\" value=\"1.0\"\/>,g" | sed -e "s,<coord axis=\"ITA2\"[^v]* value=\"1.0\"\/>,<coord axis=\"ITA2\" max=\"1.0\" min=\"0.7\" value=\"1.0\"\/>,g" | sed -e "s,<coord axis=\"ITA3\"[^v]* value=\"1.0\"\/>,<coord axis=\"ITA3\" max=\"1.0\" min=\"0.7\" value=\"1.0\"\/>,g" |tr '\r' '\n' > SpaceMono-VF.ttx

rm -rf variable_ttf
rm -rf SpaceMono-VF-1.ttx

ttx SpaceMono-VF.ttx

rm -rf SpaceMono-VF.ttx