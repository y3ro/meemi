#!/bin/sh

if [ $# -eq 1 ]; then
	echo "Usage: get_crossembs.sh embedding_file1 embedding_file2 dictionary_file [-vecmap | -muse train_size valid_size]"
	exit 1
fi

D=$PWD
F1="$(readlink -f $1)"
F2="$(readlink -f $2)"
DICTF="$(readlink -f $3)"
F1BASE="$(basename $1)"
F2BASE="$(basename $2)"
DICTFBASE="$(basename $3)"
F1NAME="${F1BASE%.*}"
F2NAME="${F2BASE%.*}"
DICTFNAME="${DICTFBASE%.*}"

SCRIPT_DIR_BASE=$(dirname "$0")
SCRIPT_DIR=$(readlink -f "$SCRIPT_DIR_BASE")

if [ "$4" = "-vecmap" ]; then

	cd $SCRIPT_DIR/utils/vecmap

	echo "Orthogonal bilingual mapping"
	EMBS1="$D"/"$F1NAME.$DICTFNAME.vecmap.w2v"
	EMBS2="$D"/"$F2NAME.$DICTFNAME.vecmap.w2v"
	python3 map_embeddings.py --normalize unit center --orthogonal "$F1" "$F2" "$EMBS1" "$EMBS2" -d "$DICTF"

	cd "$D"

elif [ "$4" = "-muse" ]; then
	head -n "$5" "$DICTF" > "$D"/"$DICTFNAME".train.txt
	tail -n "$6" "$DICTF" > "$D"/"$DICTFNAME".valid.txt

	cd $SCRIPT_DIR/utils/muse

	echo "Orthogonal bilingual mapping"
	EMBS1="$D"/"$F1NAME.$DICTFNAME.muse.w2v"
	EMBS2="$D"/"$F2NAME.$DICTFNAME.muse.w2v"
	python3 supervised.py --src_lang "$F1NAME" --tgt_lang "$F2NAME" --src_emb $F1 --tgt_emb $F2 --n_refinement 5 --normalize_embeddings center,renorm --dico_train "$D"/"$DICTFNAME".train.txt --dico_eval "$D"/"$DICTFNAME".valid.txt --export txt --exp_id "$F1NAME-$F2NAME.$DICTFNAME" --emb_dim "$(head -n 1 $F1 | cut -f 2 -d ' ')"

	mv dumped/debug/"$F1NAME-$F2NAME.$DICTFNAME"/vectors-"$F1NAME".txt "$EMBS1"
	mv dumped/debug/"$F1NAME-$F2NAME.$DICTFNAME"/vectors-"$F2NAME".txt "$EMBS2"
	rm -rf dumped/debug/"$F1NAME-$F2NAME.$DICTFNAME"

	rm "$D"/"$DICTFNAME".train.txt
	rm "$D"/"$DICTFNAME".valid.txt

	cd "$D"

else
	EMBS1="$F1"
	EMBS2="$F2"

fi

EMBS1BASE="$(basename $EMBS1)"
EMBS2BASE="$(basename $EMBS2)"
EMBS1NAME="${EMBS1BASE%.*}"
EMBS2NAME="${EMBS2BASE%.*}"

echo "Cross-lingual means"
python3 $SCRIPT_DIR/utils/get_means.py "$EMBS1" "$EMBS2" < "$DICTF" > "$EMBS1NAME-$EMBS2NAME.means.vec"

cut -f1 "$EMBS1NAME-$EMBS2NAME.means.vec" > "$EMBS1NAME.$DICTFNAME.means.w2v"
$SCRIPT_DIR/utils/add_w2v_header.sh "$EMBS1NAME.$DICTFNAME.means.w2v"
cut -f2 "$EMBS1NAME-$EMBS2NAME.means.vec" > "$EMBS2NAME.$DICTFNAME.means.w2v"
$SCRIPT_DIR/utils/add_w2v_header.sh "$EMBS2NAME.$DICTFNAME.means.w2v"

rm "$EMBS1NAME-$EMBS2NAME.means.vec"

cd $SCRIPT_DIR/utils/vecmap

echo "Mean mapping"
cut -f 1 -d " " < "$DICTF" > tmp
paste tmp tmp -d " " > "$DICTFNAME.rep1"
cut -f 2 -d " " < "$DICTF" > tmp
paste tmp tmp -d " " > "$DICTFNAME.rep2"
python3 map_embeddings.py --unconstrained "$EMBS1" "$D"/"$EMBS1NAME"."$DICTFNAME".means.w2v "$D"/"$EMBS1NAME"."$DICTFNAME".met.w2v tmp -d "$DICTFNAME.rep1"
python3 map_embeddings.py --unconstrained "$EMBS2" "$D"/"$EMBS2NAME"."$DICTFNAME".means.w2v "$D"/"$EMBS2NAME"."$DICTFNAME".met.w2v tmp -d "$DICTFNAME.rep2"

rm tmp #TODO
rm "$DICTFNAME.rep1"
rm "$DICTFNAME.rep2"

cd "$D"
