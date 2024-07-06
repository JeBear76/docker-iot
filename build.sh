cp angular-dist/browser/*.*s iotServer/iotServer/static/

for src in iotServer/iotServer/static/*.*s; do
  dest=$(echo $src | sed "s/\\-[0-9a-zA-Z]*\\././")
  mv $src $dest
done

