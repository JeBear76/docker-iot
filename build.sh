for src in angular-dist/*.*s; do
  dest=$(echo $src | sed "s/\\-[0-9a-zA-Z]*\\././")
  mv $src iotServer/static/$dest
done

