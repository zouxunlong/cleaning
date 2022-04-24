from sentence_transformers import SentenceTransformer, models
from bitext_mining_utils import *
import numpy as np
import gzip
import time
from sklearn.decomposition import PCA
import torch

start_time = time.time()

modelPath = '../model/labse_bert_model'

model = SentenceTransformer(modelPath)


# Input files. We interpret every line as sentence.
file_src = "sentences.en"
file_tgt = "sentences.zh"
file_output = "parallel-sentences.en-zh"


# We base the scoring on k nearest neighbors for each element
knn_neighbors = 4

# Min score for text pairs. Note, score can be larger than 1
min_threshold = 0.5

sentences_src = set()
sentences_src_n_gram = set()
with open(file_src) as fIn:
    line0, line1, line2 = "", "", ""
    for line in fIn:
        line0 = line1
        line1 = line2
        line2 = line.strip()
        sentences_src.add(line2)
        sentences_src_n_gram.add(line2)
        sentences_src_n_gram.add(line1+" "+line2)
        sentences_src_n_gram.add(line0+" "+line1+" "+line2)

sentences_tgt = set()
sentences_tgt_n_gram = set()
with open(file_tgt) as fIn:
    line0, line1, line2 = "", "", ""
    for line in fIn:
        line0 = line1
        line1 = line2
        line2 = line.strip()
        sentences_tgt.add(line2)
        sentences_tgt_n_gram.add(line2)
        sentences_tgt_n_gram.add(line1+line2)
        sentences_tgt_n_gram.add(line0+line1+line2)


print("Source Sentences:", len(sentences_src))
print("Target Sentences:", len(sentences_tgt))
print("Source n-gram Sentences:", len(sentences_src_n_gram))
print("Target n-gram Sentences:", len(sentences_tgt_n_gram))


# Encode source sentences
sentences_src_n_gram = list(sentences_src_n_gram)

embeddings_src_n_gram = model.encode(
    sentences_src_n_gram, show_progress_bar=True, convert_to_numpy=True)


# Encode target sentences
sentences_tgt = list(sentences_tgt)

print("Encode target sentences")
embeddings_tgt = model.encode(
    sentences_tgt, show_progress_bar=True, convert_to_numpy=True)


# Normalize embeddings
x = embeddings_src_n_gram
x = x / np.linalg.norm(x, axis=1, keepdims=True)

y = embeddings_tgt
y = y / np.linalg.norm(y, axis=1, keepdims=True)

# Perform kNN in both directions
x2y_sim, x2y_ind = kNN(x, y, k=min([len(x), len(y), knn_neighbors]))
x2y_mean = x2y_sim.mean(axis=1)

y2x_sim, y2x_ind = kNN(y, x, k=min(([len(x), len(y), knn_neighbors])))
y2x_mean = y2x_sim.mean(axis=1)

# Compute forward and backward scores

def margin(a, b): return a / b

fwd_scores = score_candidates(x, y, x2y_ind, x2y_mean, y2x_mean, margin)
bwd_scores = score_candidates(y, x, y2x_ind, y2x_mean, x2y_mean, margin)
fwd_best = x2y_ind[np.arange(x.shape[0]), fwd_scores.argmax(axis=1)]
bwd_best = y2x_ind[np.arange(y.shape[0]), bwd_scores.argmax(axis=1)]

indices = np.stack([np.concatenate([np.arange(x.shape[0]), bwd_best]),
                   np.concatenate([fwd_best, np.arange(y.shape[0])])], axis=1)
scores = np.concatenate([fwd_scores.max(axis=1), bwd_scores.max(axis=1)])
seen_src, seen_trg = set(), set()

# Extact list of parallel sentences
print("Write sentences to disc")
sentences_written = 0
with open(file_output, 'w', encoding='utf8') as fOut:
    for i in np.argsort(-scores):
        src_ind, trg_ind = indices[i]
        src_ind = int(src_ind)
        trg_ind = int(trg_ind)

        if scores[i] < min_threshold:
            break

        if src_ind not in seen_src and trg_ind not in seen_trg:
            seen_src.add(src_ind)
            seen_trg.add(trg_ind)
            fOut.write("{:.4f} | {} | {}\n".format(scores[i], sentences_src_n_gram[src_ind].replace(
                "|", " "), sentences_tgt[trg_ind].replace("|", " ")))
            sentences_written += 1

print("Done. {} sentences written".format(sentences_written))
print("--- %s seconds ---" % (time.time() - start_time))
