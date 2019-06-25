#!/bin/bash  

# Shell script to prepare the data for training

unzip Guns.zip -d gun | awk 'BEGIN { ORS = " " } { print "." }'
unzip real-life-violence-situations-dataset.zip | awk 'BEGIN { ORS = " " } { print "." }'

cd ./gun/
MP4Box -split 5 1.mp4
MP4Box -split 5 2.mp4
MP4Box -split 5 3.mp4
MP4Box -split 5 4.mp4
MP4Box -split 5 5.mp4
MP4Box -split 5 6.mp4
MP4Box -split 5 7.mp4
cd ..

rm ./gun/1.mp4 ./gun/2.mp4 ./gun/3.mp4 ./gun/4.mp4 ./gun/5.mp4 ./gun/6.mp4 ./gun/7.mp4
rm ./gun/1_001.mp4 ./gun/1_002.mp4 ./gun/1_129.mp4
rm ./gun/2_001.mp4 ./gun/2_002.mp4 ./gun/2_050.mp4
rm ./gun/3_001.mp4 ./gun/3_002.mp4 ./gun/3_003.mp4 ./gun/3_053.mp4
rm ./gun/4_001.mp4 ./gun/4_002.mp4 ./gun/4_039.mp4 ./gun/4_040.mp4
rm ./gun/5_001.mp4 ./gun/5_034.mp4 ./gun/5_035.mp4
rm ./gun/6_001.mp4
rm ./gun/7_001.mp4 ./gun/7_002.mp4 ./gun/7_020.mp4

mv ./gun/* ./train/Gun/
mv ./'Real Life Violence Dataset'/NonViolence/* ./train/Safe/
mv ./'Real Life Violence Dataset'/Violence/* ./train/Violence/

cd ./train/
cd ./Safe/ && for i in *.mp4;do name=`echo $i | cut -d'.' -f1`;echo $name;ffmpeg -loglevel panic -y -i "$i" -vcodec copy -acodec copy "${name}.avi";done
cd ../
cd ./Violence/ && for i in *.mp4;do name=`echo $i | cut -d'.' -f1`;echo $name;ffmpeg -loglevel panic -y -i "$i" -vcodec copy -acodec copy "${name}.avi";done
cd ../
cd ./Gun/ && for i in *.mp4;do name=`echo $i | cut -d'.' -f1`;echo $name;ffmpeg -loglevel panic -y -i "$i" -vcodec copy -acodec copy "${name}.avi";done
cd ../
cd ./Cold_Arms/ && for i in *.mp4;do name=`echo $i | cut -d'.' -f1`;echo $name;ffmpeg -loglevel panic -y -i "$i" -vcodec copy -acodec copy "${name}.avi";done
cd ../
cd ./Smoking/ && for i in *.mp4;do name=`echo $i | cut -d'.' -f1`;echo $name;ffmpeg -loglevel panic -y -i "$i" -vcodec copy -acodec copy "${name}.avi";done
cd ../
cd ./Kissing/ && for i in *.mp4;do name=`echo $i | cut -d'.' -f1`;echo $name;ffmpeg -loglevel panic -y -i "$i" -vcodec copy -acodec copy "${name}.avi";done
cd ../

mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np2_le_goo_0.avi' ./train/Safe/S_a.avi
mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np2_le_goo_1.avi' ./train/Safe/S_b.avi
mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np2_ba_goo_2.avi' ./train/Safe/S_c.avi
mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np2_le_goo_3.avi' ./train/Safe/S_d.avi
mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np2_le_goo_4.avi' ./train/Safe/S_e.avi
mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np4_le_goo_5.avi' ./train/Safe/S_f.avi
mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np2_ba_goo_6.avi' ./train/Safe/S_g.avi
mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np2_ba_goo_7.avi' ./train/Safe/S_h.avi
mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np2_ba_goo_8.avi' ./train/Safe/S_i.avi
mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np2_le_goo_9.avi' ./train/Safe/S_j.avi
mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np2_ba_goo_10.avi' ./train/Safe/S_k.avi
mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np2_le_goo_11.avi' ./train/Safe/S_l.avi
mv ./train/Safe/'-_FREE_HUGS_-_Abrazos_Gratis_www_abrazosgratis_org_hug_u_cm_np2_le_goo_12.avi' ./train/Safe/S_m.avi

rm ./train/*/*.mp4
rmdir gun 'Real Life Violence Dataset'

cd ./train/
k=1 && cd ./Safe/ && for i in *.avi;   do mv "$i" "S_${k}.avi";   k=$(($k+1)); done && cd ..
k=1 && cd ./Violence/ && for i in *.avi;   do mv "$i" "V_${k}.avi";   k=$(($k+1)); done && cd ..
k=1 && cd ./Gun/ && for i in *.avi;   do mv "$i" "G_${k}.avi";   k=$(($k+1)); done && cd ..
k=1 && cd ./Cold_Arms/ && for i in *.avi;   do mv "$i" "C_${k}.avi";   k=$(($k+1)); done && cd ..
k=1 && cd ./Smoking/ && for i in *.avi;   do mv "$i" "Sm_${k}.avi";   k=$(($k+1)); done && cd ..
k=1 && cd ./Kissing/ && for i in *.avi;   do mv "$i" "K_${k}.avi";   k=$(($k+1)); done && cd ..
cd ..

t=$(($(ls ./train/Safe/*|wc -w)/3)) && mv `ls ./train/Safe/* |head -$t ` ./test/Safe/
t=$(($(ls ./train/Violence/*|wc -w)/3)) && mv `ls ./train/Violence/* |head -$t ` ./test/Violence/
t=$(($(ls ./train/Gun/*|wc -w)/3)) && mv `ls ./train/Gun/* |head -$t ` ./test/Gun/
t=$(($(ls ./train/Cold_Arms/*|wc -w)/3)) && mv `ls ./train/Cold_Arms/* |head -$t ` ./test/Cold_Arms/
t=$(($(ls ./train/Smoking/*|wc -w)/3)) && mv `ls ./train/Smoking/* |head -$t ` ./test/Smoking/
t=$(($(ls ./train/Kissing/*|wc -w)/3)) && mv `ls ./train/Kissing/* |head -$t ` ./test/Kissing/
