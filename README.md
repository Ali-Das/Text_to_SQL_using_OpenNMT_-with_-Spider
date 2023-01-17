## Text_to_SQL_using_OpenNMT_with_Spider_data: Text to SQL conversion using [OpenNMT](http://opennmt.net/) to do machine translation. 
This repo provides an implementation of a model developed using the open-source neural machine translation toolkit [OpenNMT](http://opennmt.net/)  for text_to_SQL translation on a parallel corpus generated using the [spider dataset](https://yale-lily.github.io/spider)

Table of Contents
=================
  * [Installation](#Installation)
  * [Quickstart](#quickstart)
  * [Alternative: Run on google colab](#alternative-run-on-google-colab)
  * [Citation](#citation)
  * [Acknowledgement](#Acknowledgement)


# Installation
The code is written in Python 3.5 and above.

## Step I:Install `OpenNMT-py` :

from `pip`:
```bash
pip install OpenNMT-py==1.2.0
```

or from the sources:
```bash
git clone https://github.com/OpenNMT/OpenNMT-py.git
cd OpenNMT-py
python setup.py install
```
## Step II: Install other dependency by running 
```bash
pip install -r requirements.opt.txt

```
## Step III: Download the Spider dataset.
The Spider dataset can be downloaded from [Here](https://yale-lily.github.io/spider) and stored in the spider/spider_data/db_and_json_files folder.

## Step IV: Create jsonl and various text files

### Step 1: Create jsonl files
```
python3  json_to_jsonl_conversion.py
```
### Step 2: create Parallel corpora for training, development and testing and gold files from the Spider dataset.
```
python3  parallel_corpora_gen.py
```
## Step V: Download Glove file for embedding
```
!mkdir "/content/drive/MYDrive/glove"
!wget http://nlp.stanford.edu/data/glove.6B.zip
!unzip glove.6B.zip -d "/content/drive/MyDrive/glove"
```

# Quickstart


## Step I: Preprocess the data
```bash
onmt_preprocess -train_src spider/spider_data/text_files/src_train.txt -train_tgt spider/spider_data/text_files/tgt_train.txt -valid_src spider/spider_data/text_files/src_dev.txt -valid_tgt spider/spider_data/text_files/tgt_dev.txt -save_data spider/spider_data/demo
```

After running the preprocessing, the following files are generated and stored in the spider/spider_data folder:

* `demo.train.pt`: serialized PyTorch file containing training data
* `demo.valid.pt`: serialized PyTorch file containing validation data
* `demo.vocab.pt`: serialized PyTorch file containing vocabulary data

## Step II: Create Glove embedding to torch 

```bash 
python tools/embeddings_to_torch.py -emb_file_both glove/glove.6B.100d.txt -dict_file spider/spider_data/demo.vocab.pt -output_file spider/spider_data/embeddings
```

After running the embeddings_to_torch.py, the following files are generated and stored in the spider/spider_data folder:

* `embeddings.enc.pt`: serialized PyTorch file containing embeddings for encoder
* `embeddings.dec.pt`: serialized PyTorch file containing embeddings for decoder
## Step III: Train the model

To train on CPU:

```bash
onmt_train -save_model spider/spider_data/model -batch_size 64 -layers 2 -rnn_size 500 -word_vec_size 500 -pre_word_vecs_enc spider/spider_data/embeddings.enc.pt -pre_word_vecs_dec spider/spider_data/embeddings.dec.pt -data spider/spider_data -world_size 1 -save_checkpoint_steps 10000 -report_every 5000   
```

To train on GPU:

```bash
onmt_train -save_model spider/spider_data/model -batch_size 64 -layers 2 -rnn_size 500 -word_vec_size 500 -pre_word_vecs_enc spider/spider_data/embeddings.enc.pt -pre_word_vecs_dec spider/spider_data/embeddings.dec.pt -data spider/spider_data -world_size 1 -gpu_ranks 0 -save_checkpoint_steps 10000 -report_every 5000 
```
The training parameters can be changed. Read [OpenNMT](http://opennmt.net/) for more information.

## Step IV: Translate
Now you have a model which you can use to predict on new data. We do this by running beam search. This will output predictions into `pred.txt`.

```bash
onmt_translate -model spider/spider_data/model_step_80000.pt -src spider/spider_data/text_files/src_test.txt -tgt spider/spider_data/text_files/tgt_test.txt -output spider/spider_data/text_files/pred.txt
```

## Step V: Evaluate
After translation,the queries of the predicted file can be evaluated by executing the evaluation.py python program of Spider.

```bash
python spider/evaluation.py \
--gold spider/spider_data/text_files/test_gold.txt \
--pred spider/spider_data/text_files/pred.txt --etype all \
--db spider/spider_data/db_and_json_files/database \
--table spider/spider_data/db_and_json_files/tables.json
```


# Alternative: Run on google colab
If you want to train in GPU or your system is not good enough to train the model, you can use[google colab](https://colab.research.google.com/notebooks/intro.ipynb).
upload the folder Text_to_SQL_using_OpenNMT to google drive. Open the file 'Text_to_SQL_using_OpenNMT.ipynb' in google colaboratory and execute the notebook codes of the file.

# Citation

> Alaka Das, Solving Text-to-SQL task through Machine Translation

# Acknowledgement

The implementation is based on 
[OpenNMT: Neural Machine Translation Toolkit](https://arxiv.org/pdf/1805.11462), 
[spider dataset](https://yale-lily.github.io/spider). 
Please cite them too if you use this code.

