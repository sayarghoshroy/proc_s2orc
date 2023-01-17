mkdir temp
mkdir out
cd temp

metadata_path="/shared/data3/bowenj4/S2ORC/20200705v1/full/metadata/"

file_id=0

for file_id in {0..99}
do
	echo "Processing File "$file_id

	file_name="metadata_"$file_id".jsonl.gz"
	file_path="$metadata_path$file_name"
        cp $file_path .
        gzip -d $file_name

	meta_file="/home/sayar3/get_rel_work/temp/metadata_"$file_id".jsonl"
	IDs_file="/home/sayar3/get_rel_work/IDs_list.jsonl"
	out_file="/home/sayar3/get_rel_work/out/meta_out_"$file_id".jsonl"

	# 0: read_file, 1:IDs_file, 2: output file, 3: file ID
	python3 ../meta_fetch.py $meta_file $IDs_file $out_file $file_id
	rm $meta_file
done

echo "Task Completed"
