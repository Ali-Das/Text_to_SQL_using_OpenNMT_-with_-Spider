from utilities.json_to_jsonl_conversion_util import JsontoJsonlConversionUtil

# Creates parallel corpora
Jsonl_file_generator = JsontoJsonlConversionUtil()
print("building tables.jsonl..............")
Jsonl_file_generator.build_jsonl_file_from_json("tables")
print("building train.jsonl..............")
Jsonl_file_generator.build_jsonl_file_from_json("train_spider")
print("building dev.jsonl..............")
Jsonl_file_generator.build_jsonl_file_from_json("dev")
print("building test.jsonl..............")
Jsonl_file_generator.build_jsonl_file_from_json("train_others")
