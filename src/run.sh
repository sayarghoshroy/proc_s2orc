mkdir temp
mkdir out
cd temp

data_path="/shared/data3/bowenj4/S2ORC/20200705v1/full/pdf_parses/"
#metadata_path="/shared/data3/bowenj4/S2ORC/20200705v1/full/metadata"

file_id=0

for file_id in {15..99}
do
	echo "Processing File "$file_id
	file_name="pdf_parses_"$file_id".jsonl.gz"
	file_path="$data_path$file_name"
	cp $file_path .
	gzip -d $file_name

#       file_name="metadata_"$file_id".jsonl.gz
#	file_path="$metadata_path$file_name"
        #cp $file_path .
        #gzip -d $file_name

	work_file="/home/sayar3/get_rel_work/temp/pdf_parses_"$file_id".jsonl"
	#meta_file="/home/sayar3/get_rel_work/temp/metadata_"$file_id".jsonl"
	out_file="/home/sayar3/get_rel_work/out/out_"$file_id".jsonl"

	# 0: read_file, 1: output file, 2: file ID
	python3 ../create_rel_work.py $work_file $meta_file $out_file $file_id
	rm $work_file
done

echo "Task Completed"
