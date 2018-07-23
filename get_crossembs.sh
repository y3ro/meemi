#!/bin/sh

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

	echo "Applying orthogonal bilingual mapping..."
	EMBS1="$F1NAME.$DICTFNAME.ortho.w2v"
	EMBS2="$F2NAME.$DICTFNAME.ortho.w2v"
	python3 map_embeddings.py --normalize unit center --orthogonal "$F1" "$F2" "$D"/"$EMBS1" "$D"/"$EMBS2" -d "$DICTF"

	cd "$D"

elif [ "$4" = "-muse" ]; then
	head -n "$5" "$DICTF" > "$D"/"$DICTFNAME".train.txt
	tail -n "$6" "$DICTF" > "$D"/"$DICTFNAME".valid.txt

	cd $SCRIPT_DIR/utils/muse

	echo "Applying orthogonal bilingual mapping..."
	EMBS1="$F1NAME.$DICTFNAME.ortho.w2v"
	EMBS2="$F2NAME.$DICTFNAME.ortho.w2v"
	python3 supervised.py --src_lang "$F1NAME" --tgt_lang "$F2NAME" --src_emb $F1 --tgt_emb $F2 --n_refinement 5 --normalize_embeddings center,renorm --dico_train "$D"/"$DICTFNAME".train.txt --dico_eval "$D"/"$DICTFNAME".valid.txt --export txt --exp_id "$F1NAME-$F2NAME.$DICTFNAME"

	mv dumped/debug/"$F1NAME-$F2NAME.$DICTFNAME"/vectors-"$F1NAME".txt "$D"/"$EMBS1"
	mv dumped/debug/"$F1NAME-$F2NAME.$DICTFNAME"/vectors-"$F2NAME".txt "$D"/"$EMBS2"

	cd "$D"

else
	EMBS1="$F1"
	EMBS2="$F2"

fi

EMBS1BASE="$(basename $EMBS1)"
EMBS2BASE="$(basename $EMBS2)"
EMBS1NAME="${EMBS1BASE%.*}"
EMBS2NAME="${EMBS2BASE%.*}"

echo "Calculating cross-lingual means..."
python3 $SCRIPT_DIR/utils/get_means.py "$EMBS1" "$EMBS2" < "$DICTF" > "$EMBS1NAME-$EMBS2NAME.means.vec"

cut -f1 "$EMBS1NAME-$EMBS2NAME.means.vec" > "$EMBS1NAME.means.w2v"
$SCRIPT_DIR/utils/add_w2v_header.sh "$EMBS1NAME.means.w2v"
cut -f2 "$EMBS1NAME-$EMBS2NAME.means.vec" > "$EMBS2NAME.means.w2v"
$SCRIPT_DIR/utils/add_w2v_header.sh "$EMBS2NAME.means.w2v"

rm "$EMBS1NAME-$EMBS2NAME.means.vec"

cd $SCRIPT_DIR/utils/vecmap

echo "Getting final embeddings..."
python3 map_embeddings.py --unconstrained "$EMBS1" "$D"/"$EMBS1NAME".means.w2v "$D"/"$EMBS1NAME".met.w2v tmp -d "$DICTF"
python3 map_embeddings.py --unconstrained "$EMBS2" "$D"/"$EMBS2NAME".means.w2v "$D"/"$EMBS2NAME".met.w2v tmp -d "$DICTF"

rm tmp #TODO

cd "$D"
