from utilities.parallel_corpora_gen_util import ParallelCorporaGenUtil

parallel_corpora_generator = ParallelCorporaGenUtil()
print("building parallel corpora and gold file for training data.........")
parallel_corpora_generator.build_parallel_corpora_from_json("train")
print("building parallel corpora and gold file for Development Data Set.........")
parallel_corpora_generator.build_parallel_corpora_from_json("dev")
print("building parallel corpora and gold file for testing data.........")
parallel_corpora_generator.build_parallel_corpora_from_json("test")
