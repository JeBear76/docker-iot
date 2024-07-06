cp angular-dist/browser/*.*s app/static/

for src in app/static/*.*; do
  dest=$(echo $src | sed "s/\\-[0-9a-zA-Z]*\\././")
  mv $src $dest
done

cp angular-dist/browser/index.html app/static/